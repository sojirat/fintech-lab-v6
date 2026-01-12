"""
Compare All Trained Models - Enhanced Version
Shows detailed comparison with rankings and recommendations
"""
import os
import sys
import pickle
import pandas as pd
import matplotlib.pyplot as plt
import argparse

# Add current directory to path for relative imports
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(script_dir, '..', '..')
project_root = os.path.abspath(project_root)
os.chdir(project_root)


def load_metrics(ticker, model_type):
    """Load metrics for a specific ticker and model"""
    metrics_path = f"models/{ticker}/{model_type.lower()}_{ticker.lower()}_metrics.pkl"

    if os.path.exists(metrics_path):
        with open(metrics_path, 'rb') as f:
            return pickle.load(f)
    return None


def compare_ticker_models(ticker):
    """Compare all models for a specific ticker"""
    print(f"\n{'='*80}")
    print(f"MODEL COMPARISON FOR {ticker}")
    print(f"{'='*80}\n")

    models = ['LSTM', 'GRU', 'TRANSFORMER']
    results = []

    for model in models:
        metrics = load_metrics(ticker, model)
        if metrics:
            results.append({
                'Model': model,
                'RMSE': metrics['rmse'],
                'MAE': metrics['mae'],
                'MAPE': metrics['mape'],
                'Trained': metrics.get('train_date', 'Unknown'),
                'Train Samples': metrics['samples']['train'],
                'Test Samples': metrics['samples']['test']
            })

    if not results:
        print(f"❌ No trained models found for {ticker}")
        print(f"Train models first: make train-{ticker.lower()}")
        return None

    # Create DataFrame
    df = pd.DataFrame(results)

    # Display full comparison
    print("📊 PERFORMANCE METRICS:")
    print("-" * 80)
    print(df.to_string(index=False))
    print("-" * 80)

    # Rankings
    print("\n🏆 RANKINGS:")
    print("-" * 80)

    # Best RMSE (lower is better)
    best_rmse_idx = df['RMSE'].idxmin()
    best_rmse = df.loc[best_rmse_idx]
    print(f"Best RMSE:  {best_rmse['Model']} (${best_rmse['RMSE']:.2f})")

    # Best MAE (lower is better)
    best_mae_idx = df['MAE'].idxmin()
    best_mae = df.loc[best_mae_idx]
    print(f"Best MAE:   {best_mae['Model']} (${best_mae['MAE']:.2f})")

    # Best MAPE (lower is better)
    best_mape_idx = df['MAPE'].idxmin()
    best_mape = df.loc[best_mape_idx]
    print(f"Best MAPE:  {best_mape['Model']} ({best_mape['MAPE']:.2f}%)")

    # Overall ranking (average rank across all metrics)
    df['RMSE_Rank'] = df['RMSE'].rank()
    df['MAE_Rank'] = df['MAE'].rank()
    df['MAPE_Rank'] = df['MAPE'].rank()
    df['Avg_Rank'] = (df['RMSE_Rank'] + df['MAE_Rank'] + df['MAPE_Rank']) / 3
    df = df.sort_values('Avg_Rank')

    print("\n📈 OVERALL RANKING (Average across all metrics):")
    print("-" * 80)
    for idx, row in df.iterrows():
        stars = '⭐' * (4 - int(row['Avg_Rank']))
        print(f"{int(row['Avg_Rank'])}. {row['Model']:12} {stars}")
    print("-" * 80)

    # Recommendation
    best_overall = df.iloc[0]
    print(f"\n💡 RECOMMENDATION:")
    print(f"   Use {best_overall['Model']} model for {ticker}")
    print(f"   - Best overall performance (Avg Rank: {best_overall['Avg_Rank']:.2f})")
    print(f"   - RMSE: ${best_overall['RMSE']:.2f}")
    print(f"   - MAE: ${best_overall['MAE']:.2f}")
    print(f"   - MAPE: {best_overall['MAPE']:.2f}%")

    # Performance difference
    if len(results) > 1:
        print(f"\n📊 PERFORMANCE DIFFERENCES:")
        print("-" * 80)
        worst = df.iloc[-1]
        rmse_diff = ((worst['RMSE'] - best_overall['RMSE']) / best_overall['RMSE']) * 100
        mae_diff = ((worst['MAE'] - best_overall['MAE']) / best_overall['MAE']) * 100
        mape_diff = ((worst['MAPE'] - best_overall['MAPE']) / best_overall['MAPE']) * 100

        print(f"Best vs Worst model:")
        print(f"  RMSE difference: {rmse_diff:.1f}%")
        print(f"  MAE difference:  {mae_diff:.1f}%")
        print(f"  MAPE difference: {mape_diff:.1f}%")

    print(f"\n{'='*80}\n")

    return df


