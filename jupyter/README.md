# Jupyter Workspace

โครงสร้างโฟลเดอร์ที่จัดระเบียบสำหรับ Data Science และ ML Projects

## 📁 โครงสร้างโฟลเดอร์

```
jupyter/
├── models/                              # ML Models (trained models, scalers, metrics)
│   ├── lstm_tsla_model.h5
│   ├── gru_tsla_model.h5
│   ├── transformer_tsla_model.h5
│   └── *.pkl, *.png
│
├── scripts/                             # Python Scripts
│   ├── stock_prediction/               # TSLA Stock Prediction Scripts
│   │   ├── lstm_stock_prediction.py
│   │   ├── gru_stock_prediction.py
│   │   ├── transformer_stock_prediction.py
│   │   └── compare_models.py
│   ├── fraud_detection/                # Fraud Detection Scripts
│   │   ├── fraud_detection.py
│   │   └── autoencoder_anomaly_detection.py
│   ├── crypto_analysis/                # Bitcoin Analysis (future)
│   └── dashboards/                     # Streamlit Dashboards
│       ├── streamlit_stock_dashboard.py
│       └── streamlit_anomaly_dashboard.py
│
├── notebooks/                           # Jupyter Notebooks
│   ├── stock_prediction.ipynb
│   ├── fraud_detection.ipynb
│   ├── bitcoin_prophet.ipynb
│   └── example-notebook.ipynb
│
├── data/                               # Data Files
│   ├── bitcoin_history.csv
│   ├── bitcoin_predictions.csv
│   └── COMPARISON_Prophet_vs_TimeGPT.md
│
├── blockchain/                         # Smart Contracts
│   └── test_smart_contract.js
│
└── README.md                           # This file
```

## 🚀 Quick Start

### Step 1: Install Dependencies (First Time Only)

```bash
cd /home/jovyan/work
bash install_dependencies.sh
```

This installs:
- TensorFlow 2.15.0
- scikit-learn
- yfinance
- pandas, numpy, matplotlib

### Step 2: Train TSLA Stock Prediction Models

```bash
# Method 1: Train all models at once (recommended)
bash train_all_models.sh

# Method 2: Train individually
python scripts/stock_prediction/lstm_stock_prediction.py
python scripts/stock_prediction/gru_stock_prediction.py
python scripts/stock_prediction/transformer_stock_prediction.py

# Compare results
python scripts/stock_prediction/compare_models.py
```

### Run Fraud Detection

```bash
python scripts/fraud_detection/fraud_detection.py
```

### Launch Streamlit Dashboards

```bash
# Stock Dashboard
streamlit run scripts/dashboards/streamlit_stock_dashboard.py

# Anomaly Dashboard
streamlit run scripts/dashboards/streamlit_anomaly_dashboard.py
```

## 📊 Models Directory

โมเดลที่ train แล้วจะถูกบันทึกใน `models/`:
- `*_model.h5` - Trained Keras models
- `*_scaler.pkl` - MinMaxScaler objects
- `*_metrics.pkl` - Model performance metrics
- `*_prediction.png` - Prediction plots
- `model_comparison.png` - Model comparison chart

## 🔧 Development

### Adding New Scripts

1. สร้างโฟลเดอร์ย่อยใน `scripts/` สำหรับโปรเจคใหม่
2. เพิ่ม `__init__.py` ถ้าต้องการทำ Python package
3. ใช้ relative paths จาก `/home/jovyan/work`

### Working with Notebooks

Notebooks ทั้งหมดอยู่ใน `notebooks/` folder
- เปิดผ่าน JupyterLab UI
- สามารถ import scripts จาก `scripts/` ได้

## 📝 Notes

- ไฟล์โมเดลขนาดใหญ่ (`.h5`, `.pkl`) จะไม่ถูก commit ลง git
- Data files ควรเก็บใน `data/` folder
- ใช้ `os.chdir('/home/jovyan/work')` ใน scripts เพื่อให้พาธถูกต้อง
