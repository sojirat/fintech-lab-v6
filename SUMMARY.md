# 📝 สรุปโปรเจค - Fintech Lab v6

**ระบบทำนายราคาหุ้นแบบครบวงจร** ด้วย Machine Learning, Docker, และ Automation

---

## 🎯 โปรเจคนี้คืออะไร?

ระบบเทรนโมเดล Machine Learning เพื่อทำนายราคาหุ้นหลายบริษัท รองรับการเทรน 4 วิธี พร้อมระบบพยากรณ์อนาคตและเปรียบเทียบโมเดล

**เหมาะกับ:**
- 📊 Data Scientists - วิเคราะห์และเทรนโมเดล
- 💻 Developers - Integrate API และ automation
- 🎓 Students - เรียนรู้ Machine Learning และ MLOps
- 💼 Traders - ศึกษาแนวโน้มราคา (ไม่ใช่คำแนะนำการลงทุน!)

---

## ⚡ เริ่มต้นใช้งาน 3 ขั้นตอน

### 1️⃣ Setup ระบบ (3-5 นาที)
```bash
make all
```

### 2️⃣ เทรนทดสอบ (5-10 นาที)
```bash
make train-test-quick
```

### 3️⃣ เทรนจริง (30-60 นาที)
```bash
make train-aapl
```

**เสร็จแล้ว!** 🎉

---

## 🏗️ สถาปัตยกรรมระบบ

```
┌─────────────────────────────────────────────────────────┐
│                    Fintech Lab v6                       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. การเทรน (เลือกได้ 4 วิธี)                               │
│     • CLI (Make commands)      ⚡⚡⚡ เร็วที่สุด               │
│     • UI (JupyterLab Notebook) 🎨 ง่ายที่สุด                │
│     • Airflow (Scheduled)      ⏰ อัตโนมัติ                │
│     • Python Script            🔧 ยืดหยุ่นสูงสุด             │
│                                                        │
│  2. โมเดล ML (3 ประเภท)                                │
│     • LSTM        - MAPE 4.17%  ⭐⭐                    │
│     • GRU         - MAPE 3.42%  ⭐⭐⭐ ดีที่สุด!            │
│     • Transformer - MAPE 31.97% ⭐                      │
│                                                         │
│  3. การวิเคราะห์                                          │
│     • เปรียบเทียบโมเดล (LSTM vs GRU vs Transformer)       │
│     • พยากรณ์อนาคต (day, week, month, year)              │
│     • กราฟและ metrics แบบละเอียด                         │
│                                                         │
│  4. Infrastructure                                      │
│     • Docker Compose - 7 services                       │
│     • Shared Volume - /jupyter/models/                  │
│     • Makefile - 50+ คำสั่ง                               │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 🎯 4 วิธีเทรนโมเดล (เลือกได้ตามความชอบ!)

### 1. Command Line (CLI) ⚡ เร็ว แม่นยำ

```bash
# บริษัทเดียว
make train-aapl

# หลายบริษัท
make train-tech              # TSLA, AAPL, GOOGL, MSFT, NVDA

# ทดสอบเร็ว
make train-test-quick        # 5-10 นาที
```

**ข้อดี:**
- ⚡ เร็วที่สุด - รันคำสั่งเดียวจบ
- 🎯 แม่นยำ - ควบคุมได้ทุกอย่าง
- 📋 ง่าย - จำแค่ `make train-{ticker}`

**เมื่อไหร่ใช้:**
- Production environment
- Batch processing
- CI/CD pipeline

---

### 2. JupyterLab Notebook (UI) 🎨 ง่าย ดูผลทันที

```bash
# เปิด JupyterLab
make open-jupyter

# หรือเปิดเอง
# URL: http://localhost:8888
# Token: fintech2025
# File: notebooks/train_stocks_ui.ipynb
```

**ข้อดี:**
- 🎨 UI สวยงาม - เห็นภาพชัดเจน
- 🔄 Real-time - เห็นความคืบหน้าทันที
- 📊 Visualization - กราฟในหน้าเดียว

**เมื่อไหร่ใช้:**
- ครั้งแรก
- ทดสอบและ experiment
- Present ผลงาน

---

### 3. Airflow Automation ⏰ Schedule อัตโนมัติ

```bash
# Trigger DAG
make airflow-trigger

