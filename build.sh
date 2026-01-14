#!/usr/bin/env bash
# Build script for Render

set -o errexit
set -o pipefail

echo "Installing dependencies..."
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear || true

echo "Running migrations..."
python manage.py migrate --noinput || true

echo "Build completed successfully!"
