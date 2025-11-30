from .settings import *
import os
import dj_database_url

# Production settings override
DEBUG = False

# ALLOWED_HOSTS can be provided via environment variable (comma separated)
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')

# Secret key from env
SECRET_KEY = os.environ.get('SECRET_KEY', SECRET_KEY)

# Database from DATABASE_URL env var
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    DATABASES['default'] = dj_database_url.parse(DATABASE_URL, conn_max_age=600)

# Static & media already configured in settings.py; whitenoise used for static files

# Security hardening
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
