@echo off
REM Quick start script for Windows (PowerShell-friendly)

REM Activate venv
call .\venv\Scripts\activate.bat

REM Install/upgrade packages
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Run migrations
python manage.py migrate

REM Collect static files
python manage.py collectstatic --noinput

REM Run with gunicorn (production-like)
echo.
echo Starting app on http://0.0.0.0:8000 (production-like mode)
echo Press Ctrl+C to stop.
echo.
python -m gunicorn video_project.wsgi:application --bind 0.0.0.0:8000 --workers 2 --log-level info
