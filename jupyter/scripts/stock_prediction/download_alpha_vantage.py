"""
Alternative Stock Data Downloader using Alpha Vantage
Free tier: 25 requests/day, 5 requests/minute

Get FREE API key: https://www.alphavantage.co/support/#api-key
"""
import requests
import pandas as pd
from datetime import datetime
import time

# FREE API Key (demo - replace with your own)
# Get yours at: https://www.alphavantage.co/support/#api-key
API_KEY = "demo"  # Replace with your API key

def download_stock_data(ticker, start_date='2023-01-01', end_date=None, api_key=API_KEY):
    """
    Download stock data from Alpha Vantage

    Args:
        ticker: Stock symbol (e.g., 'AAPL', 'TSLA')
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD), default=today
        api_key: Alpha Vantage API key

    Returns:
        pandas DataFrame with OHLCV data
    """
    print(f"\n{'='*60}")
    print(f"Downloading {ticker} from Alpha Vantage...")
    print(f"Period: {start_date} to {end_date or 'today'}")
    print(f"{'='*60}\n")

    # API endpoint
    url = f"https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY_ADJUSTED",
        "symbol": ticker,
        "outputsize": "full",  # full = 20+ years
        "apikey": api_key,
        "datatype": "json"
    }

    try:
        print(f"🔄 Fetching data from Alpha Vantage...")
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()

        data = response.json()

        # Check for errors
        if "Error Message" in data:
            print(f"❌ Error: {data['Error Message']}")
            return None

        if "Note" in data:
            print(f"⚠️  API Limit: {data['Note']}")
            print("💡 Tip: Wait 1 minute or get your own API key (free!)")
            return None

        # Parse time series data
        if "Time Series (Daily)" not in data:
            print(f"❌ No data found. Response keys: {list(data.keys())}")
            return None

        time_series = data["Time Series (Daily)"]

        # Convert to DataFrame
        df = pd.DataFrame.from_dict(time_series, orient='index')
        df.index = pd.to_datetime(df.index)
        df = df.sort_index()

        # Rename columns to match yfinance format
        df.columns = ['Open', 'High', 'Low', 'Close', 'Adjusted Close', 'Volume', 'Dividend', 'Split']

        # Convert to numeric
        for col in df.columns:
            df[col] = pd.to_numeric(df[col])

        # Filter by date range
        if start_date:
            df = df[df.index >= start_date]
        if end_date:
            df = df[df.index <= end_date]

        print(f"✅ Downloaded {len(df)} data points!")
        print(f"Date range: {df.index[0].date()} to {df.index[-1].date()}")

        return df

    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {str(e)}")
        return None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None


def main():
    """Example usage"""
    import argparse

    parser = argparse.ArgumentParser(description='Download stock data from Alpha Vantage')
    parser.add_argument('--ticker', type=str, required=True, help='Stock ticker (e.g., AAPL)')
    parser.add_argument('--start', type=str, default='2023-01-01', help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end', type=str, default=None, help='End date (YYYY-MM-DD)')
    parser.add_argument('--output', type=str, default=None, help='Output CSV file path')
    parser.add_argument('--api-key', type=str, default=API_KEY, help='Alpha Vantage API key')

    args = parser.parse_args()

    # Download data
    df = download_stock_data(
        ticker=args.ticker,
        start_date=args.start,
        end_date=args.end,
        api_key=args.api_key
    )

    if df is not None and not df.empty:
        print(f"\n✅ Success!")
        print(f"\nFirst few rows:")
        print(df.head())

        print(f"\nLast few rows:")
        print(df.tail())

        # Save to CSV if requested
        if args.output:
            df.to_csv(args.output)
            print(f"\n💾 Saved to: {args.output}")
    else:
        print(f"\n❌ Failed to download data")


if __name__ == "__main__":
    main()
