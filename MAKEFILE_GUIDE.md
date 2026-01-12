# 📖 Makefile Guide - คู่มือคำสั่ง Make ทั้งหมด

คู่มือฉบับสมบูรณ์สำหรับคำสั่ง Make ทั้งหมด 50+ คำสั่ง พร้อมตัวอย่างการใช้งาน

---

## 📑 สารบัญ

- [🎯 Quick Reference](#-quick-reference)
- [🚀 Quick Start Commands](#-quick-start-commands)
- [🐳 Docker Management](#-docker-management)
- [🎓 Training Commands](#-training-commands)
- [🔮 Prediction Commands](#-prediction-commands)
- [📊 Analysis Commands](#-analysis-commands)
- [🌐 Services & URLs](#-services--urls)
- [📁 Model Management](#-model-management)
- [🔧 Development & Testing](#-development--testing)
- [🧹 Cleanup Commands](#-cleanup-commands)
- [📚 Workflows](#-workflows)
- [💡 Tips & Tricks](#-tips--tricks)

---

## 🎯 Quick Reference

### ดูคำสั่งทั้งหมด

```bash
make help
```

แสดงคำสั่งทั้งหมดพร้อมคำอธิบาย

---

### คำสั่งที่ใช้บ่อยที่สุด (Top 10)

| คำสั่ง | คำอธิบาย | เวลา |
|--------|----------|------|
| `make help` | ดูคำสั่งทั้งหมด | - |
| `make all` | Setup ทั้งหมดในคำสั่งเดียว | 3-5 นาที |
| `make up` | เปิด services ทั้งหมด | 30 วินาที |
| `make down` | ปิด services ทั้งหมด | 10 วินาที |
| `make train-aapl` | เทรนโมเดล AAPL | 30-60 นาที |
| `make compare-aapl` | เปรียบเทียบโมเดล AAPL | 1 วินาที |
| `make predict-aapl-day` | พยากรณ์ AAPL 30 วัน | 1-2 นาที |
| `make logs-jupyter` | ดู JupyterLab logs | - |
| `make models-list` | ดูโมเดลที่เทรนแล้ว | 1 วินาที |
| `make check` | ตรวจสอบสถานะ | 1 วินาที |

---

## 🚀 Quick Start Commands

### All-in-One Commands (แนะนำ!)

#### `make all`
```bash
make all
```
**ทำอะไรบ้าง:**
1. Stop old containers (`make down`)
2. Build images with cache (`make build-fast`)
3. Start services (`make up`)
4. Wait 30 seconds (`make wait`)
5. Check status (`make check`)

**เมื่อไหร่ใช้:**
- ครั้งแรก
- ไม่มีปัญหา
- อยากได้ทุกอย่างในคำสั่งเดียว

**ระยะเวลา:** 3-5 นาที

---

#### `make quick-start`
```bash
make quick-start
```
**คำอธิบาย:** Alias ของ `make all`

---

#### `make fresh-start`
```bash
make fresh-start
```
**ทำอะไรบ้าง:**
1. Clean Docker completely (`make clean-docker`)
2. Build with cache (`make build-fast`)
3. Start services
4. Wait and check

**เมื่อไหร่ใช้:**
- มี Docker เก่าอยู่
- เจอ error ที่แก้ไม่ได้
- ต้องการเริ่มใหม่หมด

**ระยะเวลา:** 4-6 นาที

---

#### `make fresh-start-full`
```bash
make fresh-start-full
```
**ทำอะไรบ้าง:** เหมือน `fresh-start` แต่ build without cache

**เมื่อไหร่ใช้:**
- มีปัญหาซ้ำๆ
- ต้องการ rebuild ทุกอย่างใหม่

**ระยะเวลา:** 10-15 นาที

---

#### `make network-fix`
```bash
make network-fix
```
**ทำอะไรบ้าง:**
1. Pull base image first (`make pull-base-image`)
2. Build with cache
3. Start and check

**เมื่อไหร่ใช้:**
- เจอ Network error
- เจอ EOF error
- Internet ช้า

**ระยะเวลา:** 5-10 นาที

---

## 🐳 Docker Management

### Build Commands

#### `make build`
```bash
make build
```
**คำอธิบาย:** Build Docker images (no cache)

**Options:**
- Retry 3 ครั้งถ้าล้มเหลว
- รอ 5 วินาทีระหว่าง retry

**ระยะเวลา:** 10-15 นาที

---

#### `make build-fast`
```bash
make build-fast
```
**คำอธิบาย:** Build with cache (เร็วกว่า)

**ระยะเวลา:** 2-5 นาที

---

#### `make build-offline`
```bash
make build-offline
```
**คำอธิบาย:** Build using cached base image (ไม่ pull)

**เมื่อไหร่ใช้:**
- ไม่มี internet
- มี base image อยู่แล้ว

---

#### `make force-rebuild`
```bash
make force-rebuild
```
**คำอธิบาย:** Force rebuild ทั้งหมด (no cache, pull)

**ระยะเวลา:** 15-20 นาที

---

#### `make pull-base-image`
```bash
make pull-base-image
```
**คำอธิบาย:** Pull base image manually (jupyter/scipy-notebook)

**Options:**
- Retry 5 ครั้ง
- รอ 10 วินาทีระหว่าง retry

---

### Service Management

#### `make up`
```bash
make up
```
**คำอธิบาย:** Start all services

**Services:**
- JupyterLab
- Airflow
- FastAPI
- PostgreSQL
- Redis
- Grafana
- Prometheus

---

#### `make down`
```bash
make down
```
**คำอธิบาย:** Stop all services

---

#### `make restart`
```bash
make restart
```
**คำอธิบาย:** Restart all services

**เท่ากับ:** `make down && make up`

---

#### `make ps`
```bash
make ps
```
**คำอธิบาย:** Show running containers

**ตัวอย่าง output:**
```
NAME                COMMAND             STATUS          PORTS
jupyterlab          "start-notebook"    Up 2 hours      0.0.0.0:8888->8888/tcp
airflow             "airflow webserver" Up 2 hours      0.0.0.0:8083->8080/tcp
fastapi             "uvicorn main:app"  Up 2 hours      0.0.0.0:8000->8000/tcp
```

---

### Logs

#### `make logs`
```bash
make logs
```
**คำอธิบาย:** Show logs (all services, follow mode)

**หยุด:** Ctrl+C

---

#### `make logs-jupyter`
```bash
make logs-jupyter
```
**คำอธิบาย:** Show JupyterLab logs only

---

#### `make logs-airflow`
```bash
make logs-airflow
```
**คำอธิบาย:** Show Airflow logs only

---

#### `make logs-fastapi`
```bash
make logs-fastapi
```
**คำอธิบาย:** Show FastAPI logs only

---

### Initialization & Checks

#### `make wait`
```bash
make wait
```
**คำอธิบาย:** Wait 30 seconds for services to initialize

---

#### `make check`
```bash
make check
```
**คำอธิบาย:** Check service status and show URLs

**ตัวอย่าง output:**
```
Service URLs:
  • JupyterLab:  http://localhost:8888  (Token: fintech2025)
  • Airflow:     http://localhost:8083  (admin/fintech2025)
  • FastAPI:     http://localhost:8000/docs
  • Grafana:     http://localhost:3000  (admin/fintech2025)
```

---

#### `make check-syntax`
```bash
make check-syntax
```
**คำอธิบาย:** Check Python syntax of all scripts

**ไฟล์ที่เช็ค:**
- train_multi_company.py
- lstm_stock_prediction.py
- gru_stock_prediction.py
- transformer_stock_prediction.py
- multi_company_stock_training_dag.py

---

## 🎓 Training Commands

### Single Company Training

#### `make train-tsla`
```bash
make train-tsla
```
**คำอธิบาย:** Train all models (LSTM, GRU, Transformer) for TSLA

**Parameters:**
- Ticker: TSLA
- Models: ALL
- Start Date: 2018-01-01
- End Date: Latest

**ระยะเวลา:** 30-60 นาที

**ผลลัพธ์:**
```
jupyter/models/TSLA/
├── lstm_tsla_model.h5
├── lstm_tsla_scaler.pkl
├── lstm_tsla_metrics.pkl
├── lstm_tsla_prediction.png
├── gru_tsla_model.h5
├── gru_tsla_scaler.pkl
├── gru_tsla_metrics.pkl
├── gru_tsla_prediction.png
├── transformer_tsla_model.h5
├── transformer_tsla_scaler.pkl
├── transformer_tsla_metrics.pkl
└── transformer_tsla_prediction.png
```

---

#### `make train-aapl`
```bash
make train-aapl
```
**คำอธิบาย:** Train all models for AAPL

---

#### `make train-googl`
```bash
make train-googl
```
**คำอธิบาย:** Train all models for GOOGL

---

#### `make train-nvda`
```bash
make train-nvda
```
**คำอธิบาย:** Train all models for NVDA

---

#### `make train-msft`
```bash
make train-msft
```
**คำอธิบาย:** Train all models for MSFT

---

### Multiple Companies Training

#### `make train-tech`
```bash
make train-tech
```
**คำอธิบาย:** Train major tech stocks

**Companies:** TSLA, AAPL, GOOGL, MSFT, NVDA (5 companies)

**ระยะเวลา:** 2-5 ชั่วโมง

---

#### `make train-semiconductor`
```bash
make train-semiconductor
```
**คำอธิบาย:** Train semiconductor stocks

**Companies:** NVDA, AMD, INTC, TSM (4 companies)

**ระยะเวลา:** 2-4 ชั่วโมง

---

#### `make train-faang`
```bash
make train-faang
```
**คำอธิบาย:** Train FAANG stocks

**Companies:** META, AAPL, AMZN, NFLX, GOOGL (5 companies)

**ระยะเวลา:** 2-5 ชั่วโมง

---

#### `make train-all-default`
```bash
make train-all-default
```
**คำอธิบาย:** Train all default stocks

**Companies:** TSLA, AAPL, GOOGL, MSFT, AMZN (5 companies)

**ระยะเวลา:** 2-5 ชั่วโมง

---

### Specific Model Training

#### `make train-lstm-only`
```bash
make train-lstm-only
```
**คำอธิบาย:** Train LSTM model only for TSLA

**ระยะเวลา:** ~15-20 นาที

---

#### `make train-gru-only`
```bash
make train-gru-only
```
**คำอธิบาย:** Train GRU model only for TSLA

**ระยะเวลา:** ~10-15 นาที

---

#### `make train-transformer-only`
```bash
make train-transformer-only
```
**คำอธิบาย:** Train Transformer model only for TSLA

**ระยะเวลา:** ~20-30 นาที

---

### Quick Test Training

#### `make train-test-quick`
```bash
make train-test-quick
```
**คำอธิบาย:** Quick test training

**Parameters:**
- Ticker: AAPL
- Model: LSTM
- Start: 2023-01-01
- End: 2024-01-01

**ระยะเวลา:** 5-10 นาที

**เมื่อไหร่ใช้:**
- ครั้งแรก
- ทดสอบระบบ
- ตรวจสอบว่าทุกอย่างทำงานได้

---

#### `make train-test-recent`
```bash
make train-test-recent
```
**คำอธิบาย:** Test with recent data

**Parameters:**
- Ticker: TSLA
- Model: ALL
- Start: 2023-01-01
- End: 2024-12-31

**ระยะเวลา:** 15-30 นาที

---

### Airflow Integration

#### `make airflow-trigger`
```bash
make airflow-trigger
```
**คำอธิบาย:** Trigger Airflow DAG (multi_company_stock_training)

**DAG trains:** TSLA, AAPL, GOOGL, MSFT, AMZN

---

#### `make airflow-list`
```bash
make airflow-list
```
**คำอธิบาย:** List all Airflow DAGs

---

#### `make airflow-status`
```bash
make airflow-status
```
**คำอธิบาย:** Show Airflow DAG runs status

---

#### `make airflow-logs`
```bash
make airflow-logs
```
**คำอธิบาย:** Show Airflow scheduler logs

---

## 🔮 Prediction Commands

### Generic Commands (with TICKER parameter)

#### `make predict-day TICKER=AAPL`
```bash
make predict-day TICKER=AAPL
```
**คำอธิบาย:** Predict next 30 days

**Parameters:**
- Model: GRU (default)
- Periods: 30
- Type: day

**ตัวอย่าง:**
```bash
make predict-day TICKER=AAPL
make predict-day TICKER=TSLA
make predict-day TICKER=GOOGL
```

---

#### `make predict-week TICKER=AAPL`
```bash
make predict-week TICKER=AAPL
```
**คำอธิบาย:** Predict next 4 weeks

**Parameters:**
- Model: GRU
- Periods: 4
- Type: week

---

#### `make predict-month TICKER=AAPL`
```bash
make predict-month TICKER=AAPL
```
**คำอธิบาย:** Predict next 3 months

**Parameters:**
- Model: GRU
- Periods: 3
- Type: month

---

#### `make predict-year TICKER=AAPL`
```bash
make predict-year TICKER=AAPL
```
**คำอธิบาย:** Predict next 1 year

**Parameters:**
- Model: GRU
- Periods: 1
- Type: year

---

### Specific Shortcuts (AAPL)

#### `make predict-aapl-day`
```bash
make predict-aapl-day
```
**คำอธิบาย:** Predict AAPL next 30 days

---

#### `make predict-aapl-week`
```bash
make predict-aapl-week
```
**คำอธิบาย:** Predict AAPL next 4 weeks

---

#### `make predict-aapl-month`
```bash
make predict-aapl-month
```
**คำอธิบาย:** Predict AAPL next 3 months

---

#### `make predict-aapl-year`
```bash
make predict-aapl-year
```
**คำอธิบาย:** Predict AAPL next 1 year

---

### Specific Shortcuts (TSLA)

#### `make predict-tsla-day`
```bash
make predict-tsla-day
```
**คำอธิบาย:** Predict TSLA next 30 days

---

#### `make predict-tsla-week`
```bash
make predict-tsla-week
```
**คำอธิบาย:** Predict TSLA next 4 weeks

---

#### `make predict-tsla-month`
```bash
make predict-tsla-month
```
**คำอธิบาย:** Predict TSLA next 3 months

---

### Custom Prediction (Full Control)

#### `make predict-custom`
```bash
make predict-custom TICKER=AAPL MODEL=GRU PERIODS=30 TYPE=day
```
**คำอธิบาย:** Custom prediction with full parameters

**Parameters:**
- `TICKER` - รหัสหุ้น (AAPL, TSLA, etc.) **Required**
- `MODEL` - โมเดล (LSTM, GRU, TRANSFORMER) **Optional (default: GRU)**
- `PERIODS` - จำนวนช่วงเวลา **Optional (default: 30)**
- `TYPE` - ประเภท (day, week, month, year) **Optional (default: day)**

**ตัวอย่าง:**
```bash
# ใช้โมเดล LSTM
make predict-custom TICKER=AAPL MODEL=LSTM PERIODS=30 TYPE=day

# ใช้โมเดล GRU (แนะนำ)
make predict-custom TICKER=AAPL MODEL=GRU PERIODS=3 TYPE=month

# ใช้โมเดล Transformer
make predict-custom TICKER=TSLA MODEL=TRANSFORMER PERIODS=60 TYPE=day

# พยากรณ์ 6 เดือน
make predict-custom TICKER=GOOGL MODEL=GRU PERIODS=6 TYPE=month

# พยากรณ์ 2 ปี
make predict-custom TICKER=NVDA MODEL=GRU PERIODS=2 TYPE=year
```

---

## 📊 Analysis Commands

### Model Comparison

#### `make compare-all`
```bash
make compare-all
```
**คำอธิบาย:** Compare ALL trained models (all tickers)

**ผลลัพธ์:**
- ตารางเปรียบเทียบแต่ละ ticker
- กราฟเปรียบเทียบ (บันทึกใน models/{TICKER}/)
- สรุปโมเดลที่ดีที่สุดของแต่ละ ticker

---

#### `make compare-aapl`
```bash
make compare-aapl
```
**คำอธิบาย:** Compare AAPL models (LSTM vs GRU vs Transformer)

**ผลลัพธ์:**
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

#### `make compare-tsla`
```bash
make compare-tsla
```
**คำอธิบาย:** Compare TSLA models

---

#### `make compare-models`
```bash
make compare-models
```
**คำอธิบาย:** Compare models for TSLA (legacy command)

---

### View Results

#### `make view-tsla`
```bash
make view-tsla
```
**คำอธิบาย:** View TSLA model metrics

**ตัวอย่าง output:**
```
TSLA Model Metrics:

LSTM:
  RMSE: $12.45
  MAE:  $11.23
  MAPE: 5.67%

GRU:
  RMSE: $10.34
  MAE:  $9.87
  MAPE: 4.52%

TRANSFORMER:
  RMSE: $45.67
  MAE:  $44.12
  MAPE: 25.34%
```

---

#### `make view-plots`
```bash
make view-plots
```
**คำอธิบาย:** Open all prediction plots (macOS only)

**ต้องการ:** `open` command (macOS)

---

## 🌐 Services & URLs

#### `make urls`
```bash
make urls
```
**คำอธิบาย:** Show all service URLs

**ตัวอย่าง output:**
```
Service URLs:
  • JupyterLab:  http://localhost:8888  (Token: fintech2025)
  • Airflow:     http://localhost:8083  (admin/fintech2025)
  • FastAPI:     http://localhost:8000/docs
  • Grafana:     http://localhost:3000  (admin/fintech2025)
  • Prometheus:  http://localhost:9090
```

---

### JupyterLab UI

#### `make train-ui`
```bash
make train-ui
```
**คำอธิบาย:** Show info about training UI notebook

---

#### `make open-jupyter`
```bash
make open-jupyter
```
**คำอธิบาย:** Open JupyterLab in browser (macOS only)

**URL:** http://localhost:8888/lab/tree/notebooks/train_stocks_ui.ipynb?token=fintech2025

---

#### `make notebook-info`
```bash
make notebook-info
```
**คำอธิบาย:** Show info about training notebook

---

## 📁 Model Management

#### `make models-list`
```bash
make models-list
```
**คำอธิบาย:** List all trained models (.h5 files)

**ตัวอย่าง output:**
```
Trained models:
jupyter/models/AAPL/gru_aapl_model.h5
jupyter/models/AAPL/lstm_aapl_model.h5
jupyter/models/AAPL/transformer_aapl_model.h5
jupyter/models/TSLA/gru_tsla_model.h5
jupyter/models/TSLA/lstm_tsla_model.h5
```

---

#### `make models-list-all`
```bash
make models-list-all
```
**คำอธิบาย:** List all model files (.h5, .pkl, .png)

---

#### `make models-size`
```bash
make models-size
```
**คำอธิบาย:** Show model sizes

**ตัวอย่าง output:**
```
Model sizes:
24M     jupyter/models/AAPL
28M     jupyter/models/TSLA
26M     jupyter/models/GOOGL
```

---

#### `make models-backup`
```bash
make models-backup
```
**คำอธิบาย:** Backup models to models_backup/

**ตัวอย่าง:**
```bash
make models-backup
# บันทึกไปที่: models_backup/
```

---

#### `make models-clean`
```bash
make models-clean
```
**คำอธิบาย:** Clean all trained models (DANGEROUS!)

**⚠️ Warning:** จะลบโมเดลทั้งหมด! ต้อง confirm ก่อน

**แนะนำ:** Backup ก่อน!
```bash
make models-backup   # Backup ก่อน
make models-clean    # แล้วค่อยลบ
```

---

## 🔧 Development & Testing

### Shell Access

#### `make shell-jupyter`
```bash
make shell-jupyter
```
**คำอธิบาย:** Open shell in JupyterLab container

**ตัวอย่างการใช้:**
```bash
make shell-jupyter

# ใน container:
python scripts/stock_prediction/train_multi_company.py --help
ls -la models/
```

---

#### `make shell-airflow`
```bash
make shell-airflow
```
**คำอธิบาย:** Open shell in Airflow container

---

#### `make shell-fastapi`
```bash
make shell-fastapi
```
**คำอธิบาย:** Open shell in FastAPI container

---

### Testing

#### `make test-yfinance`
```bash
make test-yfinance
```
**คำอธิบาย:** Test yfinance data download

**ตัวอย่าง output:**
```
Testing yfinance download for TSLA...
                 Open       High        Low      Close  Volume
Date
2024-12-01   250.12     255.34     248.90    253.45   1234567
2024-12-02   253.50     258.12     252.10    256.78   1345678
```

---

#### `make test-paths`
```bash
make test-paths
```
**คำอธิบาย:** Test relative paths work correctly

---

## 🧹 Cleanup Commands

#### `make clean`
```bash
make clean
```
**คำอธิบาย:** Clean Python cache files

**ลบ:**
- `__pycache__/` directories
- `*.pyc` files

---

#### `make clean-docker`
```bash
make clean-docker
```
**คำอธิบาย:** Clean Docker (containers, volumes, networks)

**ทำอะไรบ้าง:**
```bash
docker compose down -v --remove-orphans
```

---

#### `make clean-all`
```bash
make clean-all
```
**คำอธิบาย:** Clean everything

**ทำอะไรบ้าง:**
1. Stop services (`make down`)
2. Clean cache (`make clean`)
3. Clean models (`make models-clean`)

**⚠️ Warning:** จะลบทุกอย่าง!

---

#### `make reset`
```bash
make reset
```
**คำอธิบาย:** Full reset

**ทำอะไรบ้าง:**
1. Clean everything (`make clean-all`)
2. Rebuild (`make build`)
3. Start (`make up`)

**ระยะเวลา:** 15-20 นาที

---

## 📚 Workflows

### `make workflow-first-time`
```bash
make workflow-first-time
```
**คำอธิบาย:** First time setup workflow

**ทำอะไรบ้าง:**
1. Build Docker images
2. Start all services
3. Wait 30 seconds
4. Check status
5. Run quick test training

**ระยะเวลา:** 15-20 นาที

---

### `make workflow-daily`
```bash
make workflow-daily
```
**คำอธิบาย:** Daily workflow

**ทำอะไรบ้าง:**
1. Start services
2. Train TSLA models
3. View results

**ระยะเวลา:** 30-60 นาที

---

### `make workflow-weekly`
```bash
make workflow-weekly
```
**คำอธิบาย:** Weekly workflow

**ทำอะไรบ้าง:**
1. Train tech stocks (TSLA, AAPL, GOOGL, MSFT, NVDA)
2. Backup models

**ระยะเวลา:** 2-5 ชั่วโมง

---

## 💡 Tips & Tricks

### 1. การใช้ Parameters

```bash
# Generic commands ต้องใส่ TICKER
make predict-day TICKER=AAPL

# Error ถ้าไม่ใส่
make predict-day
# Output: Error: TICKER not specified!
```

---

### 2. การรันหลายคำสั่งต่อเนื่อง

```bash
# ใช้ && เพื่อรันต่อเนื่อง (หยุดถ้า error)
make up && make wait && make train-aapl

# ใช้ ; เพื่อรันต่อเนื่อง (ไม่หยุดถ้า error)
make train-aapl ; make train-tsla ; make train-googl
```

---

### 3. การ Redirect Output

```bash
# บันทึก output ไปไฟล์
make train-aapl > train.log 2>&1

# ดู log แบบ real-time
tail -f train.log
```

---

### 4. การรันใน Background

```bash
# ใช้ nohup
nohup make train-tech > train-tech.log 2>&1 &

# ใช้ screen
screen -S training
make train-tech
# กด Ctrl+A, D เพื่อ detach

# กลับมาดู
screen -r training
```

---

### 5. การเช็คก่อนรัน

```bash
# เช็คว่า container ทำงานอยู่
make ps

# เช็ค syntax ก่อนเทรน
make check-syntax

# เช็คว่ามีโมเดลอยู่แล้ว
make models-list
```

---

### 6. การใช้ Variables

```bash
# กำหนด variable
TICKER=AAPL

# ใช้ variable
make predict-day TICKER=$TICKER
make compare-$TICKER
```

---

### 7. Cheat Sheet สำหรับวันทำงานปกติ

```bash
# เช้า - เริ่มต้น
make up && make wait

# กลางวัน - เทรนโมเดล
make train-aapl

# บ่าย - เปรียบเทียบและพยากรณ์
make compare-aapl
make predict-aapl-month

# เย็น - Backup และปิด
make models-backup
make down
```

---

### 8. Troubleshooting Quick Commands

```bash
# Container ไม่ทำงาน
make ps
make restart

# เจอ error ไม่รู้สาเหตุ
make logs-jupyter

# เทรนล้มเหลว
make check-syntax
make test-yfinance

# โมเดลไม่เจอ
make models-list
```

---

## 📊 Command Categories Summary

### ตามความถี่การใช้งาน

**ใช้ทุกวัน (Daily):**
- `make up` / `make down`
- `make train-{ticker}`
- `make compare-{ticker}`
- `make predict-{ticker}-day`
- `make logs-jupyter`

**ใช้บางครั้ง (Weekly/Monthly):**
- `make train-tech`
- `make models-backup`
- `make check`
- `make compare-all`

**ใช้น้อย (Rarely):**
- `make all` / `make fresh-start`
- `make build`
- `make clean-docker`
- `make reset`

---

### ตามหมวดหมู่

| หมวด | จำนวนคำสั่ง | ตัวอย่าง |
|------|-------------|---------|
| Quick Start | 5 | `all`, `fresh-start`, `network-fix` |
| Docker | 15 | `build`, `up`, `down`, `logs` |
| Training | 20 | `train-aapl`, `train-tech`, `train-test-quick` |
| Prediction | 12 | `predict-day`, `predict-custom` |
| Analysis | 5 | `compare-all`, `view-tsla` |
| Models | 6 | `models-list`, `models-backup` |
| Development | 5 | `shell-jupyter`, `test-yfinance` |
| Cleanup | 5 | `clean`, `clean-docker`, `reset` |
| Workflows | 3 | `workflow-first-time`, `workflow-daily` |

**รวม:** 50+ คำสั่ง

---

## 📚 เอกสารเพิ่มเติม

- **[README.md](README.md)** - ภาพรวมทั้งระบบ
- **[TRAINING_GUIDE.md](TRAINING_GUIDE.md)** - คู่มือเทรนแบบละเอียด
- **[SUMMARY.md](SUMMARY.md)** - สรุปภาษาไทย

---

**Happy Making! 🚀**

Made with ❤️ for ducation and learning By Sojirat.S