# หรือเปิด Web UI
# URL: http://localhost:8083
# Username: admin
# Password: fintech2025
```

**ข้อดี:**
- ⏰ Schedule - รันอัตโนมัติทุกวัน
- 📊 Monitoring - เห็นสถานะแต่ละ Task
- 🔁 Retry - Retry อัตโนมัติเมื่อล้มเหลว

**เมื่อไหร่ใช้:**
- Production environment
- Scheduled training (ทุกวัน/สัปดาห์/เดือน)
- MLOps pipeline

---

### 4. Python Script 🔧 ยืดหยุ่นสูงสุด

```bash
# เข้า container
make shell-jupyter

# รัน script
python scripts/stock_prediction/train_multi_company.py \
    --ticker AAPL \
    --model GRU \
    --start-date 2018-01-01 \
    --epochs 50
```

**ข้อดี:**
- 🔧 ยืดหยุ่นสูง - ปรับค่าได้ทุกอย่าง
- 🎯 ควบคุมเต็มที่ - เขียน logic custom ได้
- 🐍 Python Native - เรียกจาก script อื่นได้

**เมื่อไหร่ใช้:**
- Development
- Custom workflows
- Integration กับระบบอื่น

---

## 🔮 พยากรณ์ราคาในอนาคต

### พยากรณ์แบบง่าย (ใช้โมเดล GRU)

```bash
# พยากรณ์ 30 วัน
make predict-aapl-day

# พยากรณ์ 3 เดือน
make predict-aapl-month

# พยากรณ์ 1 ปี
make predict-aapl-year
```

### พยากรณ์แบบกำหนดเอง (เลือกโมเดล)

```bash
# ใช้โมเดล LSTM
make predict-custom TICKER=AAPL MODEL=LSTM PERIODS=30 TYPE=day

# ใช้โมเดล GRU (แนะนำ - แม่นยำที่สุด)
make predict-custom TICKER=AAPL MODEL=GRU PERIODS=3 TYPE=month

# ใช้โมเดล Transformer
make predict-custom TICKER=TSLA MODEL=TRANSFORMER PERIODS=60 TYPE=day
```

### ผลลัพธ์ที่ได้

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

**พร้อม:**
- 📊 กราฟเปรียบเทียบราคาจริงและพยากรณ์
- 📈 แนวโน้ม Bullish/Bearish
- ⚠️ Disclaimer พร้อม accuracy metrics

---

## 📊 เปรียบเทียบโมเดล

```bash
# เปรียบเทียบทุกบริษัท
make compare-all

# เปรียบเทียบเฉพาะบริษัท
make compare-aapl
```

### ผลลัพธ์

```
🏆 RANKINGS:
Best RMSE:  GRU ($6.73)
Best MAE:   GRU ($6.54)
Best MAPE:  GRU (3.42%)

📈 OVERALL RANKING:
1. GRU         ⭐⭐⭐  (MAPE 3.42%)
2. LSTM        ⭐⭐   (MAPE 4.17%)
3. TRANSFORMER ⭐     (MAPE 31.97%)

💡 RECOMMENDATION:
   Use GRU model for AAPL
