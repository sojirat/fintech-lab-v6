FROM jupyter/scipy-notebook:latest

USER root

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    git \
    vim \
    curl \
    && rm -rf /var/lib/apt/lists/*

USER ${NB_UID}

# Upgrade pip
RUN pip install --upgrade pip

# Install ML/Data Science dependencies with specific versions for stability
RUN pip install --no-cache-dir \
    tensorflow==2.15.0 \
    scikit-learn==1.3.2 \
    yahooquery \
    yfinance==0.2.32 \
    pandas==2.1.4 \
    numpy==1.24.3 \
    matplotlib==3.8.2 \
    seaborn==0.13.0 \
    plotly==5.18.0 \
    psycopg2-binary==2.9.9 \
    pymongo==4.6.1 \
    redis==5.0.1 \
    requests==2.31.0 \
    pyyaml==6.0.1

# Set working directory
WORKDIR /home/jovyan/work

# Create necessary directories with proper structure for multi-company models
RUN mkdir -p models notebooks data \
    scripts/stock_prediction \
    scripts/fraud_detection \
    scripts/crypto_analysis \
    scripts/dashboards \
    blockchain \
    models/TSLA models/AAPL models/GOOGL models/MSFT models/AMZN

CMD ["start-notebook.sh", "--NotebookApp.token='fintech2025'"]