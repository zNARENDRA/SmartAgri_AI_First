#!/usr/bin/env bash
# Render.com Build Script for SmartAgri AI Backend
# This script runs during deployment to set up the environment

set -e

echo "=== Installing Python dependencies ==="
pip install -r requirements.txt

echo "=== Downloading and processing datasets ==="
python scripts/download_and_process_data.py

echo "=== Seeding SQLite database ==="
python scripts/seed_sqlite_db.py

echo "=== Training ML models ==="
python scripts/train_crop_recommendation.py
python scripts/train_yield_prediction.py
python scripts/setup_disease_model.py

echo "=== Build complete! ==="
