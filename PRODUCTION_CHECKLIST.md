# ✅ Production Deployment Checklist

Use this checklist before deploying to production.

---

## Security

- [ ] `DEBUG = False` in production settings
- [ ] `SECRET_KEY` is long (50+ chars) and random
- [ ] `ALLOWED_HOSTS` set correctly for your domain
- [ ] CSRF tokens enabled in all forms
- [ ] HTTPS/SSL enabled (platforms provide free SSL)
- [ ] Database password is strong
- [ ] `.env` file is in `.gitignore` (not pushed)
- [ ] No hardcoded secrets in code
- [ ] Database credentials from environment variables

---

## Database

- [ ] PostgreSQL set up (or other production DB)
- [ ] Migrations applied: `python manage.py migrate`
- [ ] Database backup plan documented
- [ ] Database connection string correct
- [ ] Collations set to UTF-8
- [ ] User permissions configured (not `admin` for app)

---

## Static & Media Files

- [ ] Static files collected: `python manage.py collectstatic`
- [ ] `STATIC_ROOT` correct path
- [ ] `STATIC_URL` correct path
- [ ] `MEDIA_ROOT` correct path
- [ ] `MEDIA_URL` correct path
- [ ] WhiteNoise configured (for static serving)
- [ ] (Optional) S3/CDN configured for media

---

## Django Configuration

- [ ] `ALLOWED_HOSTS` includes all domain variants
- [ ] `CSRF_TRUSTED_ORIGINS` includes your domain
- [ ] `SESSION_COOKIE_SECURE = True`
- [ ] `SESSION_COOKIE_HTTPONLY = True`
- [ ] `SECURE_SSL_REDIRECT = True`
- [ ] `HSTS_SECONDS = 31536000`
- [ ] Email backend configured (for notifications)
- [ ] Logging configured (to track errors)
- [ ] `DEBUG = False`

---

## Server & WSGI

- [ ] WSGI server configured (gunicorn, waitress)
- [ ] Worker processes set appropriately
- [ ] Timeout values configured
- [ ] Health checks/monitoring set up
- [ ] Auto-restart on failure enabled
- [ ] Logs stored and rotated

---

## Testing

- [ ] Local testing passed (`python manage.py runserver`)
- [ ] Upload test passed (file stored correctly)
- [ ] Like API test passed (returns JSON)
- [ ] Video playback works (all formats)
- [ ] Mobile responsiveness tested
- [ ] Forms validation tested
- [ ] Error pages tested (404, 500)
- [ ] CSRF token tested in forms

---

## Monitoring & Logging

- [ ] Error logging configured
- [ ] Access logs recorded
- [ ] Performance metrics set up
- [ ] Uptime monitoring enabled
- [ ] Alert emails configured
- [ ] Log retention policy set

---

## Deployment

- [ ] Code pushed to Git repository
- [ ] Repository is private (if needed)
- [ ] Deployment platform account created
- [ ] Repository connected to platform
- [ ] Environment variables added
- [ ] Database add-on provisioned
- [ ] Build command correct
- [ ] Start command correct
- [ ] Deploy completed successfully

---

## Post-Deployment

- [ ] Domain DNS configured
- [ ] SSL certificate verified (HTTPS works)
- [ ] Tested from production URL
- [ ] All pages load (no 404 errors)
- [ ] Video upload works
- [ ] Like API responds
- [ ] Database queries perform (no timeouts)
- [ ] Static files served correctly
- [ ] Error logs empty
- [ ] Monitoring dashboard checked

---

## Performance

- [ ] Page load time < 3 seconds
- [ ] Video stream starts < 2 seconds
- [ ] Database queries indexed
- [ ] No N+1 query problems
- [ ] Caching configured (if needed)
- [ ] CDN configured for static/media (optional)

---

## Backup & Recovery

- [ ] Database backups enabled
- [ ] Backup retention policy set
- [ ] Restore procedure tested
- [ ] Code recovery plan (Git history)
- [ ] Media files backup planned

---

## Documentation

- [ ] Deployment guide written
- [ ] Troubleshooting guide created
- [ ] Admin instructions documented
- [ ] How to scale documented
- [ ] Emergency contacts listed

---

## Compliance & Legal

- [ ] Privacy policy added
- [ ] Terms of service added
- [ ] Cookies policy/banner
- [ ] GDPR compliance (if EU users)
- [ ] Data retention policy documented

---

## Ongoing Maintenance

- [ ] Weekly backup checks
- [ ] Monthly dependency updates
- [ ] Security patch monitoring
- [ ] Log review schedule
- [ ] Performance monitoring active
- [ ] User feedback mechanism

---

## Platform-Specific (Render Example)

- [ ] Render account created
- [ ] GitHub connected
- [ ] Repository selected
- [ ] Build command: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
- [ ] Start command: `gunicorn video_project.wsgi:application`
- [ ] Environment variables all set
- [ ] Postgres database provisioned
- [ ] Domain/DNS configured
- [ ] Auto-deploy on Git push enabled

---

## Troubleshooting Pre-Check

**Test locally first:**
```bash
# Check for errors
python manage.py check

# Test with production settings
DJANGO_SETTINGS_MODULE=video_project.settings_prod python manage.py check

# Collect static files
python manage.py collectstatic --noinput --clear

# Run migrations
python manage.py migrate

# Start server
gunicorn video_project.wsgi:application
```

**If errors appear:** Fix them before deploying!

---

## Go Live Safely

1. **Deploy to staging first** (if possible)
2. **Test staging URL thoroughly**
3. **Create backup** before going live
4. **Deploy to production**
5. **Monitor for 24 hours** continuously
6. **Keep rollback plan ready**

---

## Success Indicators

✅ App running on your domain  
✅ Videos upload successfully  
✅ Videos play without errors  
✅ Like/interaction buttons work  
✅ No error logs in console  
✅ Database stable  
✅ SSL certificate active  
✅ All pages load under 3 seconds  

---

## Emergency Contacts

- Platform support: Check dashboard
- Django security: https://docs.djangoproject.com/en/stable/topics/security/
- Python issues: Stack Overflow

---

**Ready to deploy? Follow the DEPLOYMENT_GUIDE.md!**
