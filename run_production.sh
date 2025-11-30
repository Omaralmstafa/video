#!/bin/bash
# Quick start script for Linux/Mac

# Activate venv
source venv/bin/activate

# Install/upgrade packages
python -m pip install --upgrade pip
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Run with gunicorn (production-like)
echo ""
echo "Starting app on http://0.0.0.0:8000 (production-like mode)"
echo "Press Ctrl+C to stop."
echo ""
python -m gunicorn video_project.wsgi:application --bind 0.0.0.0:8000 --workers 2 --log-level info
