"""
Multi-Company Stock Prediction Training DAG
Supports on-demand training with configurable parameters
"""
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.models import Variable
from datetime import datetime, timedelta
import json


# Default configuration for companies to train
DEFAULT_COMPANIES = ['TSLA', 'AAPL', 'GOOGL', 'MSFT', 'AMZN']
DEFAULT_MODELS = ['LSTM', 'GRU', 'TRANSFORMER']

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2026, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'multi_company_stock_training',
    default_args=default_args,
    description='Train stock prediction models for multiple companies with on-demand triggers',
    schedule_interval='0 18 * * 6',  # Run at 18:00 every Saturday (weekly training)
    catchup=False,
    tags=['ml', 'training', 'multi-company', 'stock'],
    params={
        'companies': DEFAULT_COMPANIES,  # Can override via UI
        'models': DEFAULT_MODELS,        # Can override via UI
        'start_date': '2018-01-01',      # Can override via UI
        'end_date': None,                # None = today, can override via UI
        'epochs': 20,
        'batch_size': 32,
    }
)


def check_and_install_dependencies(**context):
    """Ensure all required Python packages are installed"""
    import subprocess
    import sys

    required_packages = [
        'tensorflow==2.15.0',
        'scikit-learn==1.3.2',
        'yfinance==0.2.32',
        'pandas',
        'numpy',
        'matplotlib'
    ]

    print("Checking dependencies...")
    try:
        import tensorflow
        import sklearn
        import yfinance
        import pandas
        import numpy
        import matplotlib
        print("All dependencies are already installed!")
    except ImportError as e:
        print(f"Missing dependency: {e}")
        print("Installing required packages...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + required_packages)
        print("Dependencies installed successfully!")


def create_training_tasks(**context):
    """Dynamically create training configuration"""
    params = context['params']

    # Get companies list (can be triggered via Airflow UI with custom params)
    companies = params.get('companies', DEFAULT_COMPANIES)
    models = params.get('models', DEFAULT_MODELS)
    start_date = params.get('start_date', '2018-01-01')
    end_date = params.get('end_date', None)
    epochs = params.get('epochs', 20)
    batch_size = params.get('batch_size', 32)

    if isinstance(companies, str):
        companies = [c.strip() for c in companies.split(',')]
    if isinstance(models, str):
        models = [m.strip() for m in models.split(',')]

    print("=" * 60)
    print("TRAINING CONFIGURATION")
    print("=" * 60)
    print(f"Companies: {', '.join(companies)}")
    print(f"Models: {', '.join(models)}")
    print(f"Period: {start_date} to {end_date or 'today'}")
    print(f"Epochs: {epochs}")
    print(f"Batch Size: {batch_size}")
    print("=" * 60)

    # Store config for downstream tasks
    ti = context['ti']
    ti.xcom_push(key='companies', value=companies)
    ti.xcom_push(key='models', value=models)
    ti.xcom_push(key='start_date', value=start_date)
    ti.xcom_push(key='end_date', value=end_date or '')
    ti.xcom_push(key='epochs', value=epochs)
    ti.xcom_push(key='batch_size', value=batch_size)


def train_company_model(**context):
    """Train models for a specific company"""
    import subprocess
    import os

    ti = context['ti']
    ticker = context['params']['ticker']
    model_type = context['params']['model_type']

    # Get config from XCom
    start_date = ti.xcom_pull(key='start_date', task_ids='create_training_config')
    end_date = ti.xcom_pull(key='end_date', task_ids='create_training_config')
    epochs = ti.xcom_pull(key='epochs', task_ids='create_training_config')
    batch_size = ti.xcom_pull(key='batch_size', task_ids='create_training_config')

    # Build command
    cmd = [
        'python',
        '/opt/airflow/work/scripts/stock_prediction/train_multi_company.py',
        '--ticker', ticker,
        '--model', model_type,
        '--start', start_date,
        '--epochs', str(epochs),
        '--batch-size', str(batch_size),
    ]

    if end_date:
        cmd.extend(['--end', end_date])

    print(f"Executing: {' '.join(cmd)}")

    # Change to work directory
    os.chdir('/opt/airflow/work')

    # Run training
    result = subprocess.run(cmd, capture_output=True, text=True)

    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)

    if result.returncode != 0:
        raise Exception(f"Training failed for {ticker} - {model_type}")

    return f"{ticker}_{model_type}_SUCCESS"


