"""
Multi-Company Stock Prediction Training Script
Supports LSTM, GRU, and Transformer models for multiple companies
"""
import numpy as np
import pandas as pd
try:
    from yahooquery import Ticker
    USE_YAHOOQUERY = True
except ImportError:
    import yfinance as yf
    USE_YAHOOQUERY = False
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, mean_absolute_percentage_error
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, GRU, Dense, Dropout, MultiHeadAttention, LayerNormalization
from tensorflow.keras.callbacks import EarlyStopping
import pickle
import os
import sys
import argparse
from datetime import datetime
import time
import requests


class StockModelTrainer:
    """Universal trainer for stock prediction models"""

    def __init__(self, ticker, model_type, start_date='2018-01-01', end_date=None, sequence_length=60):
        self.ticker = ticker.upper()
        self.model_type = model_type.upper()
        self.start_date = start_date
        self.end_date = end_date or datetime.now().strftime('%Y-%m-%d')
        self.sequence_length = sequence_length
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.model = None
        self.history = None

        # Determine project root (works both locally and in Docker)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.project_root = os.path.join(script_dir, '..', '..')  # Go up from scripts/stock_prediction to jupyter root
        self.project_root = os.path.abspath(self.project_root)

        # Create models directory structure
        self.model_dir = os.path.join(self.project_root, 'models', self.ticker)
        os.makedirs(self.model_dir, exist_ok=True)

    def download_data(self, max_retries=5):
        """Download stock data from Yahoo Finance with retry logic"""
        print(f"\n{'='*60}")
        print(f"Downloading {self.ticker} stock data...")
        print(f"Period: {self.start_date} to {self.end_date}")
        print(f"Using: {'yahooquery' if USE_YAHOOQUERY else 'yfinance'}")
        print(f"{'='*60}\n")

        for attempt in range(max_retries):
            try:
                # Add delay between attempts to avoid rate limiting
                if attempt > 0:
                    wait_time = 5 * (2 ** (attempt - 1))  # Exponential backoff: 5, 10, 20, 40 seconds
                    print(f"⏳ Waiting {wait_time} seconds before retry (attempt {attempt + 1}/{max_retries})...")
                    time.sleep(wait_time)

                print(f"🔄 Attempting to download data (attempt {attempt + 1}/{max_retries})...")

                # Use yahooquery (better) or yfinance (fallback)
                if USE_YAHOOQUERY:
                    # yahooquery - more reliable
                    ticker_obj = Ticker(self.ticker)
                    df = ticker_obj.history(start=self.start_date, end=self.end_date)

                    # yahooquery returns MultiIndex, need to process
                    if isinstance(df, pd.DataFrame) and not df.empty:
                        # Reset index to get symbol and date as columns
                        df = df.reset_index()

                        # Set date as index
                        if 'date' in df.columns:
                            df.set_index('date', inplace=True)

                        # Rename columns to match yfinance format (lowercase to Title case)
                        column_mapping = {
                            'open': 'Open',
                            'high': 'High',
                            'low': 'Low',
                            'close': 'Close',
                            'volume': 'Volume',
                            'adjclose': 'Adj Close'
                        }
                        df.rename(columns=column_mapping, inplace=True)

                        # Ensure we have Close column
                        if 'Close' not in df.columns and 'close' in df.columns:
                            df['Close'] = df['close']
                    else:
                        df = pd.DataFrame()  # Empty DataFrame
                else:
                    # yfinance - fallback
                    df = yf.download(
                        self.ticker,
                        start=self.start_date,
                        end=self.end_date,
                        progress=False,
                        show_errors=False
                    )

                if df.empty:
                    print(f"⚠️  No data returned for {self.ticker}")
                    if attempt < max_retries - 1:
                        continue
                    raise ValueError(f"No data found for ticker {self.ticker} after {max_retries} attempts")

                self.df = df
                self.data = df[['Close']].values
                print(f"✅ Downloaded {len(df)} data points successfully!")
                # Handle both datetime and date objects
                start_str = df.index[0].strftime('%Y-%m-%d') if hasattr(df.index[0], 'strftime') else str(df.index[0])
                end_str = df.index[-1].strftime('%Y-%m-%d') if hasattr(df.index[-1], 'strftime') else str(df.index[-1])
                print(f"📅 Date range: {start_str} to {end_str}")
                return True

            except requests.exceptions.HTTPError as e:
                if '429' in str(e):
                    print(f"⚠️  Rate limit detected (429 error)")
                    if attempt < max_retries - 1:
                        wait_time = 10 * (2 ** attempt)  # Longer wait for rate limits: 10, 20, 40, 80 seconds
                        print(f"⏳ Rate limited. Waiting {wait_time} seconds...")
                        time.sleep(wait_time)
                        continue
                    else:
                        print(f"❌ Rate limit persists after {max_retries} attempts")
                        print("💡 Suggestion: Wait 10-15 minutes before trying again")
                        return False
                else:
                    print(f"❌ HTTP Error: {str(e)}")
                    if attempt < max_retries - 1:
                        continue
                    return False

            except Exception as e:
                error_msg = str(e)
                print(f"⚠️  Error on attempt {attempt + 1}: {error_msg}")

                # Check for common errors
                if 'delisted' in error_msg.lower():
                    print(f"❌ Ticker {self.ticker} may be delisted or invalid")
                    return False
                elif 'no timezone found' in error_msg.lower():
                    print(f"❌ Ticker {self.ticker} data unavailable or invalid")
                    return False

                if attempt < max_retries - 1:
                    print(f"🔄 Retrying...")
                    continue
                else:
                    print(f"❌ Failed after {max_retries} attempts: {error_msg}")
                    return False

        return False

    def prepare_data(self):
        """Prepare and scale data for training"""
        print("\nPreparing data...")

        # Scale data
        self.scaled_data = self.scaler.fit_transform(self.data)

        # Create sequences
        X, y = [], []
        for i in range(self.sequence_length, len(self.scaled_data)):
            X.append(self.scaled_data[i-self.sequence_length:i, 0])
            y.append(self.scaled_data[i, 0])

        X, y = np.array(X), np.array(y)
        X = np.reshape(X, (X.shape[0], X.shape[1], 1))

        # Split into train and test sets (80/20)
        train_size = int(len(X) * 0.8)
        self.X_train, self.X_test = X[:train_size], X[train_size:]
        self.y_train, self.y_test = y[:train_size], y[train_size:]

        print(f"Training samples: {len(self.X_train)}, Test samples: {len(self.X_test)}")

    def build_lstm_model(self):
        """Build LSTM model"""
        model = Sequential()
        model.add(LSTM(units=50, return_sequences=True, input_shape=(self.X_train.shape[1], 1)))
        model.add(Dropout(0.2))
        model.add(LSTM(units=50, return_sequences=False))
        model.add(Dropout(0.2))
        model.add(Dense(25))
        model.add(Dense(1))
        model.compile(optimizer='adam', loss='mean_squared_error')
        return model

    def build_gru_model(self):
        """Build GRU model"""
        model = Sequential()
        model.add(GRU(units=50, return_sequences=True, input_shape=(self.X_train.shape[1], 1)))
        model.add(Dropout(0.2))
        model.add(GRU(units=50, return_sequences=False))
        model.add(Dropout(0.2))
        model.add(Dense(25))
        model.add(Dense(1))
        model.compile(optimizer='adam', loss='mean_squared_error')
        return model

    def build_transformer_model(self):
        """Build Transformer model"""
        from tensorflow.keras.layers import Input, GlobalAveragePooling1D
        from tensorflow.keras.models import Model

        inputs = Input(shape=(self.X_train.shape[1], 1))

        # Transformer block
        attention = MultiHeadAttention(num_heads=4, key_dim=16)(inputs, inputs)
        attention = Dropout(0.2)(attention)
        attention = LayerNormalization()(inputs + attention)

        # Feed-forward network
        ffn = Dense(64, activation='relu')(attention)
        ffn = Dropout(0.2)(ffn)
        ffn = Dense(1)(ffn)
        ffn = LayerNormalization()(attention + ffn)

        # Global pooling and output
        gap = GlobalAveragePooling1D()(ffn)
        outputs = Dense(1)(gap)

        model = Model(inputs=inputs, outputs=outputs)
        model.compile(optimizer='adam', loss='mean_squared_error')
        return model

    def build_model(self):
        """Build model based on type"""
        print(f"\nBuilding {self.model_type} model...")

        if self.model_type == 'LSTM':
            self.model = self.build_lstm_model()
        elif self.model_type == 'GRU':
            self.model = self.build_gru_model()
        elif self.model_type == 'TRANSFORMER':
            self.model = self.build_transformer_model()
        else:
            raise ValueError(f"Unknown model type: {self.model_type}")

        print(f"{self.model_type} model built successfully")

    def train_model(self, epochs=20, batch_size=32):
        """Train the model"""
        print(f"\n{'='*60}")
        print(f"Training {self.model_type} model for {self.ticker}...")
        print(f"{'='*60}\n")

        # Early stopping callback
        early_stop = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

        self.history = self.model.fit(
            self.X_train,
            self.y_train,
            epochs=epochs,
            batch_size=batch_size,
            validation_split=0.1,
            verbose=1,
            callbacks=[early_stop]
        )

    def evaluate_model(self):
        """Evaluate model performance"""
        print("\nEvaluating model...")

        # Predict on test set
        predicted_test = self.model.predict(self.X_test)
        self.predicted_prices_test = self.scaler.inverse_transform(predicted_test)
        self.actual_prices_test = self.scaler.inverse_transform(self.y_test.reshape(-1, 1))

        # Calculate metrics
        rmse = np.sqrt(mean_squared_error(self.actual_prices_test, self.predicted_prices_test))
        mae = mean_absolute_error(self.actual_prices_test, self.predicted_prices_test)
        mape = mean_absolute_percentage_error(self.actual_prices_test, self.predicted_prices_test) * 100

        print(f"\n{'='*60}")
        print(f"{self.model_type} Model Performance for {self.ticker}")
        print(f"{'='*60}")
        print(f"RMSE: ${rmse:.2f}")
        print(f"MAE: ${mae:.2f}")
        print(f"MAPE: {mape:.2f}%")
        print(f"{'='*60}\n")

        self.metrics = {
            'ticker': self.ticker,
            'model': self.model_type,
            'rmse': float(rmse),
            'mae': float(mae),
            'mape': float(mape),
            'train_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'data_period': f"{self.start_date} to {self.end_date}",
            'samples': {
                'train': len(self.X_train),
                'test': len(self.X_test)
            }
        }

        return self.metrics

    def save_model(self):
        """Save model, scaler, and metrics"""
        model_name = f"{self.model_type.lower()}_{self.ticker.lower()}_model.h5"
        scaler_name = f"{self.model_type.lower()}_{self.ticker.lower()}_scaler.pkl"
        metrics_name = f"{self.model_type.lower()}_{self.ticker.lower()}_metrics.pkl"

        # Save model
        model_path = os.path.join(self.model_dir, model_name)
        self.model.save(model_path)
        print(f"Model saved to {model_path}")

        # Save scaler
        scaler_path = os.path.join(self.model_dir, scaler_name)
        with open(scaler_path, 'wb') as f:
            pickle.dump(self.scaler, f)
        print(f"Scaler saved to {scaler_path}")

        # Save metrics
        metrics_path = os.path.join(self.model_dir, metrics_name)
        with open(metrics_path, 'wb') as f:
            pickle.dump(self.metrics, f)
        print(f"Metrics saved to {metrics_path}")

    def plot_predictions(self):
        """Plot and save prediction results"""
        print("\nGenerating plots...")

        plt.figure(figsize=(14, 6))

        # Predict on train set
        predicted_train = self.model.predict(self.X_train)
        predicted_prices_train = self.scaler.inverse_transform(predicted_train)
        actual_prices_train = self.scaler.inverse_transform(self.y_train.reshape(-1, 1))

        train_dates = self.df.index[self.sequence_length:self.sequence_length+len(actual_prices_train)]
        test_dates = self.df.index[self.sequence_length+len(actual_prices_train):self.sequence_length+len(actual_prices_train)+len(self.actual_prices_test)]

        # Plot full data
        plt.subplot(1, 2, 1)
        plt.plot(train_dates, actual_prices_train, label="Train Actual", color='blue', alpha=0.6)
        plt.plot(test_dates, self.actual_prices_test, label="Test Actual", color='green', linewidth=2)
        plt.plot(test_dates, self.predicted_prices_test, label="Test Predicted", color='red', linestyle='--', linewidth=2)
        plt.title(f"{self.ticker} Stock Price: {self.model_type} Model")
        plt.xlabel("Date")
        plt.ylabel("Price (USD)")
        plt.legend()
        plt.grid(True, alpha=0.3)

        # Plot test set only (zoomed)
        plt.subplot(1, 2, 2)
        plt.plot(test_dates, self.actual_prices_test, label="Actual Price", color='green', linewidth=2)
        plt.plot(test_dates, self.predicted_prices_test, label="Predicted Price", color='red', linestyle='--', linewidth=2)
        plt.title(f"{self.model_type} Test Predictions\nRMSE: ${self.metrics['rmse']:.2f}, MAE: ${self.metrics['mae']:.2f}")
        plt.xlabel("Date")
        plt.ylabel("Price (USD)")
        plt.legend()
        plt.grid(True, alpha=0.3)

        plt.tight_layout()

        plot_path = os.path.join(self.model_dir, f"{self.model_type.lower()}_{self.ticker.lower()}_prediction.png")
        plt.savefig(plot_path, dpi=100, bbox_inches='tight')
        print(f"Plot saved to {plot_path}")
        plt.close()

    def run(self, epochs=20, batch_size=32):
        """Run complete training pipeline"""
        try:
            if not self.download_data():
                return False

            self.prepare_data()
            self.build_model()
            self.train_model(epochs=epochs, batch_size=batch_size)
            self.evaluate_model()
            self.save_model()
            self.plot_predictions()

            print(f"\n{'='*60}")
            print(f"SUCCESS: {self.model_type} model for {self.ticker} completed!")
            print(f"{'='*60}\n")
            return True

        except Exception as e:
            print(f"\n{'='*60}")
            print(f"ERROR: Training failed for {self.ticker} - {self.model_type}")
            print(f"Error: {str(e)}")
            print(f"{'='*60}\n")
            return False


