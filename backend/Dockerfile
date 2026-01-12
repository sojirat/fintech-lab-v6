FROM python:3.10-slim
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Copy requirements and install dependencies with longer timeout
COPY requirements.txt .
RUN pip install --default-timeout=300 --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create models directory
RUN mkdir -p /app/models

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]