def plot_comparison(ticker, df):
    """Create visualization comparing models"""
    if df is None or df.empty:
        return

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle(f'{ticker} Model Comparison', fontsize=16, fontweight='bold')

    metrics = ['RMSE', 'MAE', 'MAPE']
    colors = ['#3498db', '#e74c3c', '#2ecc71']

    for idx, (ax, metric, color) in enumerate(zip(axes, metrics, colors)):
        values = df[metric].values
        models = df['Model'].values

        bars = ax.bar(models, values, color=color, alpha=0.7, edgecolor='black')

        # Highlight best model
        best_idx = values.argmin()
        bars[best_idx].set_color('#f39c12')
        bars[best_idx].set_alpha(1.0)
        bars[best_idx].set_linewidth(3)

        ax.set_ylabel(metric, fontsize=12, fontweight='bold')
        ax.set_title(f'{metric} Comparison', fontsize=12)
        ax.grid(axis='y', alpha=0.3)

        # Add value labels on bars
        for bar, value in zip(bars, values):
            height = bar.get_height()
            label = f'${value:.2f}' if metric != 'MAPE' else f'{value:.2f}%'
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   label, ha='center', va='bottom', fontsize=10, fontweight='bold')

    plt.tight_layout()

    # Save plot
    plot_path = f"models/{ticker}/comparison_{ticker.lower()}.png"
    plt.savefig(plot_path, dpi=150, bbox_inches='tight')
    print(f"📊 Comparison plot saved to: {plot_path}")
    plt.close()


def compare_all_tickers():
    """Compare models across all trained tickers"""
    models_dir = "models"

    if not os.path.exists(models_dir):
        print("❌ No models directory found")
        return

    tickers = [d for d in os.listdir(models_dir)
               if os.path.isdir(os.path.join(models_dir, d))]

    if not tickers:
        print("❌ No trained models found")
        print("Train models first: make train-tech")
        return

    print(f"\n{'#'*80}")
    print(f"COMPARING ALL TRAINED MODELS")
    print(f"Found {len(tickers)} ticker(s): {', '.join(tickers)}")
    print(f"{'#'*80}")

    all_results = {}

    for ticker in sorted(tickers):
        df = compare_ticker_models(ticker)
        if df is not None:
            all_results[ticker] = df
            plot_comparison(ticker, df)

    # Summary across all tickers
    if all_results:
        print(f"\n{'='*80}")
        print("SUMMARY ACROSS ALL TICKERS")
        print(f"{'='*80}\n")

        summary = []
        for ticker, df in all_results.items():
            best = df.iloc[0]
            summary.append({
                'Ticker': ticker,
                'Best Model': best['Model'],
                'RMSE': f"${best['RMSE']:.2f}",
                'MAE': f"${best['MAE']:.2f}",
                'MAPE': f"{best['MAPE']:.2f}%"
            })

        summary_df = pd.DataFrame(summary)
        print(summary_df.to_string(index=False))
        print(f"\n{'='*80}\n")


def main():
    parser = argparse.ArgumentParser(description='Compare trained stock prediction models')
    parser.add_argument('--ticker', type=str, default=None,
                       help='Specific ticker to compare (e.g., AAPL). If not specified, compares all.')

    args = parser.parse_args()

    if args.ticker:
        df = compare_ticker_models(args.ticker.upper())
        if df is not None:
            plot_comparison(args.ticker.upper(), df)
    else:
        compare_all_tickers()


if __name__ == "__main__":
    main()
