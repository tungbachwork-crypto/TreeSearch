import React, { useState, useMemo } from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import nodeData from "./nodes_data.json";
import edgeData from "./edges_data.json";
import tc1 from "./Test Cases/testcase01.json";

const TESTCASES = { "01": tc1 };

const MODEL_MAP = {
  "XGBoost": "XGBoost",
  "LSTM": "LSTM",
  "GRU": "GRU"
};

const ALGO_KEY_MAP = {
  "Uniform Cost Search": "ucs",
  "A* Search": "astar",
  "Breadth-First Search": "bfs",
  "Depth-First Search": "dfs",
  "Greedy Best-First Search": "gbfs",
  "Theta* Search": "theta"
};

const WIDTH = 900;
const HEIGHT = 750;
const TrafficGraph = () => {

  // STATE MANAGEMENT
  const [selectedCase, setSelectedCase] = useState("01");
  const [selectedModel, setSelectedModel] = useState("GRU");
  const [selectedAlgo, setSelectedAlgo] = useState("A* Search");
  const [selectedRouteIndex, setSelectedRouteIndex] = useState(0);
  const [hoveredNode, setHoveredNode] = useState(null);
  const [hoveredEdge, setHoveredEdge] = useState(null);
  const [mousePos, setMousePos] = useState({ x: 0, y: 0 });
  const [edgesWithCost, setEdgesWithCost] = useState([]);
  const [flows, setFlows] = useState({});
  const [results, setResults] = useState({});
  const [loading, setLoading] = useState(false);

  const currentTC = TESTCASES[selectedCase]?.[0] || tc1[0];

  const highlightedIds = [
    currentTC.origin.toString(),
    currentTC.destination.toString()
  ];

  // CREATE NODE MAP
  const nodeMap = useMemo(() => {
    const map = {};
    nodeData.forEach(n => (map[n.id.toString()] = n));
    return map;
  }, []);

  // SCALE LAT/LNG → SVG COORDS
  const { scaleX, scaleY } = useMemo(() => {
    const lats = nodeData.map(n => n.latitude);
    const lngs = nodeData.map(n => n.longitude);

    const minLat = Math.min(...lats);
    const maxLat = Math.max(...lats);
    const minLng = Math.min(...lngs);
    const maxLng = Math.max(...lngs);

    // Fit graph nicely inside SVG
    const baseScale = Math.min(
      780 / (maxLng - minLng || 1),
      630 / (maxLat - minLat || 1)
    );

    return {
      scaleX: lng => (lng - minLng) * baseScale + 60,
      scaleY: lat => (maxLat - lat) * baseScale + 60 // invert Y axis
    };
  }, []);

  // CALL BACKEND API
  const simulate = async () => {
    setLoading(true);
    setSelectedRouteIndex(0); // reset route selection

    try {
      const res = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          origin: currentTC.origin,
          destination: currentTC.destination,
          timestamp: currentTC.date,
          model: MODEL_MAP[selectedModel]
        })
      });

      const data = await res.json();

      // Ensure all results are arrays
      const formattedResults = {};
      Object.keys(data.results || {}).forEach(key => {
        const val = data.results[key];
        formattedResults[key] = Array.isArray(val) ? val : [val];
      });

      setEdgesWithCost(data.edges || []);
      setFlows(data.flows || {});
      setResults(formattedResults);

    } catch (err) {
      console.error("API Error:", err);
    }

    setLoading(false);
  };

  // Track mouse position for tooltip
  const handleMouseMove = (e) => {
    setMousePos({ x: e.clientX, y: e.clientY });
  };

  // DETERMINE EDGE STATUS
  const getEdgeStatus = (u, v) => {
    const routes = results[ALGO_KEY_MAP[selectedAlgo]] || [];
  
    // Check SELECTED route
    const selectedRoute = routes[selectedRouteIndex];
    if (selectedRoute) {
      const path = selectedRoute.path || [];
      for (let i = 0; i < path.length - 1; i++) {
        if (
          String(path[i]) === String(u) &&
          String(path[i + 1]) === String(v)
        ) {
          return "selected"; // highlight best route
        }
      }
    }
  
    // Check OTHER routes
    for (let rIdx = 0; rIdx < routes.length; rIdx++) {
      if (rIdx === selectedRouteIndex) continue;
  
      const path = routes[rIdx].path || [];
  
      for (let i = 0; i < path.length - 1; i++) {
        if (
          String(path[i]) === String(u) &&
          String(path[i + 1]) === String(v)
        ) {
          return "other"; // secondary routes
        }
      }
    }
  
    return "none"; // not part of any route
  };

  return (
    <div className="app-container" onMouseMove={handleMouseMove}>
      {(hoveredNode || hoveredEdge) && (
        <div
          className="tooltip"
          style={{ left: mousePos.x + 15, top: mousePos.y + 15 }}
        >
          {hoveredNode ? (
            <>
              <strong>Node: {hoveredNode}</strong>
              <p>
                Flow:{" "}
                {flows[String(hoveredNode)]?.toFixed(2) || "0.00"}
              </p>
            </>
          ) : (
            <>
              <strong>
                Edge: {hoveredEdge.u} → {hoveredEdge.v}
              </strong>
              <p>Cost: {hoveredEdge.cost.toFixed(5)}</p>
            </>
          )}
        </div>
      )}
      <div className="graph-container">
        <svg width={WIDTH} height={HEIGHT} className="graph-svg">

          {/* EDGES */}
          {(edgesWithCost.length > 0 ? edgesWithCost : edgeData).map((edge, i) => {
            const u = Array.isArray(edge) ? edge[0] : edge.from;
            const v = Array.isArray(edge) ? edge[1] : edge.to;
            const cost = Array.isArray(edge) ? edge[2] : 0;

            const from = nodeMap[String(u)];
            const to = nodeMap[String(v)];
            if (!from || !to) return null;

            const status = getEdgeStatus(u, v);

            return (
              <line
                key={`e-${i}`}
                x1={scaleX(from.longitude)}
                y1={scaleY(from.latitude)}
                x2={scaleX(to.longitude)}
                y2={scaleY(to.latitude)}

                // Styling based on route status
                stroke={
                  status === "selected"
                    ? "#22c55e"
                    : status === "other"
                    ? "#94a3b8"
                    : "#334155"
                }

                strokeWidth={
                  status === "selected"
                    ? 6
                    : status === "other"
                    ? 3
                    : 1.5
                }

                strokeOpacity={
                  status === "selected"
                    ? 1
                    : status === "other"
                    ? 0.3
                    : 0.6
                }

                onMouseEnter={() => setHoveredEdge({ u, v, cost })}
                onMouseLeave={() => setHoveredEdge(null)}
              />
            );
          })}

          {/* NODES */}
          {nodeData.map(node => (
            <circle
              key={node.id}
              cx={scaleX(node.longitude)}
              cy={scaleY(node.latitude)}
              r={highlightedIds.includes(String(node.id)) ? 8 : 4}
              fill={
                highlightedIds.includes(String(node.id))
                  ? "#f43f5e" // origin/destination
                  : "#64748b"
              }
              onMouseEnter={() => setHoveredNode(String(node.id))}
              onMouseLeave={() => setHoveredNode(null)}
            />
          ))}

        </svg>
      </div>
      <div className="sidebar">
        <h2>Traffic AI Control</h2>

        {/* Test Case Selector */}
        <div className="control-group">
          <label>Test Case</label>
          <select value={selectedCase} onChange={(e) => setSelectedCase(e.target.value)}>
            {Object.keys(TESTCASES).map(num => (
              <option key={num} value={num}>{num}</option>
            ))}
          </select>
        </div>

        {/* Model Selector */}
        <div className="control-group">
          <label>Model</label>
          <select value={selectedModel} onChange={(e) => setSelectedModel(e.target.value)}>
            {Object.keys(MODEL_MAP).map(m => (
              <option key={m} value={m}>{m}</option>
            ))}
          </select>
        </div>

        {/* Algorithm Selector */}
        <div className="control-group">
          <label>Algorithm</label>
          <select value={selectedAlgo} onChange={(e) => setSelectedAlgo(e.target.value)}>
            {Object.keys(ALGO_KEY_MAP).map(a => (
              <option key={a} value={a}>{a}</option>
            ))}
          </select>
        </div>

        {/* Run Button */}
        <button onClick={simulate} disabled={loading} className="run-btn">
          {loading ? "⌛ Running..." : "🚀 Run Simulation"}
        </button>

        {/* ROUTE LIST */}
        <div className="info-box">
          <h3>Top 5 Routes</h3>

          <div className="route-list">
            {(results[ALGO_KEY_MAP[selectedAlgo]] || []).map((r, i) => (
              <div
                key={i}
                className={`route-item ${i === selectedRouteIndex ? "best" : ""}`}
                onClick={() => setSelectedRouteIndex(i)}
                style={{ cursor: "pointer" }}
              >
                <span>#{i + 1}</span>
                <span>{(r.cost * 60).toFixed(2)} mins</span>
              </div>
            ))}
          </div>
        </div>

      </div>
    </div>
  );
};

// RENDER APP
const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<TrafficGraph />);