def main():
    """Main function to handle CLI arguments"""
    parser = argparse.ArgumentParser(description='Train stock prediction models for multiple companies')
    parser.add_argument('--ticker', type=str, required=True, help='Stock ticker symbol (e.g., TSLA, AAPL)')
    parser.add_argument('--model', type=str, required=True, choices=['LSTM', 'GRU', 'TRANSFORMER', 'ALL'],
                       help='Model type to train')
    parser.add_argument('--start', type=str, default='2018-01-01', help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end', type=str, default=None, help='End date (YYYY-MM-DD), defaults to today')
    parser.add_argument('--epochs', type=int, default=20, help='Number of training epochs')
    parser.add_argument('--batch-size', type=int, default=32, help='Batch size for training')
    parser.add_argument('--sequence-length', type=int, default=60, help='Sequence length for time series')

    args = parser.parse_args()

    # Train all models if requested
    if args.model == 'ALL':
        models = ['LSTM', 'GRU', 'TRANSFORMER']
    else:
        models = [args.model]

    print(f"\n{'#'*60}")
    print(f"MULTI-COMPANY STOCK PREDICTION TRAINING")
    print(f"{'#'*60}")
    print(f"Ticker: {args.ticker}")
    print(f"Models: {', '.join(models)}")
    print(f"Period: {args.start} to {args.end or 'today'}")
    print(f"{'#'*60}\n")

    results = {}
    for i, model_type in enumerate(models):
        # Add delay between models to avoid rate limiting (only if not first model)
        if i > 0:
            print(f"\n⏳ Waiting 3 seconds before training next model to avoid rate limiting...")
            time.sleep(3)

        trainer = StockModelTrainer(
            ticker=args.ticker,
            model_type=model_type,
            start_date=args.start,
            end_date=args.end,
            sequence_length=args.sequence_length
        )

        success = trainer.run(epochs=args.epochs, batch_size=args.batch_size)
        results[model_type] = success

    # Print summary
    print(f"\n{'#'*60}")
    print(f"TRAINING SUMMARY FOR {args.ticker}")
    print(f"{'#'*60}")
    for model_type, success in results.items():
        status = "SUCCESS" if success else "FAILED"
        print(f"{model_type}: {status}")
    print(f"{'#'*60}\n")


if __name__ == "__main__":
    main()
