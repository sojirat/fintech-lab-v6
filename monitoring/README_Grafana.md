# Grafana Dashboard Setup

## Quick Start

1. **Access Grafana**
   - URL: http://localhost:3000
   - Username: `admin`
   - Password: `fintech2025`

2. **Import Dashboard**
   ```bash
   # The dashboard configuration is in grafana_dashboard.json
   # Import it via Grafana UI:
   # Dashboards → Import → Upload JSON file
   ```

## Available Dashboards

### 1. FinTech Lab - Transaction Monitoring

**Panels:**
- **Fraud Detection Rate** - Real-time fraud detection metrics
- **Bitcoin Price Predictions** - TimeGPT/Prophet predictions
- **API Response Time** - FastAPI performance
- **Total Transactions** - Transaction count
- **Anomaly Detection** - Live anomaly alerts

## Data Sources

### Add Prometheus Data Source

1. Go to Configuration → Data Sources
2. Click "Add data source"
3. Select "Prometheus"
4. Configure:
   - URL: `http://prometheus:9090`
   - Access: Server (default)
5. Click "Save & Test"

## Sample Queries

### Fraud Detection Metrics
```promql
# Fraud rate over time
rate(fraud_detection_total[5m])

# Anomaly count
sum(anomaly_detected_total)

# False positive rate
rate(false_positive_total[5m]) / rate(fraud_detection_total[5m])
```

### API Performance
```promql
# Average response time
avg(http_request_duration_seconds)

# Request rate
rate(http_requests_total[1m])

# Error rate
rate(http_requests_total{status=~"5.."}[5m])
```

### Bitcoin Predictions
```promql
# Predicted price (custom metric)
bitcoin_predicted_price

# Actual vs Predicted
bitcoin_actual_price vs bitcoin_predicted_price

# Prediction accuracy
abs(bitcoin_actual_price - bitcoin_predicted_price) / bitcoin_actual_price
```

## Custom Metrics Setup

To send custom metrics to Prometheus, add to FastAPI:

```python
from prometheus_client import Counter, Histogram, generate_latest

# Define metrics
fraud_counter = Counter('fraud_detection_total', 'Total fraud detections')
prediction_histogram = Histogram('prediction_duration_seconds', 'Prediction duration')

# In your endpoint
@app.post("/predict/")
def predict(transaction: Transaction):
    with prediction_histogram.time():
        result = model.predict(...)
        if result == "Anomaly":
            fraud_counter.inc()
    return {"prediction": result}

# Metrics endpoint
@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")
```

## Dashboard Features

### Alerts
Set up alerts for:
- High fraud rate (> 10%)
- API errors (> 5%)
- Slow response time (> 1s)
- Bitcoin price drops (> 5%)

### Variables
Use dashboard variables for:
- Time range selection
- Prediction model (Prophet/TimeGPT)
- Transaction type filter

## Tips

- 📊 Refresh interval: 5s for real-time monitoring
- 🔔 Configure Slack/Email notifications
- 📈 Create separate dashboards for different use cases
- 💾 Export dashboards for backup

## Troubleshooting

**Dashboard not showing data?**
- Check Prometheus is running: `docker ps | grep prometheus`
- Verify data source connection
- Check metric names match

**Graphs are empty?**
- Ensure services are sending metrics
- Check time range (last 1 hour)
- Verify query syntax
