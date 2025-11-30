# Video Share - Django Reels App

A modern, mobile-first video sharing platform built with **Django**, featuring TikTok/Instagram Reels-style interface.

![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![Django](https://img.shields.io/badge/Django-5.0-darkgreen)

---


---

## Quick Start

### Local Development

```bash
# 1. Clone and setup
git clone <repo-url>
cd video_project
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run migrations
python manage.py migrate

# 4. Create admin user
python manage.py createsuperuser

# 5. Run server
python manage.py runserver
```

Visit: http://127.0.0.1:8000

---

## Deployment

### ⭐ Recommended: Render

1. Push to GitHub
2. Go to [Render.com](https://render.com)
3. Create Web Service → Connect repo
4. Build: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
5. Start: `gunicorn video_project.wsgi:application`
6. Add Postgres database
7. Deploy!

**See DEPLOYMENT_GUIDE.md for complete instructions.**

---

## Documentation

- **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** ⭐ Start here!
- **[QUICK_START.md](QUICK_START.md)** - Quick reference
- **[PRODUCTION_CHECKLIST.md](PRODUCTION_CHECKLIST.md)** - Pre-deploy checklist
- **[COMMANDS.md](COMMANDS.md)** - Command reference

---

## Project Structure

```
video_project/
├── video_share/          # Main app
│   ├── models.py         # Video database model
│   ├── views.py          # API & views
│   ├── urls.py           # URL routing
│   └── templates/
│       ├── video_player.html  # Main reels interface
│       ├── video_detail.html
│       └── upload.html
├── video_project/        # Django settings
│   ├── settings.py       # Development
│   └── settings_prod.py  # Production
├── static/               # CSS, JS
├── media/                # User uploads
├── requirements.txt      # Dependencies
├── Dockerfile            # Docker setup
└── docker-compose.yml    # Multi-container
```

---

## Key Features Implemented

✅ Video upload with validation  
✅ Database-backed Video model  
✅ Reels-style player interface  
✅ Like/view tracking  
✅ Responsive mobile design  
✅ CSRF protection  
✅ Static file optimization  
✅ Production settings (Postgres, HTTPS)  
✅ Docker containerization  
✅ Multi-platform deployment docs  

---

## Environment Variables

Create `.env` file:

```bash
DEBUG=False
SECRET_KEY=your-long-random-key
ALLOWED_HOSTS=yourdomain.com
DATABASE_URL=postgresql://user:pass@host:5432/db
```

---

## API Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/` | Home |
| GET | `/reels/` | Video list |
| GET | `/video/<id>/` | Single video |
| POST | `/api/like/<id>/` | Like video |
| POST | `/upload/` | Upload video |
| GET | `/stream/<id>/` | Stream video |

---

## Technology Stack

- **Backend:** Django 5.0
- **Database:** SQLite (dev) / PostgreSQL (prod)
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **Server:** Gunicorn / Waitress
- **Static:** WhiteNoise
- **Container:** Docker & Docker Compose

---

## Running Locally

```bash
# Development server
python manage.py runserver

# Or production-like
python -m waitress --port 8000 video_project.wsgi:application

# Admin panel
http://127.0.0.1:8000/admin/
```

---

## Testing Endpoints

```bash
# Home
curl http://127.0.0.1:8000/

# Reels
curl http://127.0.0.1:8000/reels/

# Like API (requires CSRF token)
curl -X POST http://127.0.0.1:8000/api/like/1/ \
  -H "X-CSRFToken: token"
```

---

## Production Deployment

Before deploying, check:

- [ ] `DEBUG = False`
- [ ] `SECRET_KEY` is strong
- [ ] `ALLOWED_HOSTS` configured
- [ ] Database configured
- [ ] Static files collected
- [ ] Migrations applied
- [ ] Environment variables set

See **PRODUCTION_CHECKLIST.md** for full checklist.

---

## Docker

```bash
# Build
docker build -t video_project:latest .

# Run with Compose
docker-compose up -d

# Migrations
docker-compose exec web python manage.py migrate

# Stop
docker-compose down
```

---

## Common Issues

### Video won't play
- Check file format (MP4 recommended)
- Verify upload succeeded
- Check browser console

### Like button not working
- Check CSRF token
- Verify JavaScript enabled
- Check server logs

### Database error
```bash
python manage.py migrate
```

---

## Performance

- CDN support ready
- S3 integration example included
- Database query optimization
- Static file compression
- Cache-friendly headers

---

## Support

- Django docs: https://docs.djangoproject.com
- Platform help: See DEPLOYMENT_GUIDE.md
- Stack Overflow: Tag with `django`

---

## License

MIT License - Use freely for personal or commercial projects

---

## Next Steps

1. **Test locally** - Run the dev server
2. **Review docs** - Read DEPLOYMENT_GUIDE.md
3. **Push to Git** - `git push origin main`
4. **Deploy** - Connect to Render/Railway
5. **Monitor** - Check logs and metrics

---

**Ready to deploy?** → See **DEPLOYMENT_GUIDE.md**

Built with Django 🚀
- تحقق من مسار MEDIA_ROOT
- تأكد من وجود مجلد media/videos

### مشكلة: خطأ 500
```bash
python manage.py collectstatic
DEBUG = True  # في settings.py
```

---

🎉 **الآن لديك مشروع كامل جاهز للتشغيل!**