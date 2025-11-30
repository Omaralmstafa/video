# Deployment Guide - Choose Your Platform

Your Django video sharing app is **production-ready**. Since you don't have Heroku CLI or Docker installed locally, here are the best options:

---

## **Option 1: Render (Recommended - Easiest)**

**Platform:** Cloud hosting with web UI (no CLI needed)  
**Free tier:** Yes (Limited)  
**Setup time:** 5-10 minutes

### Steps:

1. **Go to [https://render.com](https://render.com)** and sign up (GitHub, Google, etc.)

2. **Create New Web Service:**
   - Connect your GitHub repo
   - Build command: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
   - Start command: `gunicorn video_project.wsgi:application`
   - Add environment variables:
     ```
     DEBUG=False
     ALLOWED_HOSTS=yourdomain.onrender.com
     DATABASE_URL=postgresql://user:pass@host:5432/dbname  # Use Render Postgres
     SECRET_KEY=your-very-long-secret-key-here
     ```
   - Create Postgres database (add-on)

3. **Deploy:** Click "Deploy" - done!

**Cost:** Free tier works for testing; ~$7/month for production.

---

## **Option 2: Railway (Simple Web UI)**

**Platform:** Cloud hosting with web UI  
**Free tier:** Yes ($5/month free credits)  
**Setup time:** 5 minutes

### Steps:

1. **Go to [https://railway.app](https://railway.app)** and sign up (GitHub login recommended)

2. **New Project → Deploy from GitHub:**
   - Select your repo
   - Railway auto-detects Python/Django

3. **Add Variables:**
   - `DEBUG=False`
   - `SECRET_KEY=your-long-key`
   - `ALLOWED_HOSTS=yourdomain.railway.app`

4. **Add Postgres Database:** (Railway → "Add Service" → Postgres)

5. **Deploy:** Automatic on push to GitHub

**Cost:** $5/month free credits (covers 1 app + DB)

---

## **Option 3: PythonAnywhere (Python-Specific)**

**Platform:** Python hosting with web UI  
**Free tier:** Yes (Limited)  
**Setup time:** 10 minutes

### Steps:

1. **Go to [https://www.pythonanywhere.com](https://www.pythonanywhere.com)** and create account

2. **Add a New Web App:**
   - Choose Python 3.11
   - Framework: Django
   - Project path: Upload or clone your GitHub repo

3. **Configure:**
   - Web tab → Add static/media paths
   - WSGI configuration → Point to `video_project/wsgi.py`
   - Environment variables in WSGI file or web config

4. **Upload Files:** Via Git clone or web interface

**Cost:** Free tier for testing; $5/month for custom domain

---

## **Option 4: Digital Ocean App Platform (Professional)**

**Platform:** Cloud hosting with web UI  
**Free tier:** $5/month free tier + $3 app platform  
**Setup time:** 10 minutes

### Steps:

1. **Go to [https://www.digitalocean.com](https://www.digitalocean.com)** → App Platform

2. **Create App from GitHub:**
   - Connect your GitHub repo
   - Detect Django automatically

3. **Configure Services:**
   - Web component
   - Postgres database (add-on)
   - Environment: Set vars in UI

4. **Deploy:** Click "Deploy App"

**Cost:** $5/month starter

---

## **Option 5: GitHub Pages + Serverless (For Static + API)**

If you want **free** hosting:
- Use **Vercel** for frontend (React/static)
- Use **Replit** for Django backend
- Not recommended for video streaming (bandwidth limits)

---

## **Quick Checklist Before Deploying:**

- [ ] Update `SECRET_KEY` in `.env` (use strong random value)
- [ ] Set `DEBUG=False` in production
- [ ] Set `ALLOWED_HOSTS` to your domain
- [ ] Use `DATABASE_URL` environment variable (Postgres)
- [ ] Configure HTTPS (all platforms provide free SSL)
- [ ] Test locally first: `python manage.py runserver`
- [ ] Add `.env` to `.gitignore` (✓ Already done)
- [ ] Commit to Git before deploying

---

## **Environment Variables Template**

Create a `.env` file (not pushed to Git):

```bash
DEBUG=False
SECRET_KEY=django-insecure-your-very-long-random-secret-key-here-at-least-50-chars
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,yourdomain.onrender.com
DATABASE_URL=postgresql://user:password@hostname:5432/dbname
```

---

## **Recommended Path (Fastest to Production):**

1. **Render** (if you want simplest setup)
   - Push to GitHub
   - Connect repo to Render
   - Done in 5 minutes

2. **Railway** (if you prefer web UI)
   - Push to GitHub
   - Connect repo to Railway
   - Auto-deploys on push

3. **Digital Ocean** (if you need more control)
   - Professional platform
   - Better for scaling
   - More features

---

## **Step-by-Step: Deploy to Render (Recommended)**

### 1. Push Your Code to GitHub

```powershell
git remote add origin https://github.com/yourusername/video_project.git
git branch -M main
git push -u origin main
```

### 2. Go to Render.com

- Sign up or login
- Click "New +" → "Web Service"
- Select "Connect Repository"
- Authorize GitHub
- Choose `yourusername/video_project`

### 3. Configure Service

```
Service Name: video-project
Environment: Python
Build Command: pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
Start Command: gunicorn video_project.wsgi:application
```

### 4. Add Environment Variables

Click "Environment" and add:

```
DEBUG=False
SECRET_KEY=<generate-strong-key>
ALLOWED_HOSTS=video-project.onrender.com
DATABASE_URL=<will-be-filled-by-Postgres>
```

### 5. Add Postgres Database

- Render dashboard → "New" → "PostgreSQL"
- Connect to your web service
- Note: DATABASE_URL auto-populated

### 6. Deploy

Click "Deploy" and wait ~2 minutes. Your app goes live! 🎉

---

## **Troubleshooting**

### 500 Error
- Check logs in platform dashboard
- Verify `SECRET_KEY` and `ALLOWED_HOSTS`
- Run `python manage.py check` locally

### Database Connection Failed
- Verify `DATABASE_URL` format
- Check database credentials
- Ensure database is running

### Static Files Not Loading
- Run `python manage.py collectstatic --noinput` locally to test
- Verify `STATIC_ROOT` and `STATIC_URL` in settings

### Video Upload Not Working
- Check `MEDIA_ROOT` and `MEDIA_URL`
- For production: use **AWS S3** (see below)

---

## **Production Video Storage (AWS S3)**

For serving video files at scale, configure **Django Storages + S3**:

### Install:
```bash
pip install django-storages boto3
```

### Update `settings_prod.py`:
```python
STORAGES = {
    'default': {
        'BACKEND': 'storages.backends.s3boto3.S3Boto3Storage',
        'OPTIONS': {
            'AWS_STORAGE_BUCKET_NAME': 'your-bucket-name',
            'AWS_S3_REGION_NAME': 'us-east-1',
            'AWS_ACCESS_KEY_ID': os.getenv('AWS_ACCESS_KEY_ID'),
            'AWS_SECRET_ACCESS_KEY': os.getenv('AWS_SECRET_ACCESS_KEY'),
        }
    }
}
```

### Set env vars on Render/Railway:
```
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
```

---

## **Choose and Start**

Pick **Render** or **Railway** above and start deploying now! You can switch platforms later if needed.

Questions? Check your platform's documentation or contact their support.

Good luck! 🚀
