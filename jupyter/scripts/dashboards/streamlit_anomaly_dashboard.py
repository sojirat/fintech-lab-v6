import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import plotly.express as px

st.title("🚨 Fraud Detection with Anomaly Detection")

# Simulated data
data = pd.DataFrame({
    'amount': np.random.normal(100, 20, 200).tolist() + [1000, 1200, 1500],
    'time_diff': np.random.normal(60, 15, 200).tolist() + [5, 10, 2]
})

model = IsolationForest(contamination=0.01)
data['anomaly'] = model.fit_predict(data)
data['anomaly'] = data['anomaly'].map({1: 'Normal', -1: 'Anomaly'})

fig = px.scatter(data, x='amount', y='time_diff', color='anomaly', title="Transaction Clusters")

st.plotly_chart(fig)
st.write("Anomalous Transactions:")
st.dataframe(data[data['anomaly'] == 'Anomaly'])