```

**พร้อม:**
- ตารางเปรียบเทียบแบบละเอียด
- กราฟแท่งเปรียบเทียบ
- คำแนะนำโมเดลที่ดีที่สุด

---

## ✨ Features หลัก

### 🎯 Training Features
- ✅ **Multi-Company** - เทรนได้หลายบริษัทพร้อมกัน
- ✅ **3 Models** - LSTM, GRU (ดีที่สุด), Transformer
- ✅ **Flexible Dates** - กำหนดช่วงเวลาได้
- ✅ **Auto Retry** - จัดการ Yahoo Finance rate limit
- ✅ **yahooquery** - ใช้ yahooquery เป็นหลัก (ไม่ติด rate limit)

### 🔮 Prediction Features
- ✅ **Future Prediction** - พยากรณ์ day, week, month, year
- ✅ **Model Selection** - เลือกโมเดลได้ (LSTM, GRU, Transformer)
- ✅ **Rolling Window** - ใช้ 60 วันล่าสุดในการพยากรณ์
- ✅ **Trend Analysis** - แสดงแนวโน้ม Bullish/Bearish

### 📊 Comparison Features
- ✅ **Model Comparison** - เปรียบเทียบ LSTM vs GRU vs Transformer
- ✅ **Ranking System** - จัดอันดับตาม RMSE, MAE, MAPE
- ✅ **Recommendation** - แนะนำโมเดลที่ดีที่สุด

### 🚀 Infrastructure Features
- ✅ **Docker Compose** - 7 services (JupyterLab, Airflow, FastAPI, etc.)
- ✅ **Makefile** - 50+ คำสั่งใช้งานง่าย
- ✅ **Shared Volume** - /jupyter/models/ สำหรับเก็บโมเดล
- ✅ **Relative Paths** - รันได้ทั้ง Docker และ Local

---

## 🌐 Services

| Service | URL | Credentials | Purpose |
|---------|-----|-------------|---------|
| **JupyterLab** | http://localhost:8888 | Token: `fintech2025` | Training Notebook UI |
| **Airflow** | http://localhost:8083 | admin / fintech2025 | Workflow Automation |
| **FastAPI** | http://localhost:8000/docs | - | API Documentation |
| **Grafana** | http://localhost:3000 | admin / fintech2025 | Monitoring Dashboard |
| **Prometheus** | http://localhost:9090 | - | Metrics Collection |
| **PostgreSQL** | localhost:5432 | postgres / postgres | Database |
| **Redis** | localhost:6379 | - | Cache |

```bash
# แสดง URLs ทั้งหมด
make urls
```

---

## 📁 โครงสร้างโปรเจค

```
fintech-lab-v6/
├── 📄 Makefile                          # 50+ คำสั่ง make
├── 📄 docker-compose.yml                # Docker services
├── 📄 train_stock.sh                    # Helper script
│
├── 📂 jupyter/                          # JupyterLab service
│   ├── 📄 Dockerfile                    # Custom image (TensorFlow 2.15)
│   ├── 📂 notebooks/
│   │   └── train_stocks_ui.ipynb       # 🎨 Training UI
│   ├── 📂 models/                       # โมเดลที่เทรนแล้ว
│   │   ├── AAPL/
│   │   │   ├── gru_aapl_model.h5       # ⭐ ดีที่สุด
│   │   │   ├── lstm_aapl_model.h5
│   │   │   ├── transformer_aapl_model.h5
│   │   │   ├── *_scaler.pkl
│   │   │   ├── *_metrics.pkl
│   │   │   ├── *_prediction.png
│   │   │   ├── gru_aapl_future_prediction.png
│   │   │   └── comparison_aapl.png
│   │   └── TSLA/
│   └── 📂 scripts/
│       └── stock_prediction/
│           ├── train_multi_company.py   # 🎯 สคริปต์เทรนหลัก
│           ├── compare_all_models.py    # 📊 เปรียบเทียบโมเดล
│           ├── predict_future.py        # 🔮 พยากรณ์อนาคต
│           ├── lstm_stock_prediction.py
│           ├── gru_stock_prediction.py
│           └── transformer_stock_prediction.py
│
├── 📂 airflow/                          # Airflow service
│   ├── 📄 Dockerfile
│   └── 📂 dags/
│       └── multi_company_stock_training_dag.py
│
├── 📂 backend/                          # FastAPI service
│   ├── 📄 Dockerfile
│   ├── 📄 main.py
│   └── 📄 requirements.txt
│
└── 📂 docs/                             # เอกสาร
    ├── 📄 README.md                     # ภาพรวมทั้งระบบ
    ├── 📄 TRAINING_GUIDE.md             # คู่มือเทรนแบบละเอียด
    ├── 📄 MAKEFILE_GUIDE.md             # คู่มือ Makefile
    └── 📄 SUMMARY.md                    # สรุปภาษาไทย (ไฟล์นี้!)
```

---

## 🎓 Workflows แนะนำ

### 🆕 ครั้งแรก (First Time)

```bash
# 1. Setup ระบบ
make workflow-first-time

