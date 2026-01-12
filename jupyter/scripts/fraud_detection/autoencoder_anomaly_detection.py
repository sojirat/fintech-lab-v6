import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense

# Simulate normal transaction data
normal_data = np.random.normal(100, 20, (200, 2))
anomalies = np.array([[1000, 5], [1200, 10], [1500, 2]])
data = np.vstack([normal_data, anomalies])
scaler = MinMaxScaler()
data_scaled = scaler.fit_transform(data)

# Define autoencoder
input_layer = Input(shape=(2,))
encoded = Dense(8, activation='relu')(input_layer)
encoded = Dense(4, activation='relu')(encoded)
decoded = Dense(8, activation='relu')(encoded)
decoded = Dense(2, activation='sigmoid')(decoded)
autoencoder = Model(input_layer, decoded)

autoencoder.compile(optimizer='adam', loss='mse')
autoencoder.fit(data_scaled, data_scaled, epochs=50, batch_size=16, verbose=0)

# Reconstruction errors
reconstructions = autoencoder.predict(data_scaled)
mse = np.mean(np.power(data_scaled - reconstructions, 2), axis=1)
threshold = np.percentile(mse, 95)
anomalies = mse > threshold

# Show results
df = pd.DataFrame(data, columns=["amount", "time_diff"])
df["mse"] = mse
df["anomaly"] = anomalies
print(df[df["anomaly"] == True])