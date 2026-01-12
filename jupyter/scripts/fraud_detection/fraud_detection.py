import pandas as pd
from sklearn.ensemble import IsolationForest
import numpy as np

# Simulated transaction data
data = pd.DataFrame({
    'amount': np.random.normal(100, 20, 200).tolist() + [1000, 1200, 1500],
    'time_diff': np.random.normal(60, 15, 200).tolist() + [5, 10, 2]
})

# Train model
model = IsolationForest(contamination=0.01)
data['anomaly'] = model.fit_predict(data)
print(data.tail())