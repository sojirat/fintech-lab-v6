#!/bin/bash
# Quick script to train stock prediction models
# Usage: ./train_stock.sh TICKER [MODEL_TYPE] [START_DATE] [END_DATE]

set -e

TICKER=${1:-TSLA}
MODEL=${2:-ALL}
START=${3:-2018-01-01}
END=${4:-}

echo "========================================"
echo "Stock Prediction Training Script"
echo "========================================"
echo "Ticker: $TICKER"
echo "Model: $MODEL"
echo "Start Date: $START"
echo "End Date: ${END:-today}"
echo "========================================"

# Check if JupyterLab container is running
if ! docker compose ps jupyterlab | grep -q "Up"; then
    echo "Error: JupyterLab container is not running!"
    echo "Start it with: docker compose up -d jupyterlab"
    exit 1
fi

# Build command
CMD="python scripts/stock_prediction/train_multi_company.py --ticker $TICKER --model $MODEL --start $START"

if [ -n "$END" ]; then
    CMD="$CMD --end $END"
fi

echo ""
echo "Executing: $CMD"
echo ""

# Run training in JupyterLab container
docker compose exec -T jupyterlab bash -c "cd /home/jovyan/work && $CMD"

echo ""
echo "========================================"
echo "Training completed!"
echo "========================================"
echo "Check models in: jupyter/models/$TICKER/"
echo ""
