# Fintech Lab Services

รายการ services ทั้งหมดที่รันใน Docker Compose environment

---

## 🌐 Web UI Services

### 1. JupyterLab
- **URL**: http://localhost:8888
- **Password**: `fintech2025`
- **คำอธิบาย**: Interactive notebook สำหรับ data science และ machine learning
- **ใช้สำหรับ**: วิเคราะห์ข้อมูล, เขียน Python code, data visualization
- **ภาษา**: Python, R, Julia

### 2. FastAPI Backend
- **URL**: http://localhost:8000
- **Docs**: http://localhost:8000/docs (Swagger UI)
- **คำอธิบาย**: REST API backend framework ที่เร็วและทันสมัย
- **ใช้สำหรับ**: สร้าง API endpoints, backend logic

### 3. Django Frontend
- **URL**: http://localhost:8082
- **คำอธิบาย**: Web framework สำหรับ log viewer application
- **ใช้สำหรับ**: ดู logs, web interface

### 4. Grafana
- **URL**: http://localhost:3000
- **Username**: `admin`
- **Password**: `fintech2025`
- **คำอธิบาย**: Dashboard และ visualization platform
- **ใช้สำหรับ**: สร้าง dashboard, monitoring, data visualization

### 5. Prometheus
- **URL**: http://localhost:9090
- **คำอธิบาย**: Metrics collection และ monitoring system
- **ใช้สำหรับ**: เก็บ metrics, alert rules, time-series data

---

## 🔧 Backend Services (ไม่มี UI)

### 6. PostgreSQL Database
- **Host**: `localhost`
- **Port**: `5432`
- **Database**: `fintech`
- **Username**: `fintech`
- **Password**: `fintech`
- **คำอธิบาย**: Relational database
- **ใช้สำหรับ**: เก็บข้อมูลแบบโครงสร้าง (structured data)
- **เชื่อมต่อผ่าน**: psql, pgAdmin, DBeaver หรือ code

### 7. Redis
- **Host**: `localhost`
- **Port**: `6379`
- **ไม่มี password**
- **คำอธิบาย**: In-memory cache และ message broker
- **ใช้สำหรับ**: Caching, session storage, pub/sub messaging
- **ไม่มี UI** - ทำงานเบื้องหลังเท่านั้น
- **เชื่อมต่อผ่าน**: redis-cli หรือ code
- **หมายเหตุ**: สามารถเพิ่ม Redis Commander/RedisInsight ถ้าต้องการ UI

### 8. MongoDB
- **Host**: `localhost`
- **Port**: `27017`
- **Database**: `logviewer`
- **ไม่มี username/password**
- **คำอธิบาย**: NoSQL document database
- **ใช้สำหรับ**: เก็บ logs และข้อมูลแบบ document (JSON-like)
- **ไม่มี UI** - ทำงานเบื้องหลังเท่านั้น
- **เชื่อมต่อผ่าน**: MongoDB Compass, mongosh, pymongo หรือ code

### 9. Apache Airflow (Workflow Orchestration)
- **URL**: http://localhost:8083
- **Username**: `admin`
- **Password**: `fintech2025`
- **คำอธิบาย**: Platform สำหรับสร้างและจัดการ data pipelines และ workflows
- **ใช้สำหรับ**:
  - สร้าง ETL pipelines
  - Schedule และ monitor workflows
  - Orchestrate data processing tasks
  - Automate FinTech data pipelines
- **มี Web UI** - สามารถดู DAGs, logs, และ monitor tasks
- **ภาษา**: Python-based
- **หมายเหตุ**: ทดแทน KNIME สำหรับ workflow automation ใน Docker

### 10. Ganache (Ethereum Blockchain Simulator)
- **RPC URL**: http://localhost:8545
- **Network ID**: `1337`
- **คำอธิบาย**: Local Ethereum blockchain สำหรับ development
- **ใช้สำหรับ**:
  - ทดสอบ Smart Contracts
  - Develop DeFi applications
  - ทดสอบ Web3 transactions โดยไม่เสียเงินจริง
- **ไม่มี UI** - เป็น JSON-RPC endpoint (ไม่สามารถเปิดใน browser ได้)
- **เชื่อมต่อผ่าน**: Web3.js, Ethers.js, Truffle, Hardhat
- **หมายเหตุ**: ถ้าเปิด http://localhost:8545 ใน browser จะเห็น "400 Bad Request" ซึ่งเป็นปกติ เพราะต้องใช้ JSON-RPC calls

---

## 🗂️ Data Volumes

- `postgres_data` - PostgreSQL database files
- `mongodb_data` - MongoDB database files
- `grafana_data` - Grafana dashboards และ settings
- `./jupyter` - JupyterLab notebooks
- `./backend` - FastAPI source code
- `./frontend` - Django source code
- `./airflow/dags` - Airflow DAG files (workflows)
- `./airflow/logs` - Airflow execution logs
- `./monitoring/prometheus.yml` - Prometheus configuration

---

## 📝 Note about KNIME

KNIME Analytics Platform เป็น desktop application ที่ไม่เหมาะกับการรันใน Docker

**แนะนำ:**
- ติดตั้ง KNIME Desktop จาก: https://www.knime.com/downloads
- หรือใช้ Apache Airflow (รวมอยู่ใน stack แล้ว) สำหรับ workflow automation

ดู `knime/README.md` สำหรับรายละเอียดเพิ่มเติม

---

## 🔐 Credentials Summary

| Service | Username | Password | Port |
|---------|----------|----------|------|
| Grafana | admin | fintech2025 | 3000 |
| JupyterLab | - | fintech2025 | 8888 |
| Airflow | admin | fintech2025 | 8083 |
| PostgreSQL | fintech | fintech | 5432 |
| MongoDB | - | - | 27017 |
| Redis | - | - | 6379 |
| FastAPI | - | - | 8000 |
| Django | - | - | 8082 |
| Prometheus | - | - | 9090 |
| Ganache | - | - | 8545 |

---

## 🚀 Quick Start

Start all services:
```bash
docker compose up -d
```

Stop all services:
```bash
docker compose down
```

Remove all data (fresh start):
```bash
docker compose down -v
```


เช็ค status ของ services:
```bash
docker compose ps
```

ดู logs:
```bash
docker compose logs [service-name]
# ตัวอย่าง: docker compose logs grafana
```

Restart service:
```bash
docker compose restart [service-name]
```
