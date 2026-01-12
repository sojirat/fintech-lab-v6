"""
Future Stock Price Prediction Script
Predict future prices with flexible time periods: day, week, month, year
"""
import numpy as np
import pandas as pd
import pickle
import os
import sys
import argparse
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model

# Add current directory to path
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(script_dir, '..', '..')
project_root = os.path.abspath(project_root)
os.chdir(project_root)

# Import data download function
try:
    from yahooquery import Ticker
    USE_YAHOOQUERY = True
except ImportError:
    import yfinance as yf
    USE_YAHOOQUERY = False


class StockPredictor:
    """Predict future stock prices using trained models"""

    def __init__(self, ticker, model_type='GRU'):
        self.ticker = ticker.upper()
        self.model_type = model_type.upper()
        self.model_dir = os.path.join('models', self.ticker)

        # Load model, scaler, and metrics
        self.load_artifacts()

    def load_artifacts(self):
        """Load trained model, scaler, and metrics"""
        model_name = f"{self.model_type.lower()}_{self.ticker.lower()}_model.h5"
        scaler_name = f"{self.model_type.lower()}_{self.ticker.lower()}_scaler.pkl"
        metrics_name = f"{self.model_type.lower()}_{self.ticker.lower()}_metrics.pkl"

        model_path = os.path.join(self.model_dir, model_name)
        scaler_path = os.path.join(self.model_dir, scaler_name)
        metrics_path = os.path.join(self.model_dir, metrics_name)

        # Check if files exist
        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"❌ Model not found: {model_path}\n"
                f"Train first: make train-{self.ticker.lower()}"
            )

        print(f"\n{'='*60}")
        print(f"Loading {self.model_type} model for {self.ticker}")
        print(f"{'='*60}\n")

        # Load model
        self.model = load_model(model_path)
        print(f"✅ Model loaded: {model_name}")

        # Load scaler
        with open(scaler_path, 'rb') as f:
            self.scaler = pickle.load(f)
        print(f"✅ Scaler loaded: {scaler_name}")

        # Load metrics
        with open(metrics_path, 'rb') as f:
            self.metrics = pickle.load(f)
        print(f"✅ Metrics loaded: {metrics_name}")

        print(f"\n📊 Model Performance:")
        print(f"   RMSE: ${self.metrics['rmse']:.2f}")
        print(f"   MAE:  ${self.metrics['mae']:.2f}")
        print(f"   MAPE: {self.metrics['mape']:.2f}%")
        print(f"   Trained: {self.metrics.get('train_date', 'Unknown')}")

    def download_recent_data(self, days=100):
        """Download recent stock data for prediction"""
        print(f"\n{'='*60}")
        print(f"Downloading recent data for {self.ticker}")
        print(f"{'='*60}\n")

        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        try:
            if USE_YAHOOQUERY:
                ticker_obj = Ticker(self.ticker)
                df = ticker_obj.history(start=start_date.strftime('%Y-%m-%d'),
                                       end=end_date.strftime('%Y-%m-%d'))

                if isinstance(df, pd.DataFrame) and not df.empty:
                    df = df.reset_index()
                    if 'date' in df.columns:
                        df.set_index('date', inplace=True)
                    column_mapping = {
                        'open': 'Open', 'high': 'High', 'low': 'Low',
                        'close': 'Close', 'volume': 'Volume', 'adjclose': 'Adj Close'
                    }
                    df.rename(columns=column_mapping, inplace=True)
                    if 'Close' not in df.columns and 'close' in df.columns:
                        df['Close'] = df['close']
                else:
                    df = pd.DataFrame()
            else:
                df = yf.download(self.ticker,
                               start=start_date.strftime('%Y-%m-%d'),
                               end=end_date.strftime('%Y-%m-%d'),
                               progress=False)

            if df.empty:
                raise ValueError(f"No data downloaded for {self.ticker}")

            self.recent_data = df[['Close']].values
            self.recent_dates = df.index

            print(f"✅ Downloaded {len(df)} data points")
            print(f"📅 Latest date: {df.index[-1].strftime('%Y-%m-%d')}")
            print(f"💰 Latest price: ${df['Close'].iloc[-1]:.2f}")

            return df

        except Exception as e:
            print(f"❌ Error downloading data: {str(e)}")
            raise

    def predict_future(self, periods, period_type='day'):
        """
        Predict future prices

        Args:
            periods: Number of periods to predict
            period_type: 'day', 'week', 'month', 'year'

        Returns:
            DataFrame with predictions
        """
        # Calculate number of days
        days_map = {
            'day': 1,
            'week': 7,
            'month': 30,
            'year': 365
        }

        if period_type not in days_map:
            raise ValueError(f"Invalid period_type: {period_type}. Use: day, week, month, year")

        total_days = periods * days_map[period_type]

        # For trading days (markets closed on weekends)
        trading_days = int(total_days * 5/7)  # Approximate trading days

        print(f"\n{'='*60}")
        print(f"PREDICTING FUTURE PRICES")
        print(f"{'='*60}")
        print(f"Periods: {periods} {period_type}(s)")
        print(f"Total days: ~{total_days} days (~{trading_days} trading days)")
        print(f"{'='*60}\n")

        # Use last 60 days for prediction (sequence_length)
        sequence_length = 60
        if len(self.recent_data) < sequence_length:
            raise ValueError(f"Need at least {sequence_length} days of data. Got {len(self.recent_data)}")

        # Scale data
        scaled_data = self.scaler.transform(self.recent_data)

        # Prepare for prediction
        predictions = []
        current_sequence = scaled_data[-sequence_length:].copy()

        # Predict iteratively
        print("🔮 Generating predictions...")
        for i in range(trading_days):
            # Reshape for model input
            X_pred = current_sequence.reshape(1, sequence_length, 1)

            # Predict next day
            pred_scaled = self.model.predict(X_pred, verbose=0)
            pred_price = self.scaler.inverse_transform(pred_scaled)[0][0]

            predictions.append(pred_price)

            # Update sequence (rolling window)
            current_sequence = np.append(current_sequence[1:], pred_scaled, axis=0)

            if (i + 1) % 20 == 0:
                print(f"   Predicted {i + 1}/{trading_days} days...")

        print(f"✅ Prediction complete!\n")

        # Create prediction DataFrame
        last_date = self.recent_dates[-1]
        future_dates = pd.bdate_range(start=last_date + timedelta(days=1),
                                     periods=trading_days)

        pred_df = pd.DataFrame({
            'Date': future_dates,
            'Predicted_Price': predictions
        })
        pred_df.set_index('Date', inplace=True)

        return pred_df

    def plot_predictions(self, pred_df, show_history_days=60):
        """Plot historical data and predictions"""
        print("📊 Creating visualization...\n")

        fig, ax = plt.subplots(figsize=(16, 8))

        # Historical data (last N days)
        hist_data = pd.DataFrame({
            'Date': self.recent_dates[-show_history_days:],
            'Price': self.recent_data[-show_history_days:].flatten()
        }).set_index('Date')

        # Plot historical
        ax.plot(hist_data.index, hist_data['Price'],
               label='Historical Price', color='#2c3e50', linewidth=2)

        # Plot predictions
        ax.plot(pred_df.index, pred_df['Predicted_Price'],
               label='Predicted Price', color='#e74c3c', linewidth=2, linestyle='--')

        # Mark the transition point
        last_actual_price = hist_data['Price'].iloc[-1]
        first_pred_price = pred_df['Predicted_Price'].iloc[0]
        ax.plot([hist_data.index[-1], pred_df.index[0]],
               [last_actual_price, first_pred_price],
               color='#f39c12', linewidth=2, linestyle=':')

        # Styling
        ax.set_title(f'{self.ticker} Stock Price Prediction ({self.model_type} Model)',
                    fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Date', fontsize=12, fontweight='bold')
        ax.set_ylabel('Price (USD)', fontsize=12, fontweight='bold')
        ax.legend(loc='best', fontsize=11)
        ax.grid(True, alpha=0.3)

        # Add annotations
        last_price = hist_data['Price'].iloc[-1]
        final_pred = pred_df['Predicted_Price'].iloc[-1]
        change = final_pred - last_price
        change_pct = (change / last_price) * 100

        info_text = f"Latest: ${last_price:.2f}\n"
        info_text += f"Predicted: ${final_pred:.2f}\n"
        info_text += f"Change: ${change:+.2f} ({change_pct:+.2f}%)"

        ax.text(0.02, 0.98, info_text, transform=ax.transAxes,
               fontsize=11, verticalalignment='top',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

        plt.tight_layout()

        # Save plot
        plot_name = f"{self.model_type.lower()}_{self.ticker.lower()}_future_prediction.png"
        plot_path = os.path.join(self.model_dir, plot_name)
        plt.savefig(plot_path, dpi=150, bbox_inches='tight')
        print(f"💾 Plot saved: {plot_path}")

        return plot_path

    def display_summary(self, pred_df):
        """Display prediction summary"""
        print(f"\n{'='*60}")
        print(f"PREDICTION SUMMARY")
        print(f"{'='*60}\n")

        current_price = self.recent_data[-1][0]
        first_pred = pred_df['Predicted_Price'].iloc[0]
        final_pred = pred_df['Predicted_Price'].iloc[-1]

        total_change = final_pred - current_price
        total_change_pct = (total_change / current_price) * 100

        print(f"📍 Current Price:    ${current_price:.2f}")
        print(f"📅 Current Date:     {self.recent_dates[-1].strftime('%Y-%m-%d')}")
        print(f"\n🔮 First Prediction: ${first_pred:.2f}")
        print(f"📅 Prediction Start: {pred_df.index[0].strftime('%Y-%m-%d')}")
        print(f"\n🎯 Final Prediction: ${final_pred:.2f}")
        print(f"📅 Prediction End:   {pred_df.index[-1].strftime('%Y-%m-%d')}")
        print(f"\n📈 Expected Change:  ${total_change:+.2f} ({total_change_pct:+.2f}%)")

        if total_change > 0:
            print(f"🟢 Trend: BULLISH (Upward)")
        else:
            print(f"🔴 Trend: BEARISH (Downward)")

        # Show first and last 5 predictions
        print(f"\n📊 First 5 Predictions:")
        print("-" * 60)
        for i in range(min(5, len(pred_df))):
            date = pred_df.index[i].strftime('%Y-%m-%d')
            price = pred_df['Predicted_Price'].iloc[i]
            change = price - current_price
            change_pct = (change / current_price) * 100
            print(f"   {date}: ${price:.2f} ({change:+.2f}, {change_pct:+.2f}%)")

        if len(pred_df) > 10:
            print(f"\n   ... ({len(pred_df) - 10} more predictions) ...\n")

            print(f"📊 Last 5 Predictions:")
            print("-" * 60)
            for i in range(max(0, len(pred_df) - 5), len(pred_df)):
                date = pred_df.index[i].strftime('%Y-%m-%d')
                price = pred_df['Predicted_Price'].iloc[i]
                change = price - current_price
                change_pct = (change / current_price) * 100
                print(f"   {date}: ${price:.2f} ({change:+.2f}, {change_pct:+.2f}%)")

        print(f"\n{'='*60}")

        # Warning
        print(f"\n⚠️  DISCLAIMER:")
        print(f"   This is a prediction based on historical data.")
        print(f"   Model Accuracy: RMSE ${self.metrics['rmse']:.2f}, MAPE {self.metrics['mape']:.2f}%")
        print(f"   Actual prices may vary significantly.")
        print(f"   Not financial advice. Do your own research!")
        print(f"{'='*60}\n")


def main():
    parser = argparse.ArgumentParser(description='Predict future stock prices')
    parser.add_argument('--ticker', type=str, required=True,
                       help='Stock ticker (e.g., AAPL, TSLA)')
    parser.add_argument('--model', type=str, default='GRU',
                       choices=['LSTM', 'GRU', 'TRANSFORMER'],
                       help='Model type to use (default: GRU - best performer)')
    parser.add_argument('--periods', type=int, default=30,
                       help='Number of periods to predict (default: 30)')
    parser.add_argument('--period-type', type=str, default='day',
                       choices=['day', 'week', 'month', 'year'],
                       help='Period type: day, week, month, year (default: day)')
    parser.add_argument('--save-csv', type=str, default=None,
                       help='Save predictions to CSV file')

    args = parser.parse_args()

    try:
        # Initialize predictor
        predictor = StockPredictor(ticker=args.ticker, model_type=args.model)

        # Download recent data
        predictor.download_recent_data(days=100)

        # Predict future
        pred_df = predictor.predict_future(periods=args.periods,
                                          period_type=args.period_type)

        # Display summary
        predictor.display_summary(pred_df)

        # Plot
        predictor.plot_predictions(pred_df)

        # Save to CSV if requested
        if args.save_csv:
            pred_df.to_csv(args.save_csv)
            print(f"💾 Predictions saved to: {args.save_csv}\n")

        print("✅ Prediction completed successfully!\n")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}\n")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
