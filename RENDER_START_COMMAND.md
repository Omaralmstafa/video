# 🚀 Start Command الصحيح لـ Render

## المشكلة: خطأ 127

خطأ 127 يعني أن `gunicorn` غير موجود في PATH.

## الحلول:

### ✅ الحل 1: استخدام Python صراحة

في Render Dashboard → Start Command، استخدم:

```bash
python -m gunicorn video_project.wsgi:application --bind 0.0.0.0:$PORT
```

### ✅ الحل 2: استخدام المسار الكامل

```bash
$HOME/.local/bin/gunicorn video_project.wsgi:application --bind 0.0.0.0:$PORT
```

### ✅ الحل 3: التأكد من تثبيت gunicorn

في Build Command، تأكد من:
```bash
pip install --upgrade pip && pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate --noinput
```

---

## Start Command الموصى به:

### للـ Procfile:
```
web: python -m gunicorn video_project.wsgi:application --bind 0.0.0.0:$PORT
```

### أو في Render Dashboard:
```bash
python -m gunicorn video_project.wsgi:application --bind 0.0.0.0:$PORT
```

---

## خطوات الإصلاح:

### 1. في Render Dashboard:
1. اذهب إلى Web Service → Settings
2. ابحث عن "Start Command"
3. غيّره إلى:
   ```bash
   python -m gunicorn video_project.wsgi:application --bind 0.0.0.0:$PORT
   ```
4. احفظ التغييرات
5. اضغط "Manual Deploy"

### 2. أو حدّث Procfile:
```
web: python -m gunicorn video_project.wsgi:application --bind 0.0.0.0:$PORT
```

---

## بدائل أخرى:

### إذا لم يعمل gunicorn:

#### الخيار 1: استخدام waitress (Windows-friendly)
```bash
python -m waitress --port=$PORT video_project.wsgi:application
```

**أضف في requirements.txt:**
```
waitress==3.0.0
```

#### الخيار 2: استخدام Django runserver (للتطوير فقط)
```bash
python manage.py runserver 0.0.0.0:$PORT
```

---

## التحقق من النجاح:

بعد النشر، تحقق من Logs:
- يجب أن ترى: `Starting gunicorn...`
- يجب أن ترى: `Listening at: http://0.0.0.0:XXXX`

---

## ملاحظات:

- ✅ `$PORT` متغير بيئة من Render
- ✅ `--bind 0.0.0.0` يجعل الخادم يستمع على جميع الواجهات
- ✅ `python -m` يضمن استخدام Python الصحيح

---

**استخدم Start Command التالي في Render:**

```bash
python -m gunicorn video_project.wsgi:application --bind 0.0.0.0:$PORT
```