def generate_summary_report(**context):
    """Generate training summary report"""
    ti = context['ti']
    companies = ti.xcom_pull(key='companies', task_ids='create_training_config')
    models = ti.xcom_pull(key='models', task_ids='create_training_config')

    print("\n" + "=" * 80)
    print("MULTI-COMPANY TRAINING SUMMARY")
    print("=" * 80)
    print(f"Execution Date: {context['execution_date']}")
    print(f"Companies Trained: {', '.join(companies)}")
    print(f"Models per Company: {', '.join(models)}")
    print(f"Total Models Trained: {len(companies) * len(models)}")
    print("=" * 80)

    # List all generated models
    import os
    models_dir = '/opt/airflow/work/models'
    if os.path.exists(models_dir):
        print("\nGenerated Models:")
        for company in companies:
            company_dir = os.path.join(models_dir, company)
            if os.path.exists(company_dir):
                print(f"\n{company}:")
                for file in sorted(os.listdir(company_dir)):
                    if file.endswith('.h5'):
                        file_path = os.path.join(company_dir, file)
                        size_mb = os.path.getsize(file_path) / (1024 * 1024)
                        print(f"  - {file} ({size_mb:.2f} MB)")
    print("=" * 80 + "\n")


# Task 0: Check dependencies
check_deps = PythonOperator(
    task_id='check_dependencies',
    python_callable=check_and_install_dependencies,
    provide_context=True,
    dag=dag,
)

# Task 1: Create training configuration
create_config = PythonOperator(
    task_id='create_training_config',
    python_callable=create_training_tasks,
    provide_context=True,
    dag=dag,
)

# Task 2: Train TSLA models (default example)
train_tsla_lstm = PythonOperator(
    task_id='train_TSLA_LSTM',
    python_callable=train_company_model,
    params={'ticker': 'TSLA', 'model_type': 'LSTM'},
    provide_context=True,
    dag=dag,
)

train_tsla_gru = PythonOperator(
    task_id='train_TSLA_GRU',
    python_callable=train_company_model,
    params={'ticker': 'TSLA', 'model_type': 'GRU'},
    provide_context=True,
    dag=dag,
)

train_tsla_transformer = PythonOperator(
    task_id='train_TSLA_TRANSFORMER',
    python_callable=train_company_model,
    params={'ticker': 'TSLA', 'model_type': 'TRANSFORMER'},
    provide_context=True,
    dag=dag,
)

# Task 3: Train AAPL models
train_aapl_lstm = PythonOperator(
    task_id='train_AAPL_LSTM',
    python_callable=train_company_model,
    params={'ticker': 'AAPL', 'model_type': 'LSTM'},
    provide_context=True,
    dag=dag,
)

train_aapl_gru = PythonOperator(
    task_id='train_AAPL_GRU',
    python_callable=train_company_model,
    params={'ticker': 'AAPL', 'model_type': 'GRU'},
    provide_context=True,
    dag=dag,
)

train_aapl_transformer = PythonOperator(
    task_id='train_AAPL_TRANSFORMER',
    python_callable=train_company_model,
    params={'ticker': 'AAPL', 'model_type': 'TRANSFORMER'},
    provide_context=True,
    dag=dag,
)

# Task 4: Train GOOGL models
train_googl_lstm = PythonOperator(
    task_id='train_GOOGL_LSTM',
    python_callable=train_company_model,
    params={'ticker': 'GOOGL', 'model_type': 'LSTM'},
    provide_context=True,
    dag=dag,
)

train_googl_gru = PythonOperator(
    task_id='train_GOOGL_GRU',
    python_callable=train_company_model,
    params={'ticker': 'GOOGL', 'model_type': 'GRU'},
    provide_context=True,
    dag=dag,
)

train_googl_transformer = PythonOperator(
    task_id='train_GOOGL_TRANSFORMER',
    python_callable=train_company_model,
    params={'ticker': 'GOOGL', 'model_type': 'TRANSFORMER'},
    provide_context=True,
    dag=dag,
)

# Task 5: Generate summary
generate_summary = PythonOperator(
    task_id='generate_summary_report',
    python_callable=generate_summary_report,
    provide_context=True,
    dag=dag,
)

# Define task dependencies
check_deps >> create_config

# TSLA models run in parallel after config
create_config >> [train_tsla_lstm, train_tsla_gru, train_tsla_transformer]

# AAPL models run in parallel
create_config >> [train_aapl_lstm, train_aapl_gru, train_aapl_transformer]

# GOOGL models run in parallel
create_config >> [train_googl_lstm, train_googl_gru, train_googl_transformer]

# All training tasks must complete before summary
[
    train_tsla_lstm, train_tsla_gru, train_tsla_transformer,
    train_aapl_lstm, train_aapl_gru, train_aapl_transformer,
    train_googl_lstm, train_googl_gru, train_googl_transformer
] >> generate_summary
