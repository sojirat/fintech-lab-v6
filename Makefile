.PHONY: help all build up down restart logs clean train-tsla train-aapl train-googl train-all-stocks airflow-trigger test check-syntax

# Variables
COMPOSE := docker compose
JUPYTER_EXEC := $(COMPOSE) exec jupyterlab
AIRFLOW_EXEC := $(COMPOSE) exec airflow

# Colors for output
GREEN := \033[0;32m
YELLOW := \033[1;33m
RED := \033[0;31m
NC := \033[0m # No Color

##@ Help

help: ## Display this help
	@echo "$(GREEN)╔═══════════════════════════════════════════════════════════╗$(NC)"
	@echo "$(GREEN)║   Fintech Lab v6 - Multi-Company Stock Prediction       ║$(NC)"
	@echo "$(GREEN)╚═══════════════════════════════════════════════════════════╝$(NC)"
	@echo ""
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make $(YELLOW)<target>$(NC)\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2 } /^##@/ { printf "\n$(YELLOW)%s$(NC)\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
	@echo ""

##@ Quick Start (All-in-One)

all: down build-fast up wait check ## 🚀 Do everything: stop old containers, build (with cache), start, wait, and check status

quick-start: all ## 🚀 Alias for 'all' - complete setup in one command

fresh-start: clean-docker build-fast up wait check ## 🔄 Fresh start: clean Docker, rebuild (with cache), and start

fresh-start-full: clean-docker build up wait check ## 🔄 Fresh start full: clean Docker, rebuild (no cache), and start

network-fix: pull-base-image build-fast up wait check ## 🌐 Fix network issues: pull base image first, then build

##@ Docker Management

build: ## 🔨 Build all Docker images (especially custom JupyterLab)
	@echo "$(GREEN)Building Docker images...$(NC)"
	@for i in 1 2 3; do \
		echo "$(YELLOW)Attempt $$i/3...$(NC)"; \
		$(COMPOSE) build --no-cache jupyterlab && break || \
		(echo "$(RED)Build failed, retrying in 5 seconds...$(NC)" && sleep 5); \
	done
	@echo "$(GREEN)✓ Build complete!$(NC)"

build-fast: ## ⚡ Build with cache (faster)
	@echo "$(GREEN)Building Docker images with cache...$(NC)"
	@for i in 1 2 3; do \
		echo "$(YELLOW)Attempt $$i/3...$(NC)"; \
		$(COMPOSE) build jupyterlab && break || \
		(echo "$(RED)Build failed, retrying in 5 seconds...$(NC)" && sleep 5); \
	done
	@echo "$(GREEN)✓ Build complete!$(NC)"

build-offline: ## 🔌 Build using existing local image (no pull)
	@echo "$(YELLOW)Building offline (using cached base image)...$(NC)"
	DOCKER_BUILDKIT=1 $(COMPOSE) build --build-arg BUILDKIT_INLINE_CACHE=1 jupyterlab
	@echo "$(GREEN)✓ Offline build complete!$(NC)"

up: ## ⬆️  Start all services
	@echo "$(GREEN)Starting all services...$(NC)"
	$(COMPOSE) up -d
	@echo "$(GREEN)✓ Services started!$(NC)"

down: ## ⬇️  Stop all services
	@echo "$(YELLOW)Stopping all services...$(NC)"
	$(COMPOSE) down
	@echo "$(YELLOW)✓ Services stopped!$(NC)"

restart: down up ## 🔄 Restart all services
	@echo "$(GREEN)✓ Services restarted!$(NC)"

ps: ## 📋 Show running containers
	@$(COMPOSE) ps

logs: ## 📜 Show logs (all services)
	$(COMPOSE) logs -f

logs-jupyter: ## 📜 Show JupyterLab logs only
	$(COMPOSE) logs -f jupyterlab

logs-airflow: ## 📜 Show Airflow logs only
	$(COMPOSE) logs -f airflow

logs-fastapi: ## 📜 Show FastAPI logs only
	$(COMPOSE) logs -f fastapi

##@ Initialization & Checks

wait: ## ⏳ Wait for services to be ready (30 seconds)
	@echo "$(YELLOW)Waiting for services to initialize...$(NC)"
	@sleep 30
	@echo "$(GREEN)✓ Services should be ready now!$(NC)"

check: ## ✅ Check if all services are running
	@echo "$(GREEN)Checking service status...$(NC)"
	@$(COMPOSE) ps
	@echo ""
	@echo "$(GREEN)Service URLs:$(NC)"
	@echo "  • JupyterLab:  $(YELLOW)http://localhost:8888$(NC)  (Token: fintech2025)"
	@echo "  • Airflow:     $(YELLOW)http://localhost:8083$(NC)  (admin/fintech2025)"
	@echo "  • FastAPI:     $(YELLOW)http://localhost:8000/docs$(NC)"
	@echo "  • Grafana:     $(YELLOW)http://localhost:3000$(NC)  (admin/fintech2025)"
	@echo ""

check-syntax: ## 🔍 Check Python syntax of all scripts
	@echo "$(GREEN)Checking Python syntax...$(NC)"
	python3 -m py_compile jupyter/scripts/stock_prediction/train_multi_company.py
	python3 -m py_compile jupyter/scripts/stock_prediction/lstm_stock_prediction.py
	python3 -m py_compile jupyter/scripts/stock_prediction/gru_stock_prediction.py
	python3 -m py_compile jupyter/scripts/stock_prediction/transformer_stock_prediction.py
	python3 -m py_compile airflow/dags/multi_company_stock_training_dag.py
	@echo "$(GREEN)✓ All syntax checks passed!$(NC)"

##@ Training - Single Company

train-tsla: ## 🎯 Train all models for TSLA
	@echo "$(GREEN)Training TSLA models (LSTM, GRU, Transformer)...$(NC)"
	./train_stock.sh TSLA ALL 2018-01-01
	@echo "$(GREEN)✓ TSLA training complete! Check jupyter/models/TSLA/$(NC)"

train-aapl: ## 🍎 Train all models for AAPL
	@echo "$(GREEN)Training AAPL models (LSTM, GRU, Transformer)...$(NC)"
	./train_stock.sh AAPL ALL 2018-01-01
	@echo "$(GREEN)✓ AAPL training complete! Check jupyter/models/AAPL/$(NC)"

train-googl: ## 🔍 Train all models for GOOGL
	@echo "$(GREEN)Training GOOGL models (LSTM, GRU, Transformer)...$(NC)"
	./train_stock.sh GOOGL ALL 2018-01-01
	@echo "$(GREEN)✓ GOOGL training complete! Check jupyter/models/GOOGL/$(NC)"

train-nvda: ## 💻 Train all models for NVDA
	@echo "$(GREEN)Training NVDA models (LSTM, GRU, Transformer)...$(NC)"
	./train_stock.sh NVDA ALL 2018-01-01
	@echo "$(GREEN)✓ NVDA training complete! Check jupyter/models/NVDA/$(NC)"

train-msft: ## 🪟 Train all models for MSFT
	@echo "$(GREEN)Training MSFT models (LSTM, GRU, Transformer)...$(NC)"
	./train_stock.sh MSFT ALL 2018-01-01
	@echo "$(GREEN)✓ MSFT training complete! Check jupyter/models/MSFT/$(NC)"

##@ Training - Multiple Companies

train-tech: ## 🚀 Train major tech stocks (TSLA, AAPL, GOOGL, MSFT, NVDA)
	@echo "$(GREEN)Training major tech stocks...$(NC)"
	@for ticker in TSLA AAPL GOOGL MSFT NVDA; do \
		echo "$(YELLOW)Training $$ticker...$(NC)"; \
		./train_stock.sh $$ticker ALL 2018-01-01 || true; \
	done
	@echo "$(GREEN)✓ Tech stocks training complete!$(NC)"

train-semiconductor: ## 💾 Train semiconductor stocks (NVDA, AMD, INTC, TSM)
	@echo "$(GREEN)Training semiconductor stocks...$(NC)"
	@for ticker in NVDA AMD INTC TSM; do \
		echo "$(YELLOW)Training $$ticker...$(NC)"; \
		./train_stock.sh $$ticker ALL 2018-01-01 || true; \
	done
	@echo "$(GREEN)✓ Semiconductor stocks training complete!$(NC)"

train-faang: ## 📱 Train FAANG stocks (META, AAPL, AMZN, NFLX, GOOGL)
	@echo "$(GREEN)Training FAANG stocks...$(NC)"
	@for ticker in META AAPL AMZN NFLX GOOGL; do \
		echo "$(YELLOW)Training $$ticker...$(NC)"; \
		./train_stock.sh $$ticker ALL 2018-01-01 || true; \
	done
	@echo "$(GREEN)✓ FAANG stocks training complete!$(NC)"

train-all-default: ## 🌟 Train all default stocks (TSLA, AAPL, GOOGL, MSFT, AMZN)
	@echo "$(GREEN)Training all default stocks...$(NC)"
	@for ticker in TSLA AAPL GOOGL MSFT AMZN; do \
		echo "$(YELLOW)Training $$ticker...$(NC)"; \
		./train_stock.sh $$ticker ALL 2018-01-01 || true; \
	done
	@echo "$(GREEN)✓ All default stocks training complete!$(NC)"

##@ Training - Specific Models

train-lstm-only: ## 🧠 Train LSTM model only for TSLA (faster)
	@echo "$(GREEN)Training TSLA with LSTM only...$(NC)"
	./train_stock.sh TSLA LSTM 2018-01-01
	@echo "$(GREEN)✓ LSTM training complete!$(NC)"

train-gru-only: ## 🧠 Train GRU model only for TSLA
	@echo "$(GREEN)Training TSLA with GRU only...$(NC)"
	./train_stock.sh TSLA GRU 2018-01-01
	@echo "$(GREEN)✓ GRU training complete!$(NC)"

train-transformer-only: ## 🧠 Train Transformer model only for TSLA
	@echo "$(GREEN)Training TSLA with Transformer only...$(NC)"
	./train_stock.sh TSLA TRANSFORMER 2018-01-01
	@echo "$(GREEN)✓ Transformer training complete!$(NC)"

##@ Training - Quick Tests

train-test-quick: ## ⚡ Quick test training (AAPL, LSTM, 2023-2024)
	@echo "$(GREEN)Running quick test training...$(NC)"
	./train_stock.sh AAPL LSTM 2023-01-01 2024-01-01
	@echo "$(GREEN)✓ Quick test complete!$(NC)"

train-test-recent: ## ⚡ Test with recent data (TSLA, ALL, 2023-2024)
	@echo "$(GREEN)Training with recent data...$(NC)"
	./train_stock.sh TSLA ALL 2023-01-01 2024-12-31
	@echo "$(GREEN)✓ Recent data training complete!$(NC)"

##@ Airflow Integration

airflow-trigger: ## 🎯 Trigger Airflow DAG (multi_company_stock_training)
	@echo "$(GREEN)Triggering Airflow DAG...$(NC)"
	$(AIRFLOW_EXEC) airflow dags trigger multi_company_stock_training
	@echo "$(GREEN)✓ DAG triggered! Check http://localhost:8083$(NC)"

airflow-list: ## 📋 List all Airflow DAGs
	@echo "$(GREEN)Available Airflow DAGs:$(NC)"
	$(AIRFLOW_EXEC) airflow dags list

airflow-status: ## 📊 Show Airflow DAG status
	@echo "$(GREEN)Airflow DAG runs:$(NC)"
	$(AIRFLOW_EXEC) airflow dags list-runs

airflow-logs: ## 📜 Show Airflow scheduler logs
	$(COMPOSE) logs -f airflow

##@ Model Management

models-list: ## 📁 List all trained models
	@echo "$(GREEN)Trained models:$(NC)"
	@find jupyter/models -name "*.h5" -type f 2>/dev/null | sort || echo "No models found yet"

models-list-all: ## 📁 List all model files (h5, pkl, png)
	@echo "$(GREEN)All model files:$(NC)"
	@find jupyter/models -type f 2>/dev/null | sort || echo "No files found yet"

models-size: ## 💾 Show model sizes
	@echo "$(GREEN)Model sizes:$(NC)"
	@du -sh jupyter/models/* 2>/dev/null || echo "No models found yet"

models-clean: ## 🗑️  Clean all trained models (DANGEROUS!)
	@echo "$(RED)WARNING: This will delete all trained models!$(NC)"
	@echo "$(YELLOW)Press Ctrl+C to cancel, or Enter to continue...$(NC)"
	@read confirm
	rm -rf jupyter/models/*/
	@echo "$(GREEN)✓ Models cleaned!$(NC)"

models-backup: ## 💾 Backup models to models_backup/
	@echo "$(GREEN)Backing up models...$(NC)"
	@mkdir -p models_backup
	@cp -r jupyter/models/* models_backup/ 2>/dev/null || echo "No models to backup"
	@echo "$(GREEN)✓ Models backed up to models_backup/$(NC)"

##@ Viewing Results

view-tsla: ## 👁️  View TSLA model metrics
	@echo "$(GREEN)TSLA Model Metrics:$(NC)"
	@$(JUPYTER_EXEC) python -c "import pickle; import os; \
		for model in ['lstm', 'gru', 'transformer']: \
			path = f'models/TSLA/{model}_tsla_metrics.pkl'; \
			print(f'\n{model.upper()}:'); \
			m = pickle.load(open(path, 'rb')) if os.path.exists(path) else None; \
			print(f\"  RMSE: \$${m['rmse']:.2f}\") if m else print('  Not trained yet'); \
			print(f\"  MAE:  \$${m['mae']:.2f}\") if m else None; \
			print(f\"  MAPE: {m['mape']:.2f}%\") if m else None" 2>/dev/null || echo "Models not found. Train first!"

view-plots: ## 🖼️  Open all prediction plots (macOS)
	@echo "$(GREEN)Opening plots...$(NC)"
	@open jupyter/models/*/lstm_*_prediction.png 2>/dev/null || echo "No plots found"

compare-models: ## 📊 Compare all models for TSLA
	@echo "$(GREEN)Comparing models...$(NC)"
	$(JUPYTER_EXEC) python scripts/stock_prediction/compare_models.py

compare-all: ## 📊 Compare ALL trained models (all tickers)
	@echo "$(GREEN)Comparing all trained models...$(NC)"
	$(JUPYTER_EXEC) python scripts/stock_prediction/compare_all_models.py

compare-aapl: ## 📊 Compare AAPL models (LSTM vs GRU vs Transformer)
	@echo "$(GREEN)Comparing AAPL models...$(NC)"
	$(JUPYTER_EXEC) python scripts/stock_prediction/compare_all_models.py --ticker AAPL

compare-tsla: ## 📊 Compare TSLA models (LSTM vs GRU vs Transformer)
	@echo "$(GREEN)Comparing TSLA models...$(NC)"
	$(JUPYTER_EXEC) python scripts/stock_prediction/compare_all_models.py --ticker TSLA

##@ Future Prediction

# Generic prediction commands (use with TICKER parameter)
predict-day: ## 🔮 Predict next 30 days (use: make predict-day TICKER=AAPL)
	@if [ -z "$(TICKER)" ]; then \
		echo "$(RED)Error: TICKER not specified!$(NC)"; \
		echo "$(YELLOW)Usage: make predict-day TICKER=AAPL$(NC)"; \
		echo "$(YELLOW)Or use: make predict-aapl-day$(NC)"; \
		exit 1; \
	fi
	@echo "$(GREEN)Predicting $(TICKER) (30 days)...$(NC)"
	$(JUPYTER_EXEC) python scripts/stock_prediction/predict_future.py --ticker $(TICKER) --model GRU --periods 30 --period-type day

predict-week: ## 🔮 Predict next 4 weeks (use: make predict-week TICKER=AAPL)
	@if [ -z "$(TICKER)" ]; then \
		echo "$(RED)Error: TICKER not specified!$(NC)"; \
		echo "$(YELLOW)Usage: make predict-week TICKER=AAPL$(NC)"; \
		echo "$(YELLOW)Or use: make predict-aapl-week$(NC)"; \
		exit 1; \
	fi
	@echo "$(GREEN)Predicting $(TICKER) (4 weeks)...$(NC)"
	$(JUPYTER_EXEC) python scripts/stock_prediction/predict_future.py --ticker $(TICKER) --model GRU --periods 4 --period-type week

predict-month: ## 🔮 Predict next 3 months (use: make predict-month TICKER=AAPL)
	@if [ -z "$(TICKER)" ]; then \
		echo "$(RED)Error: TICKER not specified!$(NC)"; \
		echo "$(YELLOW)Usage: make predict-month TICKER=AAPL$(NC)"; \
		echo "$(YELLOW)Or use: make predict-aapl-month$(NC)"; \
		exit 1; \
	fi
	@echo "$(GREEN)Predicting $(TICKER) (3 months)...$(NC)"
	$(JUPYTER_EXEC) python scripts/stock_prediction/predict_future.py --ticker $(TICKER) --model GRU --periods 3 --period-type month

predict-year: ## 🔮 Predict next 1 year (use: make predict-year TICKER=AAPL)
	@if [ -z "$(TICKER)" ]; then \
		echo "$(RED)Error: TICKER not specified!$(NC)"; \
		echo "$(YELLOW)Usage: make predict-year TICKER=AAPL$(NC)"; \
		echo "$(YELLOW)Or use: make predict-aapl-year$(NC)"; \
		exit 1; \
	fi
	@echo "$(GREEN)Predicting $(TICKER) (1 year)...$(NC)"
	$(JUPYTER_EXEC) python scripts/stock_prediction/predict_future.py --ticker $(TICKER) --model GRU --periods 1 --period-type year

# Specific shortcuts for AAPL
predict-aapl-day: ## 🔮 Predict AAPL next 30 days
	@echo "$(GREEN)Predicting AAPL (30 days)...$(NC)"
	$(JUPYTER_EXEC) python scripts/stock_prediction/predict_future.py --ticker AAPL --model GRU --periods 30 --period-type day

predict-aapl-week: ## 🔮 Predict AAPL next 4 weeks
	@echo "$(GREEN)Predicting AAPL (4 weeks)...$(NC)"
	$(JUPYTER_EXEC) python scripts/stock_prediction/predict_future.py --ticker AAPL --model GRU --periods 4 --period-type week

predict-aapl-month: ## 🔮 Predict AAPL next 3 months
	@echo "$(GREEN)Predicting AAPL (3 months)...$(NC)"
	$(JUPYTER_EXEC) python scripts/stock_prediction/predict_future.py --ticker AAPL --model GRU --periods 3 --period-type month

predict-aapl-year: ## 🔮 Predict AAPL next 1 year
	@echo "$(GREEN)Predicting AAPL (1 year)...$(NC)"
	$(JUPYTER_EXEC) python scripts/stock_prediction/predict_future.py --ticker AAPL --model GRU --periods 1 --period-type year

predict-tsla-day: ## 🔮 Predict TSLA next 30 days
	@echo "$(GREEN)Predicting TSLA (30 days)...$(NC)"
	$(JUPYTER_EXEC) python scripts/stock_prediction/predict_future.py --ticker TSLA --model GRU --periods 30 --period-type day

predict-tsla-week: ## 🔮 Predict TSLA next 4 weeks
	@echo "$(GREEN)Predicting TSLA (4 weeks)...$(NC)"
	$(JUPYTER_EXEC) python scripts/stock_prediction/predict_future.py --ticker TSLA --model GRU --periods 4 --period-type week

predict-tsla-month: ## 🔮 Predict TSLA next 3 months
	@echo "$(GREEN)Predicting TSLA (3 months)...$(NC)"
	$(JUPYTER_EXEC) python scripts/stock_prediction/predict_future.py --ticker TSLA --model GRU --periods 3 --period-type month

# Custom prediction with full control
predict-custom: ## 🔮 Custom prediction (use: make predict-custom TICKER=AAPL MODEL=GRU PERIODS=30 TYPE=day)
	@if [ -z "$(TICKER)" ]; then \
		echo "$(RED)Error: TICKER not specified!$(NC)"; \
		echo "$(YELLOW)Usage: make predict-custom TICKER=AAPL MODEL=GRU PERIODS=30 TYPE=day$(NC)"; \
		echo "$(YELLOW)MODEL options: LSTM, GRU, TRANSFORMER$(NC)"; \
		echo "$(YELLOW)TYPE options: day, week, month, year$(NC)"; \
		exit 1; \
	fi
	@MODEL_TO_USE=$${MODEL:-GRU}; \
	PERIODS_TO_USE=$${PERIODS:-30}; \
	TYPE_TO_USE=$${TYPE:-day}; \
	echo "$(GREEN)Predicting $(TICKER) with $$MODEL_TO_USE model ($$PERIODS_TO_USE $$TYPE_TO_USE)...$(NC)"; \
	$(JUPYTER_EXEC) python scripts/stock_prediction/predict_future.py \
		--ticker $(TICKER) --model $$MODEL_TO_USE --periods $$PERIODS_TO_USE --period-type $$TYPE_TO_USE

##@ UI Training (JupyterLab Notebook)

train-ui: ## 🎨 Open training UI notebook in JupyterLab
	@echo "$(GREEN)Opening training UI notebook...$(NC)"
	@echo "$(YELLOW)1. Go to: http://localhost:8888$(NC)"
	@echo "$(YELLOW)2. Token: fintech2025$(NC)"
	@echo "$(YELLOW)3. Open: notebooks/train_stocks_ui.ipynb$(NC)"
	@echo ""
	@echo "$(GREEN)✓ The notebook provides an interactive UI for training!$(NC)"

open-jupyter: ## 🌐 Open JupyterLab in browser (macOS)
	@echo "$(GREEN)Opening JupyterLab...$(NC)"
	@open "http://localhost:8888/lab/tree/notebooks/train_stocks_ui.ipynb?token=fintech2025" 2>/dev/null || \
	echo "$(YELLOW)Go to: http://localhost:8888 (Token: fintech2025)$(NC)"

notebook-info: ## ℹ️  Show info about training notebook
	@echo "$(GREEN)═══════════════════════════════════════════════════════════$(NC)"
	@echo "$(GREEN)Training Notebook: train_stocks_ui.ipynb$(NC)"
	@echo "$(GREEN)═══════════════════════════════════════════════════════════$(NC)"
	@echo ""
	@echo "$(YELLOW)Features:$(NC)"
	@echo "  • Interactive widgets for configuration"
	@echo "  • Train single or multiple companies"
	@echo "  • Real-time progress display"
	@echo "  • View results and compare models"
	@echo "  • Automatic retry with rate limit handling"
	@echo ""
	@echo "$(YELLOW)How to use:$(NC)"
	@echo "  1. Run: make open-jupyter"
	@echo "  2. Navigate to: notebooks/train_stocks_ui.ipynb"
	@echo "  3. Edit configuration cells"
	@echo "  4. Run cells to train models"
	@echo ""
	@echo "$(YELLOW)Quick access:$(NC)"
	@echo "  • URL: http://localhost:8888"
	@echo "  • Token: fintech2025"
	@echo "  • File: notebooks/train_stocks_ui.ipynb"
	@echo ""

##@ Development & Testing

shell-jupyter: ## 🐚 Open shell in JupyterLab container
	$(JUPYTER_EXEC) bash

shell-airflow: ## 🐚 Open shell in Airflow container
	$(AIRFLOW_EXEC) bash

shell-fastapi: ## 🐚 Open shell in FastAPI container
	$(COMPOSE) exec fastapi bash

test-yfinance: ## 🧪 Test yfinance data download
	@echo "$(GREEN)Testing yfinance download for TSLA...$(NC)"
	$(JUPYTER_EXEC) python -c "import yfinance as yf; print(yf.download('TSLA', period='1mo'))"

test-paths: ## 🧪 Test relative paths work correctly
	@echo "$(GREEN)Testing relative paths...$(NC)"
	$(JUPYTER_EXEC) python -c "import os, sys; sys.path.insert(0, 'scripts/stock_prediction'); \
		from train_multi_company import StockModelTrainer; \
		t = StockModelTrainer('TEST', 'LSTM'); \
		print(f'Project root: {t.project_root}'); \
		print(f'Model dir: {t.model_dir}')"

##@ Cleanup

clean: ## 🧹 Clean Python cache files
	@echo "$(YELLOW)Cleaning cache files...$(NC)"
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "$(GREEN)✓ Cache cleaned!$(NC)"

clean-docker: ## 🐳 Clean Docker (stop, remove containers, volumes, networks)
	@echo "$(YELLOW)Cleaning Docker...$(NC)"
	-$(COMPOSE) down -v --remove-orphans 2>/dev/null || true
	@echo "$(GREEN)✓ Docker cleaned!$(NC)"

clean-all: down clean models-clean ## 🧹 Clean everything (stop services, clean cache, remove models)
	@echo "$(RED)Everything cleaned!$(NC)"

reset: clean-all build up ## 🔄 Full reset (clean everything and rebuild)
	@echo "$(GREEN)✓ System reset complete!$(NC)"

force-rebuild: clean-docker ## 🔨 Force rebuild (clean Docker + rebuild from scratch)
	@echo "$(YELLOW)Forcing complete rebuild with retry...$(NC)"
	@for i in 1 2 3; do \
		echo "$(YELLOW)Attempt $$i/3...$(NC)"; \
		$(COMPOSE) build --no-cache --pull jupyterlab && break || \
		(echo "$(RED)Build failed, retrying in 10 seconds...$(NC)" && sleep 10); \
	done
	@echo "$(GREEN)✓ Force rebuild complete!$(NC)"

pull-base-image: ## 📥 Pull base image manually (use if network is slow)
	@echo "$(YELLOW)Pulling base image (jupyter/scipy-notebook)...$(NC)"
	@for i in 1 2 3 4 5; do \
		echo "$(YELLOW)Attempt $$i/5...$(NC)"; \
		docker pull jupyter/scipy-notebook:latest && break || \
		(echo "$(RED)Pull failed, retrying in 10 seconds...$(NC)" && sleep 10); \
	done
	@echo "$(GREEN)✓ Base image pulled!$(NC)"

build-after-pull: pull-base-image build-fast ## 📥 Pull base image first, then build
	@echo "$(GREEN)✓ Build with pre-pulled image complete!$(NC)"

##@ Documentation

docs: ## 📚 Open documentation in browser
	@echo "$(GREEN)Opening documentation...$(NC)"
	@open SUMMARY.md README_MULTI_COMPANY.md HYBRID_TRAINING_GUIDE.md 2>/dev/null || \
		echo "Open these files manually:\n  - SUMMARY.md\n  - README_MULTI_COMPANY.md\n  - HYBRID_TRAINING_GUIDE.md"

urls: ## 🌐 Show all service URLs
	@echo "$(GREEN)Service URLs:$(NC)"
	@echo "  • JupyterLab:  http://localhost:8888  (Token: fintech2025)"
	@echo "  • Airflow:     http://localhost:8083  (admin/fintech2025)"
	@echo "  • FastAPI:     http://localhost:8000/docs"
	@echo "  • Grafana:     http://localhost:3000  (admin/fintech2025)"
	@echo "  • Prometheus:  http://localhost:9090"

##@ API-Based Training (via FastAPI)

train-api: ## 🌐 Train ticker via API (use: make train-api TICKER=AAPL)
	@if [ -z "$(TICKER)" ]; then \
		echo "$(RED)Error: TICKER not specified!$(NC)"; \
		echo "$(YELLOW)Usage: make train-api TICKER=AAPL$(NC)"; \
		exit 1; \
	fi
	@echo "$(GREEN)Starting training for $(TICKER) via API...$(NC)"
	@curl -X POST "http://localhost:8000/train/$(TICKER)" | python3 -m json.tool || echo "$(RED)API call failed. Is FastAPI running?$(NC)"
	@echo ""
	@echo "$(YELLOW)Training started! This will take 30-60 minutes.$(NC)"
	@echo "$(YELLOW)Check status at: http://localhost:8082/stock/$(NC)"

predict-api-day: ## 🌐 Predict via API (30 days, use: make predict-api-day TICKER=AAPL)
	@if [ -z "$(TICKER)" ]; then \
		echo "$(RED)Error: TICKER not specified!$(NC)"; \
		echo "$(YELLOW)Usage: make predict-api-day TICKER=AAPL MODEL=gru$(NC)"; \
		exit 1; \
	fi
	@MODEL_TO_USE=$${MODEL:-gru}; \
	echo "$(GREEN)Predicting $(TICKER) (30 days) via API...$(NC)"; \
	curl -X POST "http://localhost:8000/predict/future?ticker=$(TICKER)&model=$$MODEL_TO_USE&periods=30&period_type=day" | python3 -m json.tool || echo "$(RED)API call failed$(NC)"

predict-api-month: ## 🌐 Predict via API (3 months, use: make predict-api-month TICKER=AAPL)
	@if [ -z "$(TICKER)" ]; then \
		echo "$(RED)Error: TICKER not specified!$(NC)"; \
		echo "$(YELLOW)Usage: make predict-api-month TICKER=AAPL MODEL=gru$(NC)"; \
		exit 1; \
	fi
	@MODEL_TO_USE=$${MODEL:-gru}; \
	echo "$(GREEN)Predicting $(TICKER) (3 months) via API...$(NC)"; \
	curl -X POST "http://localhost:8000/predict/future?ticker=$(TICKER)&model=$$MODEL_TO_USE&periods=3&period_type=month" | python3 -m json.tool || echo "$(RED)API call failed$(NC)"

predict-api-year: ## 🌐 Predict via API (1 year, use: make predict-api-year TICKER=AAPL)
	@if [ -z "$(TICKER)" ]; then \
		echo "$(RED)Error: TICKER not specified!$(NC)"; \
		echo "$(YELLOW)Usage: make predict-api-year TICKER=AAPL MODEL=gru$(NC)"; \
		exit 1; \
	fi
	@MODEL_TO_USE=$${MODEL:-gru}; \
	echo "$(GREEN)Predicting $(TICKER) (1 year) via API...$(NC)"; \
	curl -X POST "http://localhost:8000/predict/future?ticker=$(TICKER)&model=$$MODEL_TO_USE&periods=1&period_type=year" | python3 -m json.tool || echo "$(RED)API call failed$(NC)"

##@ Complete Workflows

workflow-first-time: build up wait check train-test-quick ## 🎓 First time setup workflow
	@echo ""
	@echo "$(GREEN)╔═══════════════════════════════════════════════════════════╗$(NC)"
	@echo "$(GREEN)║  ✓ First time setup complete!                            ║$(NC)"
	@echo "$(GREEN)║                                                           ║$(NC)"
	@echo "$(GREEN)║  Next steps:                                              ║$(NC)"
	@echo "$(GREEN)║  1. make train-tsla      - Train TSLA models              ║$(NC)"
	@echo "$(GREEN)║  2. make train-tech      - Train tech stocks              ║$(NC)"
	@echo "$(GREEN)║  3. make view-tsla       - View metrics                   ║$(NC)"
	@echo "$(GREEN)║  4. make urls            - See all service URLs           ║$(NC)"
	@echo "$(GREEN)╚═══════════════════════════════════════════════════════════╝$(NC)"
	@echo ""

workflow-daily: up train-tsla view-tsla ## 📅 Daily workflow (start, train TSLA, view results)
	@echo "$(GREEN)✓ Daily workflow complete!$(NC)"

workflow-weekly: up train-tech models-backup ## 📅 Weekly workflow (train tech stocks, backup)
	@echo "$(GREEN)✓ Weekly workflow complete!$(NC)"
