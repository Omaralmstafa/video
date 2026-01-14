# شرح ملف settings.py

## الموقع
`video_project/settings.py`

## الوظيفة
هذا الملف يحتوي على جميع إعدادات مشروع Django. يحدد كيفية عمل التطبيق، قواعد الأمان، قاعدة البيانات، الملفات الثابتة، وغيرها.

---

## شرح الأقسام الرئيسية

### 1. المسارات الأساسية (BASE_DIR)
```python
BASE_DIR = Path(__file__).resolve().parent.parent
```
- يحدد المجلد الرئيسي للمشروع
- يستخدم لتحديد مواقع الملفات الأخرى

### 2. الأمان (SECURITY)
```python
SECRET_KEY = 'django-insecure-your-secret-key-here-change-in-production'
DEBUG = True
ALLOWED_HOSTS = ['*']
```
- **SECRET_KEY**: مفتاح سري لتشفير الجلسات والكوكيز (يجب تغييره في الإنتاج)
- **DEBUG**: وضع التطوير (True) أو الإنتاج (False)
- **ALLOWED_HOSTS**: النطاقات المسموح بها (['*'] للتطوير فقط)

### 3. التطبيقات المثبتة (INSTALLED_APPS)
```python
INSTALLED_APPS = [
    'django.contrib.admin',      # لوحة الإدارة
    'django.contrib.auth',       # نظام المصادقة
    'django.contrib.contenttypes',
    'django.contrib.sessions',   # إدارة الجلسات
    'django.contrib.messages',   # الرسائل
    'django.contrib.staticfiles', # الملفات الثابتة
    'corsheaders',              # CORS للطلبات من نطاقات أخرى
    'video_share',               # تطبيقنا الرئيسي
]
```

### 4. البرمجيات الوسطى (MIDDLEWARE)
```python
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # CORS في البداية
    'django.middleware.security.SecurityMiddleware',  # الأمان
    'whitenoise.middleware.WhiteNoiseMiddleware',  # الملفات الثابتة
    'django.contrib.sessions.middleware.SessionMiddleware',  # الجلسات
    'django.middleware.common.CommonMiddleware',  # معالجة عامة
    'django.middleware.csrf.CsrfViewMiddleware',  # حماية CSRF
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # المصادقة
    'django.contrib.messages.middleware.MessageMiddleware',  # الرسائل
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # حماية من clickjacking
]
```
- البرمجيات الوسطى تعالج الطلبات قبل وصولها للـ views

### 5. قاعدة البيانات (DATABASES)
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```
- يستخدم SQLite للتطوير (خفيف وسهل)
- في الإنتاج يستخدم PostgreSQL

### 6. الملفات الثابتة والوسائط (STATIC & MEDIA)
```python
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```
- **STATIC**: ملفات CSS, JS, الصور الثابتة
- **MEDIA**: ملفات المستخدمين (الفيديوهات المرفوعة)

### 7. اللغة والوقت (INTERNATIONALIZATION)
```python
LANGUAGE_CODE = 'ar'  # العربية
TIME_ZONE = 'Asia/Riyadh'  # توقيت السعودية
USE_I18N = True
USE_TZ = True
```

### 8. إعدادات الرفع (FILE UPLOAD)
```python
DATA_UPLOAD_MAX_MEMORY_SIZE = 524288000  # 500 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 524288000  # 500 MB
```
- حد أقصى لحجم الملفات المرفوعة

### 9. إعدادات الأمان للإنتاج
```python
if not DEBUG:
    SECURE_SSL_REDIRECT = True  # إجبار HTTPS
    SESSION_COOKIE_SECURE = True  # الكوكيز عبر HTTPS فقط
    CSRF_COOKIE_SECURE = True  # CSRF عبر HTTPS
    SECURE_HSTS_SECONDS = 31536000  # HSTS للأمان
```

---

## ملاحظات مهمة

1. **في الإنتاج**: يجب تغيير `SECRET_KEY` و `DEBUG = False`
2. **ALLOWED_HOSTS**: حدد النطاقات الفعلية بدلاً من `['*']`
3. **قاعدة البيانات**: استخدم PostgreSQL في الإنتاج
4. **الملفات الثابتة**: استخدم CDN أو S3 في الإنتاج

---

## كيفية الاستخدام

هذا الملف يُحمّل تلقائياً عند تشغيل Django. لا تحتاج لتعديله إلا عند:
- تغيير قاعدة البيانات
- إضافة تطبيق جديد
- تغيير إعدادات الأمان

