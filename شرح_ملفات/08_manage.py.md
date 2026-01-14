# شرح ملف manage.py

## الموقع
`manage.py` (في جذر المشروع)

## الوظيفة
أداة سطر الأوامر لإدارة مشروع Django. يوفر أوامر لإدارة قاعدة البيانات، التطبيقات، الخادم، وغيرها.

---

## شرح الكود

### 1. تعريف الملف
```python
#!/usr/bin/env python
```

**الوظيفة:**
- يحدد أن الملف قابل للتنفيذ
- على Linux/Mac: يمكن تشغيله مباشرة `./manage.py`

---

### 2. الوظيفة الرئيسية
```python
def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'video_project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed..."
        ) from exc
    execute_from_command_line(sys.argv)
```

**الشرح:**
1. **`os.environ.setdefault`**: يحدد إعدادات Django (settings.py)
2. **`execute_from_command_line`**: ينفذ الأوامر من سطر الأوامر
3. **`sys.argv`**: قائمة الأوامر المدخلة

**مثال:**
```bash
python manage.py runserver
# sys.argv = ['manage.py', 'runserver']
```

---

## الأوامر الأساسية

### 1. تشغيل الخادم
```bash
python manage.py runserver
```

**الوظيفة:**
- يشغل خادم التطوير
- الوصول: `http://127.0.0.1:8000/`

**خيارات:**
```bash
# على منفذ محدد
python manage.py runserver 8080

# على جميع الواجهات
python manage.py runserver 0.0.0.0:8000
```

---

### 2. إنشاء migrations
```bash
python manage.py makemigrations
```

**الوظيفة:**
- ينشئ ملفات migration عند تعديل النماذج
- يفحص التغييرات في `models.py`

**مثال:**
```python
# بعد تعديل models.py
python manage.py makemigrations
# Output: Migrations for 'video_share':
#         0002_add_category.py
```

---

### 3. تطبيق migrations
```bash
python manage.py migrate
```

**الوظيفة:**
- يطبق التغييرات على قاعدة البيانات
- ينشئ الجداول أو يعدلها

**مثال:**
```bash
python manage.py migrate
# Operations to perform:
#   Apply all migrations: admin, auth, contenttypes, sessions, video_share
# Running migrations:
#   Applying video_share.0001_initial... OK
```

---

### 4. إنشاء مستخدم إداري
```bash
python manage.py createsuperuser
```

**الوظيفة:**
- ينشئ مستخدم بصلاحيات إدارية كاملة
- للوصول إلى `/admin/`

**المطلوب:**
- اسم المستخدم
- البريد الإلكتروني (اختياري)
- كلمة المرور

---

### 5. جمع الملفات الثابتة
```bash
python manage.py collectstatic
```

**الوظيفة:**
- يجمع جميع الملفات الثابتة في `staticfiles/`
- مطلوب قبل النشر

**الاستخدام:**
```bash
python manage.py collectstatic --noinput
# --noinput: لا يسأل عن التأكيد
```

---

### 6. shell - Python shell مع Django
```bash
python manage.py shell
```

**الوظيفة:**
- يفتح Python shell مع Django محمّل
- مفيد للاختبار والتصحيح

**مثال:**
```python
>>> from video_share.models import Video
>>> Video.objects.all()
<QuerySet [<Video: فيديو 1>, <Video: فيديو 2>]>
>>> video = Video.objects.get(id=1)
>>> video.title
'فيديو رائع'
```

---

### 7. showmigrations - عرض حالة migrations
```bash
python manage.py showmigrations
```

**الوظيفة:**
- يعرض جميع migrations وحالتها
- [X] = مطبقة
- [ ] = غير مطبقة

**مثال:**
```
admin
 [X] 0001_initial
 [X] 0002_logentry_remove_auto_add
video_share
 [X] 0001_initial
 [ ] 0002_add_category
```

---

### 8. sqlmigrate - عرض SQL للـ migration
```bash
python manage.py sqlmigrate video_share 0001
```

**الوظيفة:**
- يعرض SQL الذي سينفذ
- مفيد للفهم والتصحيح

---

### 9. dbshell - فتح shell قاعدة البيانات
```bash
python manage.py dbshell
```

**الوظيفة:**
- يفتح shell لقاعدة البيانات
- SQLite: `sqlite3`
- PostgreSQL: `psql`

---

### 10. test - تشغيل الاختبارات
```bash
python manage.py test
```

**الوظيفة:**
- يشغل جميع الاختبارات في المشروع
- يبحث عن ملفات `tests.py`

---

## الأوامر المتقدمة

### 1. check - فحص المشروع
```bash
python manage.py check
```

**الوظيفة:**
- يفحص المشروع بحثاً عن أخطاء
- يتحقق من الإعدادات، النماذج، URLs

---

### 2. diffsettings - مقارنة الإعدادات
```bash
python manage.py diffsettings
```

**الوظيفة:**
- يعرض جميع الإعدادات مع القيم
- مفيد للتصحيح

---

### 3. flush - مسح قاعدة البيانات
```bash
python manage.py flush
```

**الوظيفة:**
- يحذف جميع البيانات
- يحتفظ بالهيكل (الجداول)

**تحذير:** هذا يحذف جميع البيانات!

---

### 4. loaddata - تحميل بيانات
```bash
python manage.py loaddata fixtures.json
```

**الوظيفة:**
- يحمّل بيانات من ملف JSON
- مفيد لبيانات الاختبار

---

### 5. dumpdata - تصدير بيانات
```bash
python manage.py dumpdata video_share > videos.json
```

**الوظيفة:**
- يصدر البيانات إلى JSON
- مفيد للنسخ الاحتياطي

---

## أمثلة على الاستخدام اليومي

### سيناريو 1: بدء مشروع جديد
```bash
# 1. إنشاء migrations
python manage.py makemigrations

# 2. تطبيق migrations
python manage.py migrate

# 3. إنشاء مستخدم إداري
python manage.py createsuperuser

# 4. تشغيل الخادم
python manage.py runserver
```

---

### سيناريو 2: تعديل النماذج
```bash
# 1. عدّل models.py
# 2. أنشئ migration
python manage.py makemigrations

# 3. راجع SQL (اختياري)
python manage.py sqlmigrate video_share 0002

# 4. طبّق migration
python manage.py migrate
```

---

### سيناريو 3: قبل النشر
```bash
# 1. فحص المشروع
python manage.py check

# 2. جمع الملفات الثابتة
python manage.py collectstatic --noinput

# 3. تطبيق migrations
python manage.py migrate

# 4. تصدير البيانات (اختياري)
python manage.py dumpdata > backup.json
```

---

## نصائح للاستخدام

1. **استخدم help**: `python manage.py help <command>`
2. **راجع الأخطاء**: Django يعطي رسائل واضحة
3. **احتفظ بنسخ**: قبل `migrate` أو `flush`
4. **استخدم shell**: للاختبار السريع

---

## ملاحظات مهمة

1. **يجب أن يكون في جذر المشروع**: `manage.py` يجب أن يكون في نفس مستوى `video_project/`
2. **يحتاج Python**: تأكد من تثبيت Python
3. **يحتاج Django**: تأكد من تثبيت Django
4. **يحتاج قاعدة بيانات**: تأكد من تطبيق migrations

---

## استكشاف الأخطاء

### مشكلة: ModuleNotFoundError
```bash
# تأكد من تفعيل البيئة الافتراضية
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### مشكلة: No such table
```bash
# طبّق migrations
python manage.py migrate
```

### مشكلة: Command not found
```bash
# استخدم python بدلاً من python3
python manage.py runserver
```

