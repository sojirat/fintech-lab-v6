#!/bin/bash

echo "📦 Installing Python dependencies for TSLA Stock Prediction..."
echo ""

pip install --quiet --upgrade pip

echo "Installing TensorFlow..."
pip install --quiet tensorflow==2.15.0

echo "Installing scikit-learn..."
pip install --quiet scikit-learn==1.3.2

echo "Installing yfinance..."
pip install --quiet yfinance==0.2.32

echo "Installing other dependencies..."
pip install --quiet pandas numpy matplotlib

echo ""
echo "✅ All dependencies installed successfully!"
echo ""
echo "You can now run:"
echo "  bash train_all_models.sh"