# หรือทีละขั้น
make all                     # Setup
make train-test-quick        # ทดสอบ (5-10 นาที)
make train-aapl              # เทรนจริง (30-60 นาที)
```

---

### 📅 ใช้ทุกวัน (Daily)

```bash
# 1 คำสั่งจบ
make workflow-daily

# หรือทีละขั้น
make up                      # เปิด services
make train-aapl              # เทรนโมเดล
make compare-aapl            # เปรียบเทียบ
make predict-aapl-day        # พยากรณ์
make view-tsla               # ดูผล
```

---

### 📊 ใช้ทุกสัปดาห์ (Weekly)

```bash
# 1 คำสั่งจบ
make workflow-weekly

# หรือทีละขั้น
make train-tech              # เทรนหลายบริษัท (2-5 ชั่วโมง)
make compare-all             # เปรียบเทียบทุกบริษัท
make models-backup           # Backup โมเดล
```

---

### 🔮 พยากรณ์และวิเคราะห์

```bash
# 1. เทรนโมเดล
make train-aapl

# 2. เปรียบเทียบโมเดล
make compare-aapl
# Output: "Use GRU model for AAPL"

# 3. พยากรณ์ด้วยโมเดลที่ดีที่สุด
make predict-aapl-month

# 4. ลองโมเดลอื่น
make predict-custom TICKER=AAPL MODEL=LSTM PERIODS=30 TYPE=day
```

---

## 📊 ผลลัพธ์ตัวอย่าง (AAPL)

### Model Performance

| Model | RMSE | MAE | MAPE | Rank |
|-------|------|-----|------|------|
| **GRU** | $6.73 | $6.54 | **3.42%** | 🥇 ⭐⭐⭐ |
| **LSTM** | $8.28 | $7.98 | 4.17% | 🥈 ⭐⭐ |
| **Transformer** | $61.33 | $61.17 | 31.97% | 🥉 ⭐ |

**Recommendation:** ใช้โมเดล **GRU** สำหรับ AAPL

---

### Prediction Example (30 วัน)

```
Current Price:    $259.37
Predicted (30d):  $181.87
Change:           -$77.50 (-29.88%)
Trend:            🔴 BEARISH (Downward)
```

---

## 💡 Tips & Best Practices

### 1. 🚀 เริ่มต้นด้วย Quick Test

```bash
# ทดสอบระบบก่อน (5-10 นาที)
make train-test-quick
```

ทำไมต้องทดสอบก่อน?
- ตรวจสอบว่าทุกอย่างทำงานได้
- ประหยัดเวลา (ไม่ต้องเทรนเต็มแล้วค่อยเจอ error)
- ทดสอบ Yahoo Finance API

---

### 2. 📊 เปรียบเทียบโมเดลก่อนพยากรณ์

```bash
# เทรนทั้ง 3 โมเดล
make train-aapl

# เปรียบเทียบ
make compare-aapl

# ใช้โมเดลที่ดีที่สุด
make predict-custom TICKER=AAPL MODEL=GRU PERIODS=30 TYPE=day
```

---

### 3. 💾 Backup ก่อนลบ

```bash
# Backup
make models-backup

# เช็คขนาด
make models-size

# แล้วค่อยลบ
make models-clean
```

---

### 4. 🎯 ใช้ GRU สำหรับความแม่นยำสูงสุด

GRU ให้ผลลัพธ์ดีที่สุดในทุกกรณี:
- ⭐ MAPE: 3.42% (LSTM: 4.17%, Transformer: 31.97%)
- ⚡ เร็วกว่า LSTM
- 💾 ใช้หน่วยความจำน้อยกว่า

---

### 5. ⚠️ พยากรณ์ระยะสั้นแม่นยำกว่า

| ระยะเวลา | ความแม่นยำ | คำแนะนำ |
|----------|-----------|---------|
| 1-30 วัน | ⭐⭐⭐ | ใช้ได้ |
| 1-3 เดือน | ⭐⭐ | ใช้ระวัง |
| 6-12 เดือน | ⭐ | ดูแนวโน้มเท่านั้น |

---

### 6. 📅 ใช้ข้อมูลย้อนหลังเพียงพอ

**แนะนำ:** 5-7 ปี
- น้อยกว่า 3 ปี: อาจไม่แม่นยำ ❌
- 5-7 ปี: สมดุล ✅
- มากกว่า 10 ปี: ข้อมูลเก่าไม่เกี่ยวข้อง ⚠️

```bash
# แนะนำ
START_DATE='2018-01-01'  # ✅ 7 ปี

