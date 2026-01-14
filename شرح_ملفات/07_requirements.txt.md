# شرح ملف requirements.txt

## الموقع
`requirements.txt`

## الوظيفة
يحدد جميع المكتبات (packages) المطلوبة لتشغيل المشروع. يُستخدم لتثبيت التبعيات.

---

## شرح المكتبات

### 1. Django
```txt
Django==5.0
```

**الوظيفة:**
- إطار عمل Python لبناء تطبيقات الويب
- الإصدار: 5.0

**الاستخدام:**
- بناء الـ views, models, urls
- إدارة قاعدة البيانات
- معالجة الطلبات والاستجابات

---

### 2. django-cors-headers
```txt
django-cors-headers==4.3.1
```

**الوظيفة:**
- يسمح للطلبات من نطاقات أخرى (Cross-Origin Resource Sharing)
- مفيد عند استخدام API من JavaScript في نطاق مختلف

**الاستخدام:**
- في `settings.py`: `INSTALLED_APPS` و `MIDDLEWARE`
- يضيف headers للسماح بالطلبات من أي نطاق

**مثال:**
```python
# في settings.py
INSTALLED_APPS = [
    'corsheaders',
    # ...
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    # ...
]

CORS_ALLOW_ALL_ORIGINS = True  # للتطوير فقط
```

---

### 3. gunicorn
```txt
gunicorn==21.2.0
```

**الوظيفة:**
- خادم WSGI لإنتاج Python
- يُستخدم لتشغيل Django في الإنتاج

**الاستخدام:**
```bash
# تشغيل المشروع
gunicorn video_project.wsgi:application

# مع خيارات
gunicorn video_project.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

**لماذا؟**
- خادم Django التطويري (`runserver`) غير مناسب للإنتاج
- Gunicorn أسرع وأكثر أماناً

---

### 4. whitenoise
```txt
whitenoise==6.6.0
```

**الوظيفة:**
- يخدم الملفات الثابتة (CSS, JS, صور) مباشرة من Django
- بديل لاستخدام nginx في الإنتاج

**الاستخدام:**
```python
# في settings.py
MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # ...
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

**المزايا:**
- يضغط الملفات تلقائياً
- يضيف headers للأداء (cache)
- لا يحتاج nginx للملفات الثابتة

---

### 5. Pillow
```txt
Pillow==10.4.0
```

**الوظيفة:**
- مكتبة لمعالجة الصور
- مطلوبة لـ `ImageField` في Django

**الاستخدام:**
- عند رفع صورة مصغرة (thumbnail) للفيديو
- Django يستخدم Pillow للتحقق من الصورة ومعالجتها

**مثال:**
```python
# في models.py
thumbnail = models.ImageField(upload_to='thumbnails/')
# Pillow مطلوب لهذا الحقل
```

---

### 6. python-decouple
```txt
python-decouple==3.8
```

**الوظيفة:**
- يقرأ المتغيرات من ملف `.env`
- مفيد لإدارة الإعدادات الحساسة

**الاستخدام:**
```python
# في settings.py
from decouple import config

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
```

**ملف `.env`:**
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
```

**المزايا:**
- لا تضع معلومات حساسة في الكود
- سهل التغيير بين التطوير والإنتاج

---

### 7. psycopg2-binary
```txt
psycopg2-binary==2.9.10
```

**الوظيفة:**
- محرك قاعدة بيانات PostgreSQL لـ Python
- مطلوب عند استخدام PostgreSQL في الإنتاج

**الاستخدام:**
```python
# في settings.py (للإنتاج)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydb',
        'USER': 'myuser',
        'PASSWORD': 'mypass',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

**ملاحظة:**
- في التطوير: SQLite (لا يحتاج psycopg2)
- في الإنتاج: PostgreSQL (يحتاج psycopg2)

---

### 8. dj-database-url
```txt
dj-database-url==1.0.0
```

**الوظيفة:**
- يحول رابط قاعدة البيانات (URL) إلى إعدادات Django
- مفيد عند النشر على منصات مثل Heroku, Render

**الاستخدام:**
```python
# في settings.py
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3'
    )
}
```

**مثال URL:**
```
postgres://user:pass@host:5432/dbname
```

---

## كيفية التثبيت

### 1. تثبيت جميع المكتبات
```bash
pip install -r requirements.txt
```

### 2. تثبيت مكتبة واحدة
```bash
pip install Django==5.0
```

### 3. تحديث requirements.txt
```bash
# بعد تثبيت مكتبة جديدة
pip freeze > requirements.txt
```

---

## إصدارات المكتبات

### لماذا تحديد الإصدار؟
```txt
Django==5.0  # إصدار محدد
```

**المزايا:**
- ضمان عمل المشروع بنفس الإصدارات
- تجنب مشاكل التوافق
- سهولة إعادة الإنتاج

**بديل:**
```txt
Django>=5.0  # 5.0 أو أحدث
Django~=5.0  # 5.0 إلى 5.9
```

---

## المكتبات الاختيارية

### للتطوير فقط
```txt
# يمكن إضافتها في requirements-dev.txt
django-debug-toolbar==4.2.0  # أداة تصحيح
pytest-django==4.7.0  # للاختبارات
```

### للإنتاج
```txt
# قد تحتاجها حسب المنصة
redis==5.0.1  # للكاش
celery==5.3.4  # للمهام الخلفية
```

---

## هيكل requirements.txt الموصى به

```txt
# الأساسيات
Django==5.0
django-cors-headers==4.3.1

# الملفات الثابتة
whitenoise==6.6.0

# الصور
Pillow==10.4.0

# الخادم
gunicorn==21.2.0

# قاعدة البيانات (للإنتاج)
psycopg2-binary==2.9.10
dj-database-url==1.0.0

# الإعدادات
python-decouple==3.8
```

---

## ملاحظات مهمة

1. **التحديثات**: راجع تحديثات الأمان بانتظام
2. **التوافق**: تأكد من توافق الإصدارات
3. **الحجم**: بعض المكتبات كبيرة (مثل Pillow)
4. **المنصة**: بعض المكتبات تعتمد على النظام (مثل psycopg2)

---

## استكشاف الأخطاء

### مشكلة: pip install فشل
```bash
# تحديث pip
python -m pip install --upgrade pip

# تثبيت بدون cache
pip install -r requirements.txt --no-cache-dir
```

### مشكلة: psycopg2 لا يعمل
```bash
# استخدم النسخة الثنائية
pip install psycopg2-binary
```

### مشكلة: Pillow لا يعمل
```bash
# على Ubuntu/Debian
sudo apt-get install libjpeg-dev zlib1g-dev

# ثم
pip install Pillow
```

---

## أفضل الممارسات

1. **حدد الإصدارات**: استخدم `==` لتحديد إصدار محدد
2. **راجع بانتظام**: تحقق من التحديثات الأمنية
3. **افصل التطوير والإنتاج**: استخدم `requirements-dev.txt`
4. **وثّق التغييرات**: اكتب سبب إضافة كل مكتبة

