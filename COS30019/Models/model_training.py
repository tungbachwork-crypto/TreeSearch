import pandas as pd
import numpy as np
import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import xgboost as xgb
from sklearn.multioutput import MultiOutputRegressor
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error
import joblib

# Base directory = folder containing this script (Models/)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def cyclic_encode(values, max_val):
    """Encode cyclic features (hour, minute, day_of_week) as sin/cos pairs.

    Why: hour=23 and hour=0 are only 1 hour apart,
    but as integers the model sees a gap of 23.
    Sin/cos encoding preserves the circular relationship.
    """
    sin = np.sin(2 * np.pi * values / max_val)
    cos = np.cos(2 * np.pi * values / max_val)
    return sin, cos


def build_cyclic_features(pivot_df):
    """Extract hour, minute, day_of_week from index and convert to 6 cyclic features.

    Returns numpy array of shape (N, 6):
        [hour_sin, hour_cos, minute_sin, minute_cos, dow_sin, dow_cos]
    """
    hour = pivot_df.index.hour
    minute = pivot_df.index.minute
    dow = pivot_df.index.dayofweek

    hour_sin, hour_cos = cyclic_encode(hour, 24)
    minute_sin, minute_cos = cyclic_encode(minute, 60)
    dow_sin, dow_cos = cyclic_encode(dow, 7)

    return np.column_stack([
        hour_sin, hour_cos,
        minute_sin, minute_cos,
        dow_sin, dow_cos
    ])


def create_sequences(features, targets, seq_len=4):
    """Create sliding window sequences for LSTM/GRU.

    For each time step t, the input is features[t-seq_len : t]
    and the target is targets[t].

    This gives the model 'seq_len' past time steps as context.
    With 15-minute intervals and seq_len=4, the model sees 1 hour of history.

    Args:
        features: (N, 6) array of cyclic features
        targets:  (N, num_nodes) array of scaled flow values
        seq_len:  number of past time steps to include

    Returns:
        X_seq: (N - seq_len, seq_len, 6)
        y_seq: (N - seq_len, num_nodes)
    """
    X_seq, y_seq = [], []
    for i in range(seq_len, len(features)):
        X_seq.append(features[i - seq_len : i])
        y_seq.append(targets[i])
    return np.array(X_seq), np.array(y_seq)


# ============================================================
# 1: LOAD AND PREPROCESS DATA
# ============================================================

# Load processed CSV and convert Timestamp to datetime
df = pd.read_csv(os.path.join(BASE_DIR, 'processed_traffic_data.csv'))
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# Pivot: Rows → Timestamp, Columns → SCATS sensors, Values → Flow
pivot_df = df.pivot_table(
    index='Timestamp',
    columns='SCATS Number',
    values='Flow',
    aggfunc='mean'
).fillna(0)

# Sort by timestamp (important for sliding window)
pivot_df = pivot_df.sort_index()

# ============================================================
# 2: FEATURE ENGINEERING — Cyclic Encoding
# ============================================================

# Build 6 cyclic features: hour_sin/cos, minute_sin/cos, dow_sin/cos
# These are already in range [-1, 1], so no scaler needed for X
X = build_cyclic_features(pivot_df)

# Target columns = SCATS node IDs
target_cols = [c for c in pivot_df.columns if isinstance(c, (int, float, np.integer))]
y = pivot_df[target_cols].values

# ============================================================
# 3: SCALE TARGET DATA
# ============================================================

# Only scale y (traffic flows). X (sin/cos) is already normalized.
scaler_y = MinMaxScaler()
y_scaled = scaler_y.fit_transform(y)

# Save scaler and metadata
joblib.dump(scaler_y, os.path.join(BASE_DIR, 'scaler_y.pkl'))
joblib.dump(target_cols, os.path.join(BASE_DIR, 'node_ids.pkl'))

# ============================================================
# 4: PREPARE DATA FOR EACH MODEL TYPE
# ============================================================

# --- Hyperparameters ---
SEQ_LEN = 4        # sliding window size (4 steps × 15 min = 1 hour)
INPUT_SIZE = 6      # 6 cyclic features
HIDDEN_SIZE = 64
NUM_LAYERS = 2
OUTPUT_SIZE = len(target_cols)
EPOCHS = 50

# Save metadata for inference
metadata = {
    'SEQ_LEN': SEQ_LEN,
    'INPUT_SIZE': INPUT_SIZE,
    'HIDDEN_SIZE': HIDDEN_SIZE,
    'NUM_LAYERS': NUM_LAYERS,
    'OUTPUT_SIZE': OUTPUT_SIZE,
}
joblib.dump(metadata, os.path.join(BASE_DIR, 'model_metadata.pkl'))

# --- LSTM/GRU data: 3D sequences ---
X_seq, y_seq = create_sequences(X, y_scaled, seq_len=SEQ_LEN)
X_seq_t = torch.tensor(X_seq, dtype=torch.float32)     # (N-SEQ_LEN, SEQ_LEN, 6)
y_seq_t = torch.tensor(y_seq, dtype=torch.float32)      # (N-SEQ_LEN, num_nodes)

seq_loader = DataLoader(
    TensorDataset(X_seq_t, y_seq_t),
    batch_size=32,
    shuffle=True
)

