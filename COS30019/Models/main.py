import os
import json
import joblib
import torch
import torch.nn as nn
import pandas as pd
import numpy as np
import sys
import math

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SEARCH_DIR = os.path.normpath(os.path.join(BASE_DIR, '..', 'Search Algorithms'))
WEBSITE_DIR = os.path.normpath(os.path.join(BASE_DIR, '..', 'Website'))

if SEARCH_DIR not in sys.path:
    sys.path.append(SEARCH_DIR)

from a_star import a_star
from bfs import bfs
from dfs import dfs
from gbfs import gbfs
from cus1 import ucs
from cus2 import theta_star
from k_shortest_paths import get_k_shortest_paths 

# 1: MODEL CLASSES 

# LSTM Model
class LSTMModel(nn.Module):
    def __init__(self, input_size, hidden_size, output_size, num_layers=2):
        super(LSTMModel, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers

        # LSTM layer
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)

        # Fully connected output layer
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        # Initialize hidden state (h0) and cell state (c0)
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)

        # Forward pass through LSTM
        out, _ = self.lstm(x, (h0, c0))

        # Take output from last time step
        return self.fc(out[:, -1, :])


# GRU Model
class GRUModel(nn.Module):
    def __init__(self, input_size, hidden_size, output_size, num_layers=2):
        super(GRUModel, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers

        # GRU layer
        self.gru = nn.GRU(input_size, hidden_size, num_layers, batch_first=True)

        # Output layer
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        # Initialize hidden state
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)

        # Forward pass
        out, _ = self.gru(x, h0)

        # Last time step output
        return self.fc(out[:, -1, :])

# 2: HELPER FUNCTIONS

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km

    # Convert degrees → radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Differences
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Haversine formula
    a = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    return R * c


def load_nodes():
    path = os.path.join(WEBSITE_DIR, "nodes_data.json")

    with open(path, "r") as f:
        data = json.load(f)

    return {
        str(node["id"]): (node["latitude"], node["longitude"])
        for node in data
    }


def load_edges():
    path = os.path.join(WEBSITE_DIR, "edges_data.json")

    with open(path, "r") as f:
        data = json.load(f)

    # Weight is set to 0 for now (will compute later)
    return [(str(e["from"]), str(e["to"]), 0) for e in data]

# 3: FLOW PREDICTION

def predict_node_flow(timestamp, model_type):
    scaler_X = joblib.load(os.path.join(BASE_DIR, 'scaler_X.pkl'))
    scaler_y = joblib.load(os.path.join(BASE_DIR, 'scaler_y.pkl'))
    node_ids = joblib.load(os.path.join(BASE_DIR, 'node_ids.pkl'))

    # Convert timestamp → features
    t = pd.to_datetime(timestamp)
    features = np.array([[t.hour, t.dayofweek, t.minute]])

    # Scale features
    features_scaled = scaler_X.transform(features)

    if model_type == "XGBoost":
        model = joblib.load(os.path.join(BASE_DIR, 'xgboost_model.pkl'))
        preds_scaled = model.predict(features_scaled).reshape(1, -1)

    else:
        input_size, hidden_size, output_size = 3, 64, len(node_ids)
        if model_type == "LSTM":
            model = LSTMModel(input_size, hidden_size, output_size)
            weights = 'lstm_weights.pth'
        else:
            model = GRUModel(input_size, hidden_size, output_size)
            weights = 'gru_weights.pth'

        model.load_state_dict(
            torch.load(os.path.join(BASE_DIR, weights), map_location='cpu', weights_only=True)
        )
        model.eval()

        # Prepare tensor
        feat_t = torch.tensor(features_scaled, dtype=torch.float32).unsqueeze(1)

        # Run inference
        with torch.no_grad():
            preds_scaled = model(feat_t).numpy()

    # Convert back to real values
    flows = scaler_y.inverse_transform(preds_scaled)[0]

    # Return dictionary: {node_id: flow}
    return {
        str(node_id): float(flow)
        for node_id, flow in zip(node_ids, flows)
    }

# 6: COST CALCULATION

def compute_costs(edges, flow_dict, coords):
    SPEED = 60  # km/h
    NODE_DELAY = 30 / 3600  # 30 seconds → hours

    node_costs = {
        str(node): max(0, float(flow)) / 200
        for node, flow in flow_dict.items()
    }

    weighted_edges = []

    for (u, v, _) in edges:
        u_str, v_str = str(u), str(v)

        # Skip if coordinates missing
        if u_str not in coords or v_str not in coords:
            continue

        lat1, lon1 = coords[u_str]
        lat2, lon2 = coords[v_str]

        # Distance between nodes
        dist = haversine(lat1, lon1, lat2, lon2)

        # Total cost formula:
        # travel time + delay + congestion penalty
        total_cost = float(
            (dist / SPEED) +
            NODE_DELAY +
            node_costs.get(v_str, 0)
        )

        weighted_edges.append((u_str, v_str, total_cost))

    return weighted_edges, node_costs


def build_graph(weighted_edges):

    graph = {}

    for u, v, cost in weighted_edges:
        graph.setdefault(u, {})[v] = cost

    return graph

# 7: NAVIGATION

def run_navigation(origin, destination, timestamp, model_type="GRU"):

    origin_str, dest_str = str(origin), str(destination)

    # Load map data
    coords = load_nodes()
    raw_edges = load_edges()

    # Predict traffic flow at given time
    flow_dict = predict_node_flow(timestamp, model_type)

    # Compute edge weights based on traffic
    weighted_edges, _ = compute_costs(raw_edges, flow_dict, coords)

    # Build graph
    graph = build_graph(weighted_edges)

    results = {}
    k_val = 5  # number of shortest paths to return

    results["astar"] = get_k_shortest_paths(
        graph, coords, origin_str, dest_str,
        k=k_val, algorithm_func=a_star
    )

    results["ucs"] = get_k_shortest_paths(
        graph, coords, origin_str, dest_str,
        k=k_val,
        algorithm_func=lambda g, c, o, d: ucs(g, o, d)
    )

    results["bfs"] = get_k_shortest_paths(
        graph, coords, origin_str, dest_str,
        k=k_val,
        algorithm_func=lambda g, c, o, d: bfs(g, o, d)
    )

    results["gbfs"] = get_k_shortest_paths(
        graph, coords, origin_str, dest_str,
        k=k_val,
        algorithm_func=gbfs
    )

    results["theta"] = get_k_shortest_paths(
        graph, coords, origin_str, dest_str,
        k=k_val,
        algorithm_func=theta_star
    )

    results["dfs"] = get_k_shortest_paths(
        graph, coords, origin_str, dest_str,
        k=k_val,
        algorithm_func=lambda g, c, o, d: dfs(g, o, d)
    )

    return {
        "flows": flow_dict,      # predicted traffic per node
        "results": results,      # paths from each algorithm
        "edges": weighted_edges  # graph with costs
    }