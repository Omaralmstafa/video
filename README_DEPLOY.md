Deployment guide — quick start

This project contains Docker and docker-compose configuration to run the app locally or in production-like environments.

Prerequisites
- Docker & docker-compose
- (Optional) A server or cloud provider supporting Docker

Quick local run with Docker Compose
1. Copy `.env.example` to `.env` and edit values (SECRET_KEY, DATABASE_URL if needed).
2. Build and start services:

```bash
docker-compose build
docker-compose up -d
```

3. Run migrations and create a superuser:

```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

4. Visit `http://localhost:8000`.

Production notes
- For production, use a secure `SECRET_KEY`, set `ALLOWED_HOSTS`, and point `DATABASE_URL` to a managed Postgres instance.
- Use S3 (or equivalent) for media storage for large video files.
- Use a reverse proxy (nginx) or cloud load balancer in front of the container.

Heroku
- You can deploy to Heroku using the provided `Procfile` and requirements.txt. Set config vars via `heroku config:set`.

Security
- Ensure `DEBUG=False` and the production settings are used (e.g. set `DJANGO_SETTINGS_MODULE=video_project.settings_prod`).

If you want, I can:
- Build and run the Docker image here locally (requires Docker on your machine).
- Prepare a sample `nginx` config or a systemd unit for Gunicorn.