# --- XGBoost data: 2D flat (no sliding window) ---
# XGBoost is not a sequence model, so it uses flat features
X_flat = X          # (N, 6)
y_flat = y_scaled   # (N, num_nodes)

print(f"Dataset size: {len(X)} samples")
print(f"LSTM/GRU sequences: {len(X_seq)} (after sliding window, SEQ_LEN={SEQ_LEN})")
print(f"Features: {INPUT_SIZE} cyclic (hour_sin/cos, minute_sin/cos, dow_sin/cos)")
print(f"Targets: {OUTPUT_SIZE} SCATS nodes")
print(f"Epochs: {EPOCHS}")

# ============================================================
# 5: MODEL DEFINITIONS
# ============================================================

class LSTMModel(nn.Module):
    def __init__(self, input_size, hidden_size, output_size, num_layers=2):
        super(LSTMModel, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        out, _ = self.lstm(x, (h0, c0))
        return self.fc(out[:, -1, :])


class GRUModel(nn.Module):
    def __init__(self, input_size, hidden_size, output_size, num_layers=2):
        super(GRUModel, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.gru = nn.GRU(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        out, _ = self.gru(x, h0)
        return self.fc(out[:, -1, :])


# ============================================================
# 6: TRAINING FUNCTION
# ============================================================

def train_loop(model, loader, epochs=EPOCHS):
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    criterion = nn.MSELoss()

    model.train()

    for epoch in range(epochs):
        total_loss = 0
        for bx, by in loader:
            optimizer.zero_grad()
            output = model(bx)
            loss = criterion(output, by)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()

        if (epoch + 1) % 10 == 0:
            print(f"  Epoch {epoch+1}/{epochs}, Loss: {total_loss/len(loader):.6f}")

    return model


# ============================================================
# 7: TRAIN ALL MODELS
# ============================================================

# --- Train LSTM ---
print(f"\n{'='*50}")
print(f"Training LSTM ({NUM_LAYERS} layers, {HIDDEN_SIZE} hidden, {EPOCHS} epochs)")
print(f"{'='*50}")
lstm_model = LSTMModel(INPUT_SIZE, HIDDEN_SIZE, OUTPUT_SIZE, NUM_LAYERS)
lstm_model = train_loop(lstm_model, seq_loader)
torch.save(lstm_model.state_dict(), os.path.join(BASE_DIR, 'lstm_weights.pth'))

# --- Train GRU ---
print(f"\n{'='*50}")
print(f"Training GRU ({NUM_LAYERS} layers, {HIDDEN_SIZE} hidden, {EPOCHS} epochs)")
print(f"{'='*50}")
gru_model = GRUModel(INPUT_SIZE, HIDDEN_SIZE, OUTPUT_SIZE, NUM_LAYERS)
gru_model = train_loop(gru_model, seq_loader)
torch.save(gru_model.state_dict(), os.path.join(BASE_DIR, 'gru_weights.pth'))

# --- Train XGBoost ---
print(f"\n{'='*50}")
print("Training XGBoost")
print(f"{'='*50}")
xgb_reg = xgb.XGBRegressor(
    n_estimators=100,
    max_depth=5,
    learning_rate=0.1
)
xgb_model = MultiOutputRegressor(xgb_reg)
xgb_model.fit(X_flat, y_flat)
joblib.dump(xgb_model, os.path.join(BASE_DIR, 'xgboost_model.pkl'))

# ============================================================
# 8: EVALUATION — MSE & MAE on full dataset
# ============================================================

print(f"\n{'='*50}")
print("EVALUATION (on training data)")
print(f"{'='*50}")

# --- LSTM evaluation ---
lstm_model.eval()
with torch.no_grad():
    lstm_preds = lstm_model(X_seq_t).numpy()
lstm_mse = mean_squared_error(y_seq, lstm_preds)
lstm_mae = mean_absolute_error(y_seq, lstm_preds)
print(f"LSTM    → MSE: {lstm_mse:.6f}, MAE: {lstm_mae:.6f}")

# --- GRU evaluation ---
gru_model.eval()
with torch.no_grad():
    gru_preds = gru_model(X_seq_t).numpy()
gru_mse = mean_squared_error(y_seq, gru_preds)
gru_mae = mean_absolute_error(y_seq, gru_preds)
print(f"GRU     → MSE: {gru_mse:.6f}, MAE: {gru_mae:.6f}")

# --- XGBoost evaluation ---
xgb_preds = xgb_model.predict(X_flat)
xgb_mse = mean_squared_error(y_flat, xgb_preds)
xgb_mae = mean_absolute_error(y_flat, xgb_preds)
print(f"XGBoost → MSE: {xgb_mse:.6f}, MAE: {xgb_mae:.6f}")

# ============================================================
# 9: COMPLETE
# ============================================================

print(f"\n{'='*50}")
print("SUCCESS: All models and scalers saved!")
print(f"{'='*50}")
print("Files generated:")
print("  - lstm_weights.pth")
print("  - gru_weights.pth")
print("  - xgboost_model.pkl")
print("  - scaler_y.pkl")
print("  - node_ids.pkl")
print("  - model_metadata.pkl")
print("\nRemoved (no longer needed):")
print("  - scaler_X.pkl (sin/cos features are self-normalized)")
