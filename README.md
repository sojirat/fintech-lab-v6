# Fintech Lab v6 - Multi-Company Stock Prediction 🚀

ระบบ Machine Learning แบบครบวงจรสำหรับทำนายราคาหุ้นหลายบริษัท พร้อม Airflow automation, JupyterLab UI, และ Future Prediction

[![Python](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.15-orange.svg)](https://www.tensorflow.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)

---

## ⚡ Quick Start (คำสั่งเดียวจบ!)

### 🆕 ครั้งแรก หรือไม่มีปัญหา
```bash
make all
```

### 🔄 มี Docker เก่าอยู่ หรือเจอ error
```bash
make fresh-start
```

### 🌐 มีปัญหา Network / EOF Error
```bash
make network-fix
```

เท่านี้ก็พร้อมใช้งานได้เลย! 🎉

---

## 📚 สารบัญ

- [🎯 เทรนโมเดล 4 วิธี](#-เทรนโมเดล-4-วิธี)
  - [วิธีที่ 1: Command Line (CLI)](#วิธีที่-1-command-line-cli---เร็ว-แม่นยำ)
  - [วิธีที่ 2: JupyterLab Notebook](#วิธีที่-2-jupyterlab-notebook-ui---ง่าย-ดูผลทันที)
  - [วิธีที่ 3: Airflow Schedule](#วิธีที่-3-airflow-automation---schedule-อัตโนมัติ)
  - [วิธีที่ 4: Python Script](#วิธีที่-4-python-script-โดยตรง---ยืดหยุ่นสูง)
- [🔮 พยากรณ์ราคาในอนาคต](#-พยากรณราคาในอนาคต)
- [📊 เปรียบเทียบโมเดล](#-เปรยบเทยบโมเดล)
- [📈 ดูผลลัพธ์](#-ดผลลพธ)
- [🌐 Service URLs](#-service-urls)
- [✨ Features](#-features)
- [📁 File Structure](#-file-structure)
- [🚨 Troubleshooting](#-troubleshooting)

---

## 🎯 เทรนโมเดล 4 วิธี

### วิธีที่ 1: Command Line (CLI) - เร็ว แม่นยำ

**เทรนบริษัทเดียว (ทั้ง 3 โมเดล: LSTM, GRU, Transformer):**
```bash
make train-tsla     # Tesla
make train-aapl     # Apple
make train-googl    # Google
make train-nvda     # NVIDIA
make train-msft     # Microsoft
```

**เทรนหลายบริษัทพร้อมกัน:**
```bash
make train-tech              # 🚀 Tech Giants (TSLA, AAPL, GOOGL, MSFT, NVDA)
make train-semiconductor     # 💾 Semiconductors (NVDA, AMD, INTC, TSM)
make train-faang             # 📱 FAANG (META, AAPL, AMZN, NFLX, GOOGL)
make train-all-default       # 🌟 All Default (TSLA, AAPL, GOOGL, MSFT, AMZN)
```

**เทรนเฉพาะโมเดล (สำหรับ TSLA):**
```bash
make train-lstm-only         # เฉพาะ LSTM
make train-gru-only          # เฉพาะ GRU
make train-transformer-only  # เฉพาะ Transformer
```

**ทดสอบเร็ว (แนะนำเริ่มต้น!):**
```bash
make train-test-quick        # AAPL, LSTM, 2023-2024 (ใช้เวลาแค่ไม่กี่นาที!)
make train-test-recent       # TSLA, ALL, 2023-2024
```

**💡 ข้อดี:**
- ⚡ เร็วที่สุด - รันคำสั่งเดียวจบ
- 🎯 แม่นยำ - ควบคุมได้ทุกอย่าง
- 📋 ง่าย - จำแค่ `make train-{ticker}`

---

### วิธีที่ 2: JupyterLab Notebook (UI) - ง่าย ดูผลทันที

**เปิด Training Notebook:**
```bash
make open-jupyter            # เปิด browser อัตโนมัติ
```

หรือเปิดเอง:
```
URL:   http://localhost:8888
Token: fintech2025
File:  notebooks/train_stocks_ui.ipynb
```

**Features:**
- ✅ **Interactive Widgets** - ปรับค่าได้ง่าย
- ✅ **Real-time Progress** - เห็นความคืบหน้าทันที
- ✅ **View Results** - ดู plots และ metrics ทันที
- ✅ **Auto Retry** - จัดการ rate limit อัตโนมัติ
- ✅ **Multiple Companies** - เทรนหลายบริษัทในคลิกเดียว

**ตัวอย่างการใช้งาน:**
1. เปิด notebook: `train_stocks_ui.ipynb`
2. แก้ไข Configuration Cell:
   ```python
   TICKER = 'AAPL'          # หรือ 'TSLA', 'GOOGL', etc.
   MODEL_TYPE = 'ALL'       # หรือ 'LSTM', 'GRU', 'TRANSFORMER'
   START_DATE = '2018-01-01'
   END_DATE = None          # None = วันล่าสุด
   EPOCHS = 50
   BATCH_SIZE = 32
   ```
3. รัน Cell "Train Single Company"
4. ดูผลใน Cell "View Results"

**💡 ข้อดี:**
- 🎨 UI สวยงาม - เห็นภาพชัดเจน
- 🔄 Real-time - เห็นผลทันที
- 📊 Visualization - กราฟในหน้าเดียว
- 👥 เหมาะกับ - Data Scientists, Analysts

**อ่านเพิ่ม:** [TRAINING_GUIDE.md](TRAINING_GUIDE.md)

---

### วิธีที่ 3: Airflow Automation - Schedule อัตโนมัติ

**เปิด Airflow Web UI:**
```bash
open http://localhost:8083
# Login: admin / fintech2025
```

**Trigger DAG ด้วย Command:**
```bash
make airflow-trigger         # Trigger: multi_company_stock_training
make airflow-list            # ดู DAGs ทั้งหมด
make airflow-status          # ดูสถานะการรัน
make airflow-logs            # ดู logs
```

**DAG Features:**
- 🔄 **Auto Schedule** - รันทุกวันเวลา 6:00 AM
- 📅 **On-Demand** - Trigger ได้ตามต้องการ
- 🎯 **Multi-Company** - เทรนหลายบริษัทพร้อมกัน
- 🔔 **Monitoring** - ติดตามผ่าน Web UI

**💡 ข้อดี:**
- ⏰ Schedule - รันอัตโนมัติทุกวัน
- 📊 Monitoring - เห็นสถานะแต่ละ Task
- 🔁 Retry - Retry อัตโนมัติเมื่อล้มเหลว
- 🏭 เหมาะกับ - Production Environment

---

### วิธีที่ 4: Python Script โดยตรง - ยืดหยุ่นสูง

**รันใน Docker Container:**
```bash
make shell-jupyter           # เข้า container

# แล้วรัน:
python scripts/stock_prediction/train_multi_company.py \
    --ticker TSLA \
    --model ALL \
    --start-date 2018-01-01 \
    --end-date 2024-12-31 \
    --epochs 50 \
    --batch-size 32
```

**Parameters:**
- `--ticker`: รหัสหุ้น (TSLA, AAPL, etc.)
- `--model`: โมเดล (LSTM / GRU / TRANSFORMER / ALL)
- `--start-date`: วันเริ่มต้น (YYYY-MM-DD)
- `--end-date`: วันสิ้นสุด (ไม่ใส่ = วันล่าสุด)
- `--epochs`: จำนวน epochs (default: 50)
- `--batch-size`: Batch size (default: 32)

**💡 ข้อดี:**
- 🔧 ยืดหยุ่นสูง - ปรับค่าได้ทุกอย่าง
- 🎯 ควบคุมเต็มที่ - รันแบบ custom ได้
- 🐍 Python Native - เรียกจาก script อื่นได้
- 🧪 เหมาะกับ - Development, Testing

---

## 🔮 พยากรณ์ราคาในอนาคต

### ใช้โมเดลที่เทรนแล้วพยากรณ์ราคาในอนาคต

**คำสั่งพยากรณ์แบบง่าย (ใช้โมเดล GRU):**

```bash
# พยากรณ์ 30 วัน
make predict-day TICKER=AAPL
make predict-aapl-day
make predict-tsla-day

# พยากรณ์ 4 สัปดาห์
make predict-week TICKER=AAPL
make predict-aapl-week
make predict-tsla-week

# พยากรณ์ 3 เดือน
make predict-month TICKER=AAPL
make predict-aapl-month
make predict-tsla-month

# พยากรณ์ 1 ปี
make predict-year TICKER=AAPL
make predict-aapl-year
```

**คำสั่งพยากรณ์แบบกำหนดเอง (เลือกโมเดลได้):**

```bash
# ใช้โมเดล LSTM
make predict-custom TICKER=AAPL MODEL=LSTM PERIODS=30 TYPE=day

# ใช้โมเดล GRU (ดีที่สุด)
make predict-custom TICKER=AAPL MODEL=GRU PERIODS=3 TYPE=month

# ใช้โมเดล Transformer
make predict-custom TICKER=TSLA MODEL=TRANSFORMER PERIODS=60 TYPE=day
```

**ตัวเลือกโมเดล:**
- `LSTM` - มาตรฐาน, RMSE สูงกว่า GRU เล็กน้อย
- `GRU` - ⭐ **แนะนำ** - ดีที่สุด (RMSE ต่ำสุด, MAPE 3.42%)
- `TRANSFORMER` - ต้องการข้อมูลมาก, RMSE สูง

**ตัวเลือกช่วงเวลา (TYPE):**
- `day` - รายวัน (1 day)
- `week` - รายสัปดาห์ (7 days)
- `month` - รายเดือน (30 days)
- `year` - รายปี (365 days)

**ผลลัพธ์ที่ได้:**
- 📊 ราคาพยากรณ์ทุกวัน
- 📈 เปอร์เซ็นต์เปลี่ยนแปลง
- 🎯 แนวโน้ม (Bullish/Bearish)
- 📉 กราฟเปรียบเทียบราคาจริงและพยากรณ์
- ⚠️ Disclaimer พร้อม accuracy metrics

**ตัวอย่างผลลัพธ์:**
```
Current Price:    $259.37
Predicted (30d):  $181.87
Change:           -$77.50 (-29.88%)
Trend:            🔴 BEARISH (Downward)

Model Accuracy:
  RMSE: $6.73
  MAE:  $6.54
  MAPE: 3.42%
```

**💡 เคล็ดลับ:**
- ใช้โมเดล **GRU** สำหรับความแม่นยำสูงสุด
- พยากรณ์ระยะสั้น (30-60 วัน) แม่นยำกว่าระยะยาว
- ดู accuracy metrics (RMSE, MAPE) เพื่อประเมินความน่าเชื่อถือ
- ⚠️ ไม่ใช่คำแนะนำการลงทุน - ใช้เพื่อศึกษาเท่านั้น!

---

## 📊 เปรียบเทียบโมเดล

### เปรียบเทียบ LSTM vs GRU vs Transformer

**เปรียบเทียบทุกบริษัท:**
```bash
make compare-all             # เปรียบเทียบทุก ticker
```

**เปรียบเทียบเฉพาะบริษัท:**
```bash
make compare-aapl            # เฉพาะ AAPL
make compare-tsla            # เฉพาะ TSLA
```

**ผลลัพธ์ที่ได้:**
- 📊 ตารางเปรียบเทียบ RMSE, MAE, MAPE
- 🏆 อันดับโมเดลที่ดีที่สุด
- 💡 คำแนะนำโมเดลที่เหมาะสม
- 📈 กราฟเปรียบเทียบ (บันทึกใน models/{TICKER}/)

**ตัวอย่างผลลัพธ์:**
```
🏆 RANKINGS:
Best RMSE:  GRU ($6.73)
Best MAE:   GRU ($6.54)
Best MAPE:  GRU (3.42%)

📈 OVERALL RANKING:
1. GRU         ⭐⭐⭐
2. LSTM        ⭐⭐
3. TRANSFORMER ⭐

💡 RECOMMENDATION:
   Use GRU model for AAPL
```

---

## 📈 ดูผลลัพธ์

```bash
# ดู metrics ของแต่ละบริษัท
make view-tsla               # TSLA metrics

# ดูโมเดลทั้งหมด
make models-list             # โมเดล .h5 ทั้งหมด
make models-list-all         # ไฟล์ทั้งหมด (.h5, .pkl, .png)
make models-size             # ขนาดโมเดล

# เปรียบเทียบโมเดล
make compare-all             # เปรียบเทียบทุกโมเดล
make compare-aapl            # เปรียบเทียบ AAPL
make compare-tsla            # เปรียบเทียบ TSLA

# ดู plots (macOS)
make view-plots              # เปิดกราฟทั้งหมด
```

**โครงสร้างไฟล์ผลลัพธ์:**
```
models/
├── AAPL/
│   ├── lstm_aapl_model.h5           # โมเดล LSTM
│   ├── lstm_aapl_scaler.pkl         # Scaler
│   ├── lstm_aapl_metrics.pkl        # Metrics
│   ├── lstm_aapl_prediction.png     # กราฟ prediction
│   ├── gru_aapl_model.h5            # โมเดล GRU (ดีที่สุด)
│   ├── gru_aapl_future_prediction.png  # กราฟพยากรณ์อนาคต
│   └── comparison_aapl.png          # กราฟเปรียบเทียบ
└── TSLA/
    └── ...
```

---

## 🌐 Service URLs

```bash
make urls                    # แสดง URLs ทั้งหมด
make check                   # ตรวจสอบสถานะ
```

| Service | URL | Credentials | Description |
|---------|-----|-------------|-------------|
| **JupyterLab** | http://localhost:8888 | Token: `fintech2025` | Training Notebook UI |
| **Airflow** | http://localhost:8083 | admin / fintech2025 | Workflow Automation |
| **FastAPI** | http://localhost:8000/docs | - | API Documentation |
| **Grafana** | http://localhost:3000 | admin / fintech2025 | Monitoring Dashboard |
| **Prometheus** | http://localhost:9090 | - | Metrics Collection |

---

## ✨ Features

### 🎯 Training Features
- ✅ **Multi-Company** - เทรนได้หลายบริษัทพร้อมกัน
- ✅ **3 Models** - LSTM, GRU, Transformer
- ✅ **Flexible Dates** - กำหนด start/end ได้ (ไม่ใส่ end = ใช้วันล่าสุด)
- ✅ **Auto Retry** - จัดการ Yahoo Finance rate limit
- ✅ **yahooquery** - ใช้ yahooquery เป็นหลัก (ไม่ติด rate limit)
- ✅ **Fallback** - ถ้า yahooquery ไม่ได้ จะใช้ yfinance

### 🔮 Prediction Features
- ✅ **Future Prediction** - พยากรณ์ day, week, month, year
- ✅ **Model Selection** - เลือกใช้ LSTM, GRU, หรือ Transformer
- ✅ **Rolling Window** - ใช้ 60 วันล่าสุดในการพยากรณ์
- ✅ **Trend Analysis** - แสดงแนวโน้ม Bullish/Bearish
- ✅ **Visualization** - กราฟเปรียบเทียบราคาจริงและพยากรณ์

### 📊 Comparison Features
- ✅ **Model Comparison** - เปรียบเทียบ LSTM vs GRU vs Transformer
- ✅ **Ranking System** - จัดอันดับตาม RMSE, MAE, MAPE
- ✅ **Recommendation** - แนะนำโมเดลที่ดีที่สุด
- ✅ **Visualization** - กราฟแท่งเปรียบเทียบ

### 🚀 Infrastructure Features
- ✅ **Airflow Automation** - Schedule และ on-demand
- ✅ **JupyterLab UI** - Interactive training notebook
- ✅ **Makefile Commands** - 50+ คำสั่งใช้งานง่าย
- ✅ **Relative Paths** - รันได้ทั้ง Docker และ Local
- ✅ **Lightweight FastAPI** - ไม่มี ML dependencies

---

## 📁 File Structure

```
fintech-lab-v6/
├── Makefile                              # 50+ คำสั่ง make
├── train_stock.sh                        # Helper script สำหรับ CLI
├── docker-compose.yml                    # Docker services config
│
├── jupyter/                              # JupyterLab service
│   ├── Dockerfile                        # Custom image (TensorFlow 2.15)
│   ├── notebooks/
│   │   └── train_stocks_ui.ipynb        # 🎨 Training UI Notebook
│   ├── models/                           # โมเดลที่เทรนแล้ว
│   │   ├── AAPL/
│   │   │   ├── lstm_aapl_model.h5
│   │   │   ├── gru_aapl_model.h5        # ⭐ ดีที่สุด
│   │   │   ├── transformer_aapl_model.h5
│   │   │   ├── *_scaler.pkl
│   │   │   ├── *_metrics.pkl
│   │   │   ├── *_prediction.png
│   │   │   ├── gru_aapl_future_prediction.png
│   │   │   └── comparison_aapl.png
│   │   ├── TSLA/
│   │   └── ...
│   └── scripts/
│       └── stock_prediction/
│           ├── train_multi_company.py    # 🎯 สคริปต์เทรนหลัก
│           ├── compare_all_models.py     # 📊 เปรียบเทียบโมเดล
│           ├── predict_future.py         # 🔮 พยากรณ์อนาคต
│           ├── lstm_stock_prediction.py
│           ├── gru_stock_prediction.py
│           └── transformer_stock_prediction.py
│
├── airflow/                              # Airflow service
│   ├── Dockerfile
│   └── dags/
│       └── multi_company_stock_training_dag.py
│
├── backend/                              # FastAPI service
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt                  # Lightweight (ไม่มี TensorFlow)
│
└── docs/                                 # เอกสารประกอบ
    ├── TRAINING_GUIDE.md                 # 📚 คู่มือเทรนแบบละเอียด
    ├── MAKEFILE_GUIDE.md
    ├── SUMMARY.md
    └── ...
```

---

## 🎓 Workflows

### 🆕 ครั้งแรก (First Time Setup)
```bash
make workflow-first-time
# หรือ
make all && make train-test-quick
```

**ทำอะไรบ้าง:**
1. Build Docker images
2. Start all services
3. Wait 30 seconds
4. Check status
5. Run quick test training

---

### 📅 ใช้ทุกวัน (Daily Workflow)
```bash
make workflow-daily
```

**ทำอะไรบ้าง:**
1. Start services (ถ้ายังไม่ได้เปิด)
2. Train TSLA models
3. View results

หรือเลือกเอง:
```bash
make up
make train-aapl
make compare-aapl
make predict-aapl-day
make view-tsla
```

---

### 📊 ใช้ทุกสัปดาห์ (Weekly Workflow)
```bash
make workflow-weekly
```

**ทำอะไรบ้าง:**
1. Train tech stocks (TSLA, AAPL, GOOGL, MSFT, NVDA)
2. Backup models

---

### 🔮 พยากรณ์และวิเคราะห์
```bash
# 1. เทรนโมเดล
make train-aapl

# 2. เปรียบเทียบโมเดล
make compare-aapl

# 3. พยากรณ์ด้วยโมเดลที่ดีที่สุด
make predict-aapl-month

# 4. ลองโมเดลอื่น
make predict-custom TICKER=AAPL MODEL=LSTM PERIODS=30 TYPE=day
```

---

## 🔧 จัดการระบบ

### เปิด/ปิด Services
```bash
make up              # ⬆️  เปิดทุก services
make down            # ⬇️  ปิดทุก services
make restart         # 🔄 Restart
make ps              # 📋 ดูสถานะ containers
```

### Build & Rebuild
```bash
make build           # 🔨 Build (no cache)
make build-fast      # ⚡ Build (with cache)
make force-rebuild   # 🔨 Force rebuild with retry
make network-fix     # 🌐 Pull base image first, then build
```

### ดู Logs
```bash
make logs            # 📜 ทุก services
make logs-jupyter    # 📜 JupyterLab only
make logs-airflow    # 📜 Airflow only
make logs-fastapi    # 📜 FastAPI only
```

### Shell Access
```bash
make shell-jupyter   # 🐚 เข้า JupyterLab container
make shell-airflow   # 🐚 เข้า Airflow container
make shell-fastapi   # 🐚 เข้า FastAPI container
```

### Management
```bash
make models-backup   # 💾 Backup โมเดลไป models_backup/
make models-clean    # 🗑️  ลบโมเดลทั้งหมด (ระวัง!)
make clean           # 🧹 ลบ Python cache
make clean-docker    # 🐳 ลบ Docker containers & volumes
make clean-all       # 🧹 ลบทุกอย่าง
make reset           # 🔄 Reset ระบบทั้งหมด
```

---

## 🚨 Troubleshooting

### ❌ EOF Error เมื่อ Build
```bash
# วิธีแก้ที่ 1: Fresh start
make fresh-start

# วิธีแก้ที่ 2: Network fix
make network-fix

# วิธีแก้ที่ 3: Pull base image ก่อน
make pull-base-image
make build-fast
make up
```

---

### ❌ Yahoo Finance Rate Limit (429 Error)
```bash
# ไม่ต้องกังวล! ระบบจัดการให้อัตโนมัติแล้ว
# - ใช้ yahooquery เป็นหลัก (ไม่ติด rate limit)
# - Fallback ไป yfinance ถ้าจำเป็น
# - Retry อัตโนมัติ 5 ครั้ง (5s, 10s, 20s, 40s, 80s)

# ถ้ายังเจอ ให้รอ 5-10 นาที แล้วลองใหม่
make train-test-quick
```

**อ่านเพิ่ม:** [TRAINING_GUIDE.md](TRAINING_GUIDE.md) - หัวข้อ "Rate Limiting"

---

### ❌ Container ไม่ทำงาน
```bash
# ตรวจสอบสถานะ
make ps

# ดู logs
make logs-jupyter

# Restart
make restart

# หรือ rebuild
make down
make build-fast
make up
make wait
```

---

### ❌ เทรนล้มเหลว
```bash
# 1. ตรวจสอบ syntax
make check-syntax

# 2. ทดสอบ yfinance
make test-yfinance

# 3. ทดสอบ paths
make test-paths

# 4. เข้า container ตรวจสอบ
make shell-jupyter
python scripts/stock_prediction/train_multi_company.py --help
```

---

### ❌ โมเดลไม่เจอ
```bash
# ดูโมเดลที่มี
make models-list
make models-list-all

# ตรวจสอบไฟล์
ls -la jupyter/models/AAPL/

# ถ้าไม่มี ให้เทรนใหม่
make train-aapl
```

---

### ❌ พยากรณ์ล้มเหลว
```bash
# เช็คว่าโมเดลถูกเทรนแล้ว
make models-list

# ถ้ายังไม่ได้เทรน
make train-aapl

# แล้วลองพยากรณ์ใหม่
make predict-aapl-day
```

---

## 💡 Tips & Best Practices

### 1. 🚀 เริ่มต้นด้วย Quick Test
```bash
make train-test-quick        # ใช้เวลาแค่ไม่กี่นาที
```

### 2. 📊 เปรียบเทียบโมเดลก่อนพยากรณ์
```bash
make train-aapl              # เทรนทั้ง 3 โมเดล
make compare-aapl            # เปรียบเทียบ
# ดูว่าโมเดลไหนดีที่สุด แล้วใช้โมเดลนั้นพยากรณ์
```

### 3. 💾 Backup ก่อนลบ
```bash
make models-backup           # Backup ก่อนเสมอ
make models-clean            # แล้วค่อยลบ
```

### 4. 📜 ดู Logs เมื่อมีปัญหา
```bash
make logs-jupyter            # ดู logs ละเอียด
make check                   # ตรวจสอบสถานะ
```

### 5. 🎯 ใช้ GRU สำหรับความแม่นยำสูงสุด
```bash
# GRU มี MAPE ต่ำที่สุด (3.42% vs LSTM 4.17%)
make predict-custom TICKER=AAPL MODEL=GRU PERIODS=30 TYPE=day
```

### 6. ⚠️ พยากรณ์ระยะสั้นแม่นยำกว่า
```bash
# แนะนำ: 30-60 วัน
make predict-aapl-day        # 30 วัน
make predict-aapl-week       # 4 สัปดาห์ (28 วัน)

# ระยะยาวมี uncertainty สูง
make predict-aapl-year       # 1 ปี (ใช้เพื่อดูแนวโน้ม)
```

---

## 📖 เอกสารเพิ่มเติม

| ไฟล์ | เนื้อหา | เมื่อไหร่ใช้ |
|------|---------|--------------|
| **[TRAINING_GUIDE.md](TRAINING_GUIDE.md)** | 📚 คู่มือเทรนแบบละเอียด | เทรนครั้งแรก, มีปัญหา |
| **[MAKEFILE_GUIDE.md](MAKEFILE_GUIDE.md)** | 📖 คู่มือ Makefile | ดูคำสั่งทั้งหมด |
| **[SUMMARY.md](SUMMARY.md)** | 📝 สรุปภาษาไทย | ภาพรวมทั้งระบบ |

**ดูคำสั่งทั้งหมด:**
```bash
make help                    # แสดงคำสั่งทั้งหมด 50+ คำสั่ง
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   HYBRID ARCHITECTURE                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. Training (เลือกได้ 4 วิธี)                                  │
│     ┌──────────┬──────────┬──────────┬──────────┐           │
│     │   CLI    │    UI    │ Airflow  │  Python  │           │
│     │ (Make)   │(Notebook)│(Schedule)│ (Script) │           │
│     └─────┬────┴─────┬────┴─────┬────┴─────┬────┘           │
│           └──────────┼──────────┼──────────┘                │
│                      ▼          ▼                           │
│              train_multi_company.py                         │
│                      │                                      │
│                      ▼                                      │
│              yahooquery / yfinance                          │
│              (Auto retry, rate limit handling)              │
│                      │                                      │
│                      ▼                                      │
│              LSTM / GRU / Transformer                       │
│                      │                                      │
│                      ▼                                      │
│  2. Shared Volume: /jupyter/models/                         │
│     ├── AAPL/                                               │
│     │   ├── lstm_aapl_model.h5                              │
│     │   ├── gru_aapl_model.h5        ⭐ Best                │
│     │   ├── transformer_aapl_model.h5                       │
│     │   └── ...                                             │
│     └── TSLA/                                               │
│                      │                                      │
│                      ▼                                      │
│  3. Analysis & Prediction                                   │
│     ┌──────────┬──────────┐                                 │
│     │ Compare  │ Predict  │                                 │
│     │ Models   │ Future   │                                 │
│     └─────┬────┴─────┬────┘                                 │
│           └──────────┘                                      │
│                │                                            │
│                ▼                                            │
│  4. Serving (Future)                                        │
│     FastAPI (Lightweight, no ML deps)                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 Roadmap

### ✅ Completed
- [x] Multi-company training
- [x] 3 models (LSTM, GRU, Transformer)
- [x] Airflow automation
- [x] JupyterLab UI
- [x] Makefile commands (50+)
- [x] Rate limit handling
- [x] yahooquery integration
- [x] Model comparison
- [x] Future prediction

### 🚧 In Progress
- [ ] FastAPI prediction endpoints
- [ ] Real-time prediction API
- [ ] Model versioning

### 📋 Planned
- [ ] More technical indicators
- [ ] Ensemble models
- [ ] Backtesting framework
- [ ] Portfolio optimization
- [ ] Real-time streaming data

---

## ⚠️ Disclaimer

**โปรเจคนี้สร้างขึ้นเพื่อการศึกษาเท่านั้น**

- ❌ **ไม่ใช่คำแนะนำการลงทุน**
- ❌ ไม่รับประกันความแม่นยำของการพยากรณ์
- ❌ ใช้ยอมรับความเสี่ยงของตนเอง
- ✅ ใช้เพื่อเรียนรู้ Machine Learning และ Data Science

**การลงทุนมีความเสี่ยง ควรศึกษาข้อมูลก่อนตัดสินใจลงทุน**

---

## 📄 License

This project is for educational purposes only.

---

## 🎉 เริ่มต้นใช้งาน!

```bash
# คำสั่งเดียวจบ!
make all

# หรือแบบละเอียด
make workflow-first-time
```

**ขั้นตอนถัดไป:**

1. ✅ เทรนโมเดล: `make train-aapl`
2. ✅ เปรียบเทียบ: `make compare-aapl`
3. ✅ พยากรณ์: `make predict-aapl-month`
4. ✅ ดูผล: `make view-tsla`
5. ✅ เปิด UI: `make open-jupyter`

---

**Happy Trading! 📈💰**

Made with ❤️ for ducation and learning By Sojirat.S
