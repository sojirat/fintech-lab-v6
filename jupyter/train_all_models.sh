#!/bin/bash

# Train All TSLA Stock Prediction Models
# This script trains LSTM, GRU, and Transformer models sequentially

echo "=================================="
echo "TSLA Stock Prediction Model Training"
echo "=================================="
echo ""

# Check if TensorFlow is installed
if ! python -c "import tensorflow" 2>/dev/null; then
    echo "⚠️  TensorFlow not found!"
    echo ""
    echo "Please install dependencies first:"
    echo "  bash install_dependencies.sh"
    echo ""
    echo "Or install manually:"
    echo "  pip install tensorflow scikit-learn yfinance"
    echo ""
    exit 1
fi

cd /home/jovyan/work

echo "📊 Step 1/4: Training LSTM Model..."
python scripts/stock_prediction/lstm_stock_prediction.py
if [ $? -eq 0 ]; then
    echo "✓ LSTM model trained successfully"
else
    echo "✗ LSTM training failed"
    exit 1
fi

echo ""
echo "📊 Step 2/4: Training GRU Model..."
python scripts/stock_prediction/gru_stock_prediction.py
if [ $? -eq 0 ]; then
    echo "✓ GRU model trained successfully"
else
    echo "✗ GRU training failed"
    exit 1
fi

echo ""
echo "📊 Step 3/4: Training Transformer Model..."
python scripts/stock_prediction/transformer_stock_prediction.py
if [ $? -eq 0 ]; then
    echo "✓ Transformer model trained successfully"
else
    echo "✗ Transformer training failed"
    exit 1
fi

echo ""
echo "📊 Step 4/4: Comparing Models..."
python scripts/stock_prediction/compare_models.py
if [ $? -eq 0 ]; then
    echo "✓ Model comparison completed"
else
    echo "✗ Model comparison failed"
    exit 1
fi

echo ""
echo "=================================="
echo "✅ All models trained successfully!"
echo "=================================="
echo ""
echo "Results saved in: models/"
ls -lh models/
