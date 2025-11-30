# Command Reference

Quick commands for development and deployment.

---

## Local Development

### Setup
```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser (admin)
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic
```

### Running Server
```bash
# Development server
python manage.py runserver

# Production-like (Waitress)
python -m waitress --host 0.0.0.0 --port 8000 video_project.wsgi:application

# Production (Gunicorn - Linux only)
gunicorn video_project.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

### Testing
```bash
# Run all tests
python manage.py test

# Run specific test
python manage.py test video_share.tests.VideoModelTest

# Check for issues
python manage.py check

# Check with production settings
DJANGO_SETTINGS_MODULE=video_project.settings_prod python manage.py check
```

---

## Database

### Migrations
```bash
# Create migration (after model changes)
python manage.py makemigrations

# Show migration status
python manage.py showmigrations

# Apply migrations
python manage.py migrate

# Reverse migration
python manage.py migrate video_share 0001

# List all migrations
python manage.py migrate --list
```

### Database Shell
```bash
# SQLite shell
python manage.py dbshell

# Run raw SQL
python manage.py dbshell < script.sql
```

### Django Shell
```bash
# Interactive Python shell with Django context
python manage.py shell

# Example commands:
# >>> from video_share.models import Video
# >>> Video.objects.all()
# >>> v = Video.objects.get(id=1)
# >>> v.likes
# >>> v.toggle_like(user=request.user)
```

---

## Static Files

```bash
# Collect all static files
python manage.py collectstatic

# Collect without prompting
python manage.py collectstatic --noinput

# Clear and collect
python manage.py collectstatic --clear --noinput

# Show files that would be collected (dry run)
python manage.py collectstatic --dry-run
```

---

## Git Commands

```bash
# Initialize repository
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit"

# Add remote
git remote add origin https://github.com/yourusername/video_project.git

# Push to GitHub
git push -u origin main

# Check status
git status

# View log
git log --oneline

# Create new branch
git checkout -b feature-branch

# Switch branch
git checkout main

# Merge branch
git merge feature-branch
```

---

## Docker (if Docker installed)

```bash
# Build image
docker build -t video_project:latest .

# Run container
docker run -p 8000:8000 video_project:latest

# Docker Compose
docker-compose up -d
docker-compose down
docker-compose logs -f web

# Run migration in container
docker-compose exec web python manage.py migrate

# Access container shell
docker-compose exec web bash
```

---

## Deployment Commands

### Render/Railway (Web UI)
```
No commands needed! Just push to GitHub.
Platforms auto-deploy on push.
```

### Heroku (CLI)
```bash
# Login
heroku login

# Create app
heroku create your-app-name

# Set environment variable
heroku config:set DEBUG=False

# Deploy
git push heroku main

# View logs
heroku logs --tail

# Open app
heroku open
```

### Manual VPS/Server
```bash
# SSH into server
ssh user@server.com

# Clone repo
git clone https://github.com/yourusername/video_project.git

# Setup venv
python3 -m venv venv
source venv/bin/activate

# Install deps
pip install -r requirements.txt

# Migrate database
python manage.py migrate

# Collect static
python manage.py collectstatic --noinput

# Start Gunicorn
gunicorn video_project.wsgi:application --bind 0.0.0.0:8000
```

---

## Debugging

```bash
# Print SQL queries
python manage.py shell
>>> from django.db import connection
>>> connection.queries

# Profile view performance
python manage.py shell
>>> import cProfile
>>> cProfile.run('...')

# Verbose output
python manage.py migrate --verbosity 2

# Debug specific view
python manage.py runserver --debug-toolbar

# Check settings
python manage.py shell
>>> from django.conf import settings
>>> settings.DEBUG
```

---

## Admin Commands

```bash
# Create admin user
python manage.py createsuperuser

# Change password
python manage.py changepassword username

# Delete all data
python manage.py flush

# Clear cache
python manage.py clear_cache

# Count records
python manage.py shell
>>> from video_share.models import Video
>>> Video.objects.count()
```

---

## Production Utilities

```bash
# Generate SECRET_KEY
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Check allowed hosts
python manage.py shell
>>> from django.conf import settings
>>> settings.ALLOWED_HOSTS

# Test email
python manage.py shell
>>> from django.core.mail import send_mail
>>> send_mail('Test', 'Message', 'from@example.com', ['to@example.com'])

# Create fixture (export data)
python manage.py dumpdata video_share > backup.json

# Load fixture (import data)
python manage.py loaddata backup.json
```

---

## Monitoring & Logs

```bash
# View logs (production)
# Render: Dashboard → Logs
# Railway: Dashboard → Logs
# Heroku: heroku logs --tail

# Check app status
curl https://yourdomain.com/

# Test API
curl -X POST https://yourdomain.com/api/like/1/ \
  -H "X-CSRFToken: token" \
  -H "Content-Type: application/json"

# Monitor resource usage
# Render: Dashboard → Metrics
# Railway: Dashboard → Deployments → Logs
```

---

## Performance Optimization

```bash
# Check N+1 queries
pip install django-debug-toolbar

# Profile database
python manage.py shell
>>> from django.test.utils import CaptureQueriesContext
>>> from django.db import connection
>>> with CaptureQueriesContext(connection) as ctx:
>>>     Video.objects.all().count()
>>> len(ctx)  # Number of queries

# Check template rendering
pip install django-silk
# (Add to INSTALLED_APPS and MIDDLEWARE)
```

---

## Useful Shortcuts

| Command | Purpose |
|---------|---------|
| `python manage.py` | Help for all commands |
| `python manage.py help <command>` | Help for specific command |
| `python manage.py shell` | Interactive Django shell |
| `python manage.py sqlsequencereset video_share` | Reset database sequences |
| `python manage.py inspectdb` | Reverse engineer database |

---

## Environment Variables

```bash
# Windows PowerShell
$env:DEBUG = "False"
$env:DATABASE_URL = "postgresql://..."

# Linux/Mac
export DEBUG=False
export DATABASE_URL="postgresql://..."

# Check env var
$env:DEBUG  # PowerShell
echo $DEBUG  # Linux/Mac
```

---

## Useful Packages

```bash
# Already installed:
pip install Django==5.0
pip install django-cors-headers==4.3.1
pip install gunicorn==21.2.0
pip install whitenoise==6.6.0
pip install Pillow==10.4.0
pip install psycopg2-binary==2.9.10
pip install dj-database-url==1.0.0

# Additional (optional):
pip install django-debug-toolbar          # Development debugging
pip install django-extensions             # Extra management commands
pip install django-storages               # AWS S3 support
pip install boto3                          # AWS SDK
pip install celery                         # Task queue
pip install redis                          # Caching
pip install djangorestframework             # REST API
```

---

## Emergency Commands

```bash
# Stop runaway processes
taskkill /IM python.exe /F  # Windows

# Kill by port
lsof -ti:8000 | xargs kill -9  # Mac/Linux

# Restore database from backup
# Contact platform support or restore from backup service

# Rollback deployment
# Render: Dashboard → Deployment History → Rollback
# Railway: Similar process
# Git: git revert HEAD

# Emergency downtime message
# Update Django template or create maintenance.html
```

---

## Tips & Tricks

- Add `.py` files to `.gitignore` for secrets
- Use environment variables for all secrets
- Always test locally before deploying
- Keep database backups
- Monitor error logs daily
- Keep dependencies updated
- Use virtual environment always
- Test on mobile devices
- Enable HTTPS everywhere
- Use strong SECRET_KEY

---

**For more help:** Check DEPLOYMENT_GUIDE.md or QUICK_START.md