# หลีกเลี่ยง
START_DATE='2023-01-01'  # ❌ 2 ปี
```

---

### 7. 📜 ดู Logs เมื่อมีปัญหา

```bash
# ดู logs
make logs-jupyter

# เช็คสถานะ
make check
make ps

# เข้า container debug
make shell-jupyter
```

---

### 8. 🔄 Update โมเดลเป็นประจำ

ตลาดหุ้นเปลี่ยนแปลงตลอดเวลา:
- **แนะนำ:** Update ทุกสัปดาห์/เดือน
- **ใช้ Airflow:** Schedule อัตโนมัติทุกวันเวลา 6:00 AM

```bash
# Manual update
make train-aapl

# Airflow auto-schedule
make airflow-trigger
```

---

## 🚨 Troubleshooting พบบ่อย

### ❌ Yahoo Finance Rate Limit (429 Error)

**สาเหตุ:** Yahoo Finance จำกัดการเรียก API (~100-200 requests/hour)

**วิธีแก้:**
1. ✅ ระบบมี **retry อัตโนมัติ** 5 ครั้ง (5s, 10s, 20s, 40s, 80s)
2. ✅ ใช้ **yahooquery** เป็นหลัก (ไม่ติด rate limit บ่อย)
3. ✅ **Fallback** ไป yfinance ถ้าจำเป็น
4. ⏰ รอ 5-10 นาทีแล้วลองใหม่

```bash
# ลองใหม่
make train-aapl
```

---

### ❌ Container ไม่ทำงาน

```bash
# เช็คสถานะ
make ps

# ดู logs
make logs-jupyter

# Restart
make restart

# หรือ rebuild
make down
make build-fast
make up && make wait
```

---

### ❌ เทรนล้มเหลว

```bash
# 1. เช็ค syntax
make check-syntax

# 2. ทดสอบ yfinance
make test-yfinance

# 3. เข้า container debug
make shell-jupyter
python scripts/stock_prediction/train_multi_company.py --help
```

---

### ❌ โมเดลไม่เจอ

```bash
# ดูว่ามีโมเดลอะไรบ้าง
make models-list

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

## 📖 เอกสารทั้งหมด

| ไฟล์ | บรรทัด | เนื้อหา | เมื่อไหร่ใช้ |
|------|--------|---------|--------------|
| **[README.md](README.md)** | 855 | ภาพรวมทั้งระบบ, Quick Start, 4 วิธีเทรน | เริ่มต้นใช้งาน |
| **[TRAINING_GUIDE.md](TRAINING_GUIDE.md)** | 1,200+ | คู่มือเทรนแบบละเอียด, Best Practices, FAQ | เทรนครั้งแรก, มีปัญหา |
| **[MAKEFILE_GUIDE.md](MAKEFILE_GUIDE.md)** | 1,100+ | คู่มือคำสั่ง Make ทั้งหมด 50+ คำสั่ง | ดูคำสั่งทั้งหมด |
| **[SUMMARY.md](SUMMARY.md)** | 900+ | สรุปภาษาไทย (ไฟล์นี้!) | ภาพรวมทั้งระบบ |

---

## 🎯 Roadmap

### ✅ Completed (เสร็จแล้ว)
- [x] Multi-company training (หลายบริษัทพร้อมกัน)
- [x] 3 models (LSTM, GRU, Transformer)
- [x] 4 training methods (CLI, UI, Airflow, Python)
- [x] Airflow automation (Schedule อัตโนมัติ)
- [x] JupyterLab UI (Training notebook)
- [x] Makefile commands (50+ คำสั่ง)
- [x] Rate limit handling (Auto retry)
- [x] yahooquery integration (ไม่ติด rate limit)
- [x] Model comparison (เปรียบเทียบโมเดล)
- [x] Future prediction (พยากรณ์อนาคต)
- [x] Complete documentation (เอกสารครบ 5 ไฟล์)

