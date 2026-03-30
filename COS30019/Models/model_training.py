import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import xgboost as xgb
from sklearn.multioutput import MultiOutputRegressor
from sklearn.preprocessing import MinMaxScaler
import joblib


# 1: Load and Preprocess Data
# Load processed CSV and Convert Timestamp column to datetime format
df = pd.read_csv('processed_traffic_data.csv')
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# Rows → Timestamp
# Columns → SCATS sensors (nodes)
# Values → Flow (traffic)
pivot_df = df.pivot_table(
    index='Timestamp',
    columns='SCATS Number',
    values='Flow',
    aggfunc='mean'
).fillna(0)  # Replace missing values with 0

# 2: Feature Engineering
pivot_df['hour'] = pivot_df.index.hour
pivot_df['day_of_week'] = pivot_df.index.dayofweek
pivot_df['minute'] = pivot_df.index.minute

# STEP 3: Define Inputs (X) and Outputs (y)

# Target columns = SCATS node IDs (traffic sensors)
target_cols = [c for c in pivot_df.columns if isinstance(c, (int, float, np.integer))]

# X = time features
X = pivot_df[['hour', 'day_of_week', 'minute']].values

# y = traffic flow at all nodes
y = pivot_df[target_cols].values

# 4: Scale Data (IMPORTANT for ML models)
# Normalize values to range [0,1]
scaler_X = MinMaxScaler()
scaler_y = MinMaxScaler()

X_scaled = scaler_X.fit_transform(X)
y_scaled = scaler_y.fit_transform(y)

# Save scalers
joblib.dump(scaler_X, 'scaler_X.pkl')
joblib.dump(scaler_y, 'scaler_y.pkl')
joblib.dump(target_cols, 'node_ids.pkl')

# 5: Define Deep Learning Models (LSTM & GRU)
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

# 6: Prepare Data for PyTorch
# Convert numpy arrays → PyTorch tensors

# Add sequence dimension:
# Shape becomes (batch_size, sequence_length=1, features=3)
X_train_t = torch.tensor(X_scaled, dtype=torch.float32).unsqueeze(1)

# Output tensor
y_train_t = torch.tensor(y_scaled, dtype=torch.float32)

# Create DataLoader (for batching)
loader = DataLoader(
    TensorDataset(X_train_t, y_train_t),
    batch_size=32,
    shuffle=True
)

# 7: Training Function
def train_loop(model, loader, epochs=20):
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    criterion = nn.MSELoss()  # Mean Squared Error loss

    model.train()

    for epoch in range(epochs):
        total_loss = 0

        for bx, by in loader:
            optimizer.zero_grad()

            # Forward pass
            output = model(bx)

            # Compute loss
            loss = criterion(output, by)

            # Backpropagation
            loss.backward()
            optimizer.step()

            total_loss += loss.item()

        # Print progress every 5 epochs
        if (epoch + 1) % 5 == 0:
            print(f"Epoch {epoch+1}/{epochs}, Loss: {total_loss/len(loader):.6f}")

    return model

# 8: Train Models
INPUT_SIZE = 3 # hour, day_of_week, minute
HIDDEN_SIZE = 64 # neurons in hidden layers
NUM_LAYERS = 2
OUTPUT_SIZE = len(target_cols)  # number of nodes

# Train LSTM
print(f"\nTraining LSTM ({NUM_LAYERS} Layers)...")
lstm_node = LSTMModel(INPUT_SIZE, HIDDEN_SIZE, OUTPUT_SIZE, NUM_LAYERS)
lstm_node = train_loop(lstm_node, loader)
torch.save(lstm_node.state_dict(), 'lstm_weights.pth')

# Train GRU
print(f"\nTraining GRU ({NUM_LAYERS} Layers)...")
gru_node = GRUModel(INPUT_SIZE, HIDDEN_SIZE, OUTPUT_SIZE, NUM_LAYERS)
gru_node = train_loop(gru_node, loader)
torch.save(gru_node.state_dict(), 'gru_weights.pth')


# Train XGBoost
print("\nTraining XGBoost...")
# XGBoost works with 2D data (not sequence data)
xgb_reg = xgb.XGBRegressor(
    n_estimators=100,
    max_depth=5,
    learning_rate=0.1
)
xgb_model = MultiOutputRegressor(xgb_reg)
xgb_model.fit(X_scaled, y_scaled)
joblib.dump(xgb_model, 'xgboost_model.pkl')

# 9: Complete
print("SUCCESS: All models and scalers saved!")
print("Files generated:")
print("- lstm_weights.pth")
print("- gru_weights.pth")
print("- xgboost_model.pkl")
print("- scaler_X.pkl")
print("- scaler_y.pkl")
print("- node_ids.pkl")
