# شرح ملف wsgi.py

## الموقع
`video_project/wsgi.py`

## الوظيفة
ملف إعداد WSGI (Web Server Gateway Interface). يربط خادم الويب (مثل Gunicorn) مع تطبيق Django.

---

## شرح الكود

### 1. الوثائق
```python
"""
WSGI config for video_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""
```

**الشرح:**
- وثائق توضح وظيفة الملف
- رابط للوثائق الرسمية

---

### 2. الاستيرادات
```python
import os
from django.core.wsgi import get_wsgi_application
```

**الشرح:**
- `os`: للوصول لمتغيرات البيئة
- `get_wsgi_application`: وظيفة Django لإنشاء تطبيق WSGI

---

### 3. إعدادات Django
```python
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'video_project.settings')
```

**الوظيفة:**
- يحدد ملف الإعدادات الذي سيستخدمه Django
- `video_project.settings`: المسار لملف settings.py

**متى يُستخدم:**
- إذا لم يكن `DJANGO_SETTINGS_MODULE` محدداً مسبقاً
- `setdefault()`: يضبط فقط إذا لم يكن موجوداً

---

### 4. تطبيق WSGI
```python
application = get_wsgi_application()
```

**الوظيفة:**
- ينشئ تطبيق WSGI
- `application`: متغير قياسي يجب أن يكون بهذا الاسم
- خادم الويب (Gunicorn) يستخدمه

---

## ما هو WSGI؟

### التعريف
WSGI = Web Server Gateway Interface

**الوظيفة:**
- معيار Python لربط خوادم الويب مع تطبيقات Python
- يسمح لأي خادم ويب (Gunicorn, uWSGI) بالعمل مع Django

---

## كيفية الاستخدام

### 1. مع Gunicorn
```bash
gunicorn video_project.wsgi:application
```

**الشرح:**
- `video_project.wsgi`: المسار للملف
- `application`: المتغير في الملف

---

### 2. مع خيارات
```bash
gunicorn video_project.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 4 \
  --timeout 120
```

**الخيارات:**
- `--bind`: العنوان والمنفذ
- `--workers`: عدد العمليات
- `--timeout`: مهلة الوقت

---

### 3. في الإنتاج
```bash
# في Procfile (Heroku)
web: gunicorn video_project.wsgi:application

# في systemd (Linux)
ExecStart=/path/to/gunicorn video_project.wsgi:application
```

---

## الفرق بين WSGI و ASGI

### WSGI
- **للإنتاج الحالي**: HTTP requests فقط
- **مثال**: Gunicorn
- **استخدام**: معظم المواقع

### ASGI
- **للمستقبل**: HTTP + WebSockets
- **مثال**: Uvicorn
- **استخدام**: تطبيقات الوقت الفعلي

---

## ملاحظات مهمة

1. **لا تعدل هذا الملف**: عادة لا تحتاج لتعديله
2. **للإنتاج فقط**: في التطوير استخدم `runserver`
3. **المتغير**: يجب أن يكون اسمه `application`
4. **الإعدادات**: تأكد من `DJANGO_SETTINGS_MODULE`

---

## استكشاف الأخطاء

### مشكلة: ModuleNotFoundError
```python
# تأكد من المسار
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'video_project.settings')
```

### مشكلة: Application not found
```python
# تأكد من وجود application
application = get_wsgi_application()
```

---

## مثال كامل

```python
"""
WSGI config for video_project project.
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'video_project.settings')

application = get_wsgi_application()
```

**هذا كل شيء!** الملف بسيط جداً.

---

## استخدامات متقدمة (اختيارية)

### 1. إعدادات مختلفة
```python
# للإنتاج
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'video_project.settings_prod')
```

### 2. Middleware مخصص
```python
application = get_wsgi_application()
# يمكن إضافة middleware هنا
```

---

## الخلاصة

هذا الملف:
- ✅ بسيط جداً (5 أسطر فقط)
- ✅ يربط Django بخادم الويب
- ✅ مطلوب للنشر في الإنتاج
- ✅ لا يحتاج تعديل في معظم الحالات

