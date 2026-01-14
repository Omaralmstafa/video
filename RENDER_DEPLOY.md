# دليل النشر على Render

## متطلبات النشر

### 1. إعدادات البيئة (Environment Variables)

في Render Dashboard، أضف المتغيرات التالية:

```
SECRET_KEY=your-very-long-random-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com
DATABASE_URL=postgresql://user:pass@host:5432/dbname
```

### 2. Build Command
```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
```

### 3. Start Command
```bash
gunicorn video_project.wsgi:application
```

### 4. Python Version
استخدم Python 3.11 أو أحدث

---

## خطوات النشر

### 1. إعداد المستودع
- ارفع الكود إلى GitHub
- تأكد من وجود جميع الملفات المطلوبة

### 2. إنشاء Web Service في Render
1. اذهب إلى [Render Dashboard](https://dashboard.render.com)
2. اضغط "New +" → "Web Service"
3. اختر المستودع الخاص بك
4. املأ المعلومات:
   - **Name**: video-project
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
   - **Start Command**: `gunicorn video_project.wsgi:application`

### 3. إضافة قاعدة بيانات PostgreSQL
1. في Render Dashboard
2. اضغط "New +" → "PostgreSQL"
3. اختر الخطة المناسبة
4. انسخ `Internal Database URL`
5. أضفه كـ `DATABASE_URL` في Environment Variables

### 4. إعداد Environment Variables
في Web Service → Environment:
```
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com
DATABASE_URL=postgresql://user:pass@host:5432/dbname
```

### 5. إنشاء Superuser
بعد النشر، استخدم Render Shell:
```bash
python manage.py createsuperuser
```

---

## ملاحظات مهمة

### 1. الملفات الثابتة
- WhiteNoise يتولى خدمة الملفات الثابتة
- تأكد من تشغيل `collectstatic` في Build Command

### 2. الملفات المرفوعة (Media)
- Render لا يحفظ الملفات المرفوعة بشكل دائم
- استخدم S3 أو خدمة تخزين خارجية للإنتاج

### 3. حجم الملفات
- Render لديه حد أقصى لحجم الملفات
- استخدم CDN للملفات الكبيرة

### 4. الأمان
- تأكد من `DEBUG=False` في الإنتاج
- استخدم `SECRET_KEY` قوي
- حدد `ALLOWED_HOSTS` بشكل صحيح

---

## استكشاف الأخطاء

### مشكلة: Static files لا تظهر
```bash
# تأكد من collectstatic في Build Command
python manage.py collectstatic --noinput
```

### مشكلة: Database connection failed
- تحقق من `DATABASE_URL`
- تأكد من أن قاعدة البيانات نشطة

### مشكلة: 500 Error
- تحقق من Logs في Render Dashboard
- تأكد من `DEBUG=False` و `ALLOWED_HOSTS`

---

## تحسينات للإنتاج

### 1. استخدام S3 للملفات
```python
# في settings.py
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_STORAGE_BUCKET_NAME = 'your-bucket-name'
```

### 2. إضافة CDN
- استخدم Cloudflare أو AWS CloudFront
- لتحسين أداء الملفات الثابتة

### 3. Monitoring
- أضف Sentry لمراقبة الأخطاء
- استخدم Render Metrics

---

## الخلاصة

المشروع جاهز للنشر على Render بعد:
- ✅ إعداد Environment Variables
- ✅ إضافة قاعدة بيانات PostgreSQL
- ✅ تعديل ALLOWED_HOSTS
- ✅ تعطيل DEBUG

