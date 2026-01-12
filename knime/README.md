# KNIME Docker Setup

## ⚠️ Important Note

KNIME Analytics Platform is a desktop application and doesn't work well in Docker without a display server.

**We recommend using the desktop version instead of Docker.**

## 🎯 Recommended Approach: Desktop Installation

### For macOS (your system):
1. Go to: https://www.knime.com/downloads
2. Download **KNIME Analytics Platform** for macOS
3. Install the .dmg file
4. Launch KNIME from Applications

## 🐳 Alternative: Docker with X11 (Advanced)

If you really need KNIME in Docker:

### Step 1: Download KNIME
1. Download Linux version from: https://www.knime.com/downloads
2. Get: `knime_X.X.X.linux.gtk.x86_64.tar.gz`
3. Place it in this `knime/` directory

### Step 2: Update Dockerfile
Uncomment the installation lines in the Dockerfile

### Step 3: Set up X11 forwarding
```bash
# Install XQuartz on macOS
brew install --cask xquartz

# Start XQuartz
open -a XQuartz

# Allow connections
xhost + localhost

# Update docker compose.yml to add:
environment:
  - DISPLAY=host.docker.internal:0
volumes:
  - /tmp/.X11-unix:/tmp/.X11-unix
```

### Step 4: Build and run
```bash
docker compose build knime
docker compose up -d knime
```

## 🔄 Better Alternatives

If you need workflow automation in Docker:

### Apache Airflow
- Workflow orchestration
- Python-based
- Great Docker support
```yaml
airflow:
  image: apache/airflow:2.8.1
  ports:
    - "8081:8080"
```

### Prefect
- Modern workflow orchestration
- Python-native
- Cloud and self-hosted
```yaml
prefect:
  image: prefecthq/prefect:2-latest
  ports:
    - "4200:4200"
```

### Apache NiFi
- Data flow automation
- Visual programming
- Good Docker support
```yaml
nifi:
  image: apache/nifi:latest
  ports:
    - "8443:8443"
```

## 📚 Resources

- KNIME Documentation: https://docs.knime.com/
- KNIME Forum: https://forum.knime.com/
- KNIME Hub: https://hub.knime.com/
