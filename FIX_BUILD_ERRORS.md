# 🔧 إصلاح أخطاء البناء (Build Errors)

## المشاكل الشائعة وحلولها

### 1. خطأ في Import
**الخطأ**: `ModuleNotFoundError` أو `ImportError`

**الحل**:
- تأكد من وجود جميع المكتبات في `requirements.txt`
- تحقق من عدم وجود أخطاء في `settings.py`

### 2. خطأ في collectstatic
**الخطأ**: `CommandError: You must set settings.STATIC_ROOT`

**الحل**: تم إصلاحه في `settings.py`:
```python
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
```

### 3. خطأ في Database
**الخطأ**: `django.db.utils.OperationalError`

**الحل**:
- تأكد من إضافة `DATABASE_URL` في Environment Variables
- أو استخدم SQLite للتطوير

### 4. خطأ في Secret Key
**الخطأ**: `ImproperlyConfigured: The SECRET_KEY setting must not be empty`

**الحل**:
- أضف `SECRET_KEY` في Environment Variables في Render
- أو استخدم القيمة الافتراضية للتطوير

### 5. خطأ في Python Version
**الخطأ**: `Python version not supported`

**الحل**:
- تأكد من وجود `runtime.txt` مع الإصدار الصحيح
- Render يدعم Python 3.11+

---

## Build Command الصحيح

في Render Dashboard، استخدم:

```bash
pip install --upgrade pip && pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
```

أو استخدم `build.sh`:
```bash
chmod +x build.sh
./build.sh
```

---

## Start Command الصحيح

```bash
gunicorn video_project.wsgi:application
```

---

## Environment Variables المطلوبة

في Render Dashboard → Environment:

```
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com
DATABASE_URL=postgresql://... (من Render Database)
```

---

## التحقق من الأخطاء

### 1. تحقق من Logs
في Render Dashboard → Logs، ابحث عن:
- `ERROR`
- `Exception`
- `Traceback`

### 2. تحقق من Build Logs
- اذهب إلى Deploys → Latest Deploy → Build Logs
- ابحث عن السطر الذي فشل

### 3. تحقق من Runtime Logs
- اذهب إلى Deploys → Latest Deploy → Runtime Logs
- تحقق من أخطاء التشغيل

---

## حلول سريعة

### إذا فشل pip install:
```bash
# أضف في Build Command:
pip install --upgrade pip setuptools wheel
```

### إذا فشل collectstatic:
```bash
# تأكد من وجود STATIC_ROOT في settings.py
# أو استخدم:
python manage.py collectstatic --noinput --clear
```

### إذا فشل migrate:
```bash
# تأكد من DATABASE_URL
# أو استخدم:
python manage.py migrate --run-syncdb
```

---

## اختبار محلي قبل النشر

```bash
# 1. محاكاة Build
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate

# 2. محاكاة Start
gunicorn video_project.wsgi:application --bind 0.0.0.0:8000
```

---

## إذا استمرت المشكلة

1. **تحقق من Logs** في Render Dashboard
2. **انسخ رسالة الخطأ الكاملة**
3. **ابحث في Google** عن رسالة الخطأ
4. **تحقق من Django Docs**: https://docs.djangoproject.com

---

## نصائح

- ✅ استخدم `--noinput` في جميع الأوامر
- ✅ تأكد من جميع Environment Variables
- ✅ تحقق من Logs بعد كل Deploy
- ✅ اختبر محلياً قبل النشر

---

**إذا واجهت خطأ محدد، انسخ رسالة الخطأ الكاملة وسأساعدك في حلها!**