### 🚧 In Progress (กำลังทำ)
- [ ] FastAPI prediction endpoints
- [ ] Real-time prediction API
- [ ] Model versioning

### 📋 Planned (วางแผนไว้)
- [ ] More technical indicators (RSI, MACD, Bollinger Bands)
- [ ] Ensemble models (รวมโมเดลหลายตัว)
- [ ] Backtesting framework (ทดสอบ strategy)
- [ ] Portfolio optimization (จัดพอร์ตโฟลิโอ)
- [ ] Real-time streaming data (ข้อมูล real-time)
- [ ] Mobile app (แอพมือถือ)

---

## ⚠️ Disclaimer (ข้อจำกัดความรับผิดชอบ)

**โปรเจคนี้สร้างขึ้นเพื่อการศึกษาเท่านั้น**

### ❌ ไม่ใช่
- ❌ **ไม่ใช่คำแนะนำการลงทุน**
- ❌ ไม่รับประกันความแม่นยำของการพยากรณ์
- ❌ ไม่รับผิดชอบต่อความเสียหายจากการใช้งาน
- ❌ ไม่เหมาะกับการตัดสินใจลงทุนจริง

### ✅ เหมาะกับ
- ✅ เรียนรู้ Machine Learning
- ✅ ศึกษา MLOps และ automation
- ✅ ทดลอง time series prediction
- ✅ พัฒนาทักษะ Data Science

**การลงทุนมีความเสี่ยง ควรศึกษาข้อมูลก่อนตัดสินใจลงทุน**

---

## 💻 Technical Stack

### Backend
- 🐍 **Python 3.10**
- 🧠 **TensorFlow 2.15** - Deep Learning
- 📊 **scikit-learn 1.3** - Data preprocessing
- 📈 **pandas 2.1** - Data manipulation
- 🔢 **numpy 1.24** - Numerical computing

### Data Source
- 📊 **yahooquery** - Primary (ไม่ติด rate limit)
- 📊 **yfinance** - Fallback

### Infrastructure
- 🐳 **Docker Compose** - Container orchestration
- ⏰ **Apache Airflow** - Workflow automation
- 🚀 **FastAPI** - REST API
- 📓 **JupyterLab** - Interactive notebooks

### Database & Cache
- 🐘 **PostgreSQL** - Database
- 🔴 **Redis** - Cache

### Monitoring
- 📊 **Grafana** - Visualization
- 📈 **Prometheus** - Metrics collection

---

## 📊 ข้อมูลโปรเจค

### 📈 สถิติ

- **Services:** 7 containers
- **Models:** 3 types (LSTM, GRU, Transformer)
- **Training Methods:** 4 ways
- **Makefile Commands:** 50+ commands
- **Documentation:** 5 files (3,500+ lines)
- **Supported Stocks:** Unlimited
- **Prediction Periods:** day, week, month, year

### 🎯 Performance

| Model | Training Time | MAPE (AAPL) | Recommended |
|-------|---------------|-------------|-------------|
| LSTM | 15-20 min | 4.17% | ⭐⭐ |
| GRU | 10-15 min | **3.42%** | ⭐⭐⭐ |
| Transformer | 20-30 min | 31.97% | ⭐ |

### 🚀 Setup Time

| Task | Time |
|------|------|
| First Setup | 15-20 min |
| Quick Test | 5-10 min |
| Train Single (3 models) | 30-60 min |
| Train Tech (5 stocks) | 2-5 hours |

---

## 🤝 Contributing

Pull requests are welcome! สำหรับการเปลี่ยนแปลงใหญ่ กรุณาเปิด issue ก่อนเพื่อหารือ

---

## 📜 License

This project is for educational purposes only.

---

## 🎉 เริ่มต้นเลยตอนนี้!

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

---

## 📞 ติดต่อ & ช่วยเหลือ

### ❓ มีคำถาม?
1. อ่าน [TRAINING_GUIDE.md](TRAINING_GUIDE.md) FAQ section
2. อ่าน [MAKEFILE_GUIDE.md](MAKEFILE_GUIDE.md) Tips & Tricks
3. เช็ค Troubleshooting section ใน README

