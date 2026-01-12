import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, mean_absolute_percentage_error
import tensorflow as tf
from tensorflow.keras import layers, Model
import pickle
import os

# Determine project root (works both locally and in Docker)
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(script_dir, '..', '..')  # Go up from scripts/stock_prediction to jupyter root
project_root = os.path.abspath(project_root)
os.chdir(project_root)

# Load stock data for TSLA
print("Downloading TSLA stock data...")
df = yf.download('TSLA', start='2018-01-01', end='2024-12-31')
data = df[['Close']].values

# Scale data
scaler = MinMaxScaler(feature_range=(0, 1))
data_scaled = scaler.fit_transform(data)

# Sequence creation
seq_len = 60
X, y = [], []
for i in range(seq_len, len(data_scaled)):
    X.append(data_scaled[i-seq_len:i])
    y.append(data_scaled[i])
X, y = np.array(X), np.array(y)

# Split into train and test sets (80/20)
train_size = int(len(X) * 0.8)
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

print(f"Training samples: {len(X_train)}, Test samples: {len(X_test)}")

# Transformer model with improved architecture
def create_transformer_model(seq_len):
    inputs = layers.Input(shape=(seq_len, 1))

    # Multi-head attention
    attention_output = layers.MultiHeadAttention(
        num_heads=4,
        key_dim=16,
        dropout=0.1
    )(inputs, inputs)

    # Add & Norm
    attention_output = layers.LayerNormalization(epsilon=1e-6)(attention_output + inputs)

    # Feed Forward Network
    ffn = layers.Dense(64, activation='relu')(attention_output)
    ffn = layers.Dropout(0.2)(ffn)
    ffn = layers.Dense(1)(ffn)

    # Add & Norm
    ffn_output = layers.LayerNormalization(epsilon=1e-6)(ffn + attention_output)

    # Global pooling
    pooled = layers.GlobalAveragePooling1D()(ffn_output)

    # Final dense layers
    dense = layers.Dense(32, activation='relu')(pooled)
    dense = layers.Dropout(0.2)(dense)
    outputs = layers.Dense(1)(dense)

    model = Model(inputs=inputs, outputs=outputs)
    return model

model = create_transformer_model(seq_len)
model.compile(optimizer='adam', loss='mse', metrics=['mae'])

print("\nTraining Transformer model...")
history = model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.1, verbose=1)

# Predict on test set
print("\nMaking predictions on test set...")
predicted_test = model.predict(X_test)
predicted_prices_test = scaler.inverse_transform(predicted_test)
actual_prices_test = scaler.inverse_transform(y_test)

# Calculate metrics
rmse = np.sqrt(mean_squared_error(actual_prices_test, predicted_prices_test))
mae = mean_absolute_error(actual_prices_test, predicted_prices_test)
mape = mean_absolute_percentage_error(actual_prices_test, predicted_prices_test) * 100

print("\n=== Transformer Model Performance Metrics ===")
print(f"RMSE: ${rmse:.2f}")
print(f"MAE: ${mae:.2f}")
print(f"MAPE: {mape:.2f}%")

# Save model and scaler
os.makedirs('models', exist_ok=True)
model.save('models/transformer_tsla_model.h5')
with open('models/transformer_scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)

# Save metrics
metrics = {
    'model': 'Transformer',
    'rmse': float(rmse),
    'mae': float(mae),
    'mape': float(mape)
}
with open('models/transformer_metrics.pkl', 'wb') as f:
    pickle.dump(metrics, f)

print("\nModel saved to models/transformer_tsla_model.h5")

# Plot comparison
plt.figure(figsize=(14, 6))

# Plot full data
plt.subplot(1, 2, 1)
predicted_train = model.predict(X_train)
predicted_prices_train = scaler.inverse_transform(predicted_train)
actual_prices_train = scaler.inverse_transform(y_train)

train_dates = df.index[seq_len:seq_len+len(actual_prices_train)]
test_dates = df.index[seq_len+len(actual_prices_train):seq_len+len(actual_prices_train)+len(actual_prices_test)]

plt.plot(train_dates, actual_prices_train, label="Train Actual", color='blue', alpha=0.6)
plt.plot(test_dates, actual_prices_test, label="Test Actual", color='green', linewidth=2)
plt.plot(test_dates, predicted_prices_test, label="Test Predicted", color='red', linestyle='--', linewidth=2)
plt.title("TSLA Stock Price: Transformer Model")
plt.xlabel("Date")
plt.ylabel("Price (USD)")
plt.legend()
plt.grid(True, alpha=0.3)

# Plot test set only (zoomed)
plt.subplot(1, 2, 2)
plt.plot(test_dates, actual_prices_test, label="Actual Price", color='green', linewidth=2)
plt.plot(test_dates, predicted_prices_test, label="Predicted Price", color='red', linestyle='--', linewidth=2)
plt.title(f"Transformer Test Set Predictions\nRMSE: ${rmse:.2f}, MAE: ${mae:.2f}, MAPE: {mape:.2f}%")
plt.xlabel("Date")
plt.ylabel("Price (USD)")
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('models/transformer_prediction.png', dpi=100, bbox_inches='tight')
print("Plot saved to models/transformer_prediction.png")
plt.show()
