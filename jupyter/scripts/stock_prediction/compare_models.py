import pickle
import pandas as pd
import matplotlib.pyplot as plt
import os

# Determine project root (works both locally and in Docker)
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(script_dir, '..', '..')  # Go up from scripts/stock_prediction to jupyter root
project_root = os.path.abspath(project_root)
os.chdir(project_root)

# Load metrics from all models
models_dir = 'models'

metrics_data = []

model_files = ['lstm_metrics.pkl', 'gru_metrics.pkl', 'transformer_metrics.pkl']

for model_file in model_files:
    filepath = os.path.join(models_dir, model_file)
    if os.path.exists(filepath):
        with open(filepath, 'rb') as f:
            metrics = pickle.load(f)
            metrics_data.append(metrics)
    else:
        print(f"Warning: {model_file} not found. Please train the model first.")

if not metrics_data:
    print("No metrics found. Please train the models first.")
    exit()

# Create comparison dataframe
df_metrics = pd.DataFrame(metrics_data)
print("\n" + "="*60)
print("MODEL COMPARISON - TSLA Stock Price Prediction")
print("="*60)
print(df_metrics.to_string(index=False))
print("="*60)

# Find best model
best_rmse = df_metrics.loc[df_metrics['rmse'].idxmin()]
best_mae = df_metrics.loc[df_metrics['mae'].idxmin()]
best_mape = df_metrics.loc[df_metrics['mape'].idxmin()]

print("\n" + "="*60)
print("BEST MODELS BY METRIC")
print("="*60)
print(f"Best RMSE: {best_rmse['model']} (${best_rmse['rmse']:.2f})")
print(f"Best MAE:  {best_mae['model']} (${best_mae['mae']:.2f})")
print(f"Best MAPE: {best_mape['model']} ({best_mape['mape']:.2f}%)")
print("="*60)

# Calculate overall best model (average rank)
df_metrics['rmse_rank'] = df_metrics['rmse'].rank()
df_metrics['mae_rank'] = df_metrics['mae'].rank()
df_metrics['mape_rank'] = df_metrics['mape'].rank()
df_metrics['avg_rank'] = (df_metrics['rmse_rank'] + df_metrics['mae_rank'] + df_metrics['mape_rank']) / 3

overall_best = df_metrics.loc[df_metrics['avg_rank'].idxmin()]
print(f"\n🏆 OVERALL BEST MODEL: {overall_best['model']} (Avg Rank: {overall_best['avg_rank']:.2f})")

# Plot comparison
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# RMSE comparison
axes[0].bar(df_metrics['model'], df_metrics['rmse'], color=['#1f77b4', '#ff7f0e', '#2ca02c'])
axes[0].set_title('RMSE Comparison\n(Lower is Better)', fontweight='bold')
axes[0].set_ylabel('RMSE (USD)')
axes[0].set_xlabel('Model')
axes[0].grid(True, alpha=0.3, axis='y')
for i, v in enumerate(df_metrics['rmse']):
    axes[0].text(i, v + 0.5, f'${v:.2f}', ha='center', va='bottom', fontweight='bold')

# MAE comparison
axes[1].bar(df_metrics['model'], df_metrics['mae'], color=['#1f77b4', '#ff7f0e', '#2ca02c'])
axes[1].set_title('MAE Comparison\n(Lower is Better)', fontweight='bold')
axes[1].set_ylabel('MAE (USD)')
axes[1].set_xlabel('Model')
axes[1].grid(True, alpha=0.3, axis='y')
for i, v in enumerate(df_metrics['mae']):
    axes[1].text(i, v + 0.5, f'${v:.2f}', ha='center', va='bottom', fontweight='bold')

# MAPE comparison
axes[2].bar(df_metrics['model'], df_metrics['mape'], color=['#1f77b4', '#ff7f0e', '#2ca02c'])
axes[2].set_title('MAPE Comparison\n(Lower is Better)', fontweight='bold')
axes[2].set_ylabel('MAPE (%)')
axes[2].set_xlabel('Model')
axes[2].grid(True, alpha=0.3, axis='y')
for i, v in enumerate(df_metrics['mape']):
    axes[2].text(i, v + 0.1, f'{v:.2f}%', ha='center', va='bottom', fontweight='bold')

plt.suptitle(f'TSLA Stock Prediction Model Comparison\n🏆 Best Overall: {overall_best["model"]}',
             fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(models_dir, 'model_comparison.png'), dpi=100, bbox_inches='tight')
print(f"\nComparison plot saved to {os.path.join(models_dir, 'model_comparison.png')}")
plt.show()

# Save comparison results
comparison_results = {
    'metrics': df_metrics[['model', 'rmse', 'mae', 'mape', 'avg_rank']].to_dict('records'),
    'best_overall': overall_best['model'],
    'best_rmse': best_rmse['model'],
    'best_mae': best_mae['model'],
    'best_mape': best_mape['model']
}

with open(os.path.join(models_dir, 'comparison_results.pkl'), 'wb') as f:
    pickle.dump(comparison_results, f)

print("\nComparison results saved!")
