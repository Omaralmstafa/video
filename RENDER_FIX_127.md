# 🔧 حل نهائي لخطأ 127 في Render

## المشكلة:
خطأ 127 = Command not found

## الحلول الموصى بها (بالترتيب):

### ✅ الحل 1: استخدام gunicorn مباشرة (الأبسط)

في Render Dashboard → Start Command:
```bash
gunicorn video_project.wsgi:application
```

**مهم**: Render يضيف `$PORT` تلقائياً، لا حاجة لكتابته.

### ✅ الحل 2: استخدام waitress (بديل موثوق)

**أولاً**: أضف waitress في requirements.txt:
```
waitress==3.0.0
```

**ثانياً**: في Start Command:
```bash
waitress-serve --port=$PORT video_project.wsgi:application
```

### ✅ الحل 3: استخدام python3
```bash
python3 -m gunicorn video_project.wsgi:application
```

### ✅ الحل 4: استخدام المسار الكامل
```bash
/usr/local/bin/gunicorn video_project.wsgi:application
```

---

## ⚠️ الأهم: في Render Dashboard

Render **لا يستخدم Procfile تلقائياً**! يجب تحديد Start Command في Dashboard:

1. اذهب إلى Web Service → Settings
2. ابحث عن "Start Command"
3. أدخل الأمر مباشرة هناك
4. **اترك Procfile كما هو** (للاستخدام المحلي)

---

## Start Command الموصى به لـ Render:

### الخيار الأفضل:
```bash
gunicorn video_project.wsgi:application
```

Render يضيف `--bind` و `$PORT` تلقائياً.

---

## إذا لم يعمل gunicorn:

### استخدم waitress:

1. **أضف في requirements.txt:**
```
waitress==3.0.0
```

2. **في Start Command:**
```bash
waitress-serve --port=$PORT video_project.wsgi:application
```

---

## خطوات الإصلاح الكاملة:

### 1. في Render Dashboard:
- Settings → Start Command
- أدخل: `gunicorn video_project.wsgi:application`
- احفظ

### 2. تأكد من Build Command:
```bash
pip install --upgrade pip && pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate --noinput
```

### 3. Environment Variables:
```
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-app.onrender.com
DATABASE_URL=postgresql://...
```

### 4. إعادة النشر:
- Manual Deploy → Deploy latest commit

---

## التحقق من النجاح:

في Logs يجب أن ترى:
```
[INFO] Starting gunicorn...
[INFO] Listening at: http://0.0.0.0:XXXX
```

---

## إذا استمرت المشكلة:

انسخ **رسالة الخطأ الكاملة** من Render Logs وسأساعدك.

---

**الحل الأبسط: استخدم `gunicorn video_project.wsgi:application` في Start Command في Render Dashboard!**

