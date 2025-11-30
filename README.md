# 🎬 مشروع مشاركة الفيديوهات - الريلز

مشروع Django لمشاركة ومشاهدة الفيديوهات بتصميم Reels (Instagram/TikTok)

## ✨ المميزات

- 📱 تصميم Reels متجاوب بالكامل
- ⬆️⬇️ التقليب بين الفيديوهات (Swipe)
- 📤 رفع الفيديوهات بسهولة
- 💬 مشاركة عبر واتساب وتيليجرام
- ⬇️ تحميل الفيديوهات مع شريط تقدم
- ❤️ نظام الإعجاب
- 🎯 تشغيل تلقائي

## 🚀 التثبيت والتشغيل

### 1. استنساخ المشروع
\\`\\`\\`bash
git clone <repository-url>
cd video_reels_project
\\`\\`\\`

### 2. إنشاء بيئة افتراضية
\\`\\`\\`bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\\Scripts\\activate     # Windows
\\`\\`\\`

### 3. تثبيت المكتبات
\\`\\`\\`bash
pip install -r requirements.txt
\\`\\`\\`

### 4. إنشاء المجلدات
\\`\\`\\`bash
mkdir -p media/videos
mkdir -p staticfiles
\\`\\`\\`

### 5. تطبيق الهجرات
\\`\\`\\`bash
python manage.py migrate
\\`\\`\\`

### 6. إنشاء مستخدم admin (اختياري)
\\`\\`\\`bash
python manage.py createsuperuser
\\`\\`\\`

### 7. تشغيل السيرفر
\\`\\`\\`bash
python manage.py runserver
\\`\\`\\`

### 8. فتح المتصفح
\\`\\`\\`
http://127.0.0.1:8000
\\`\\`\\`

## 📱 الاستخدام

1. **رفع فيديو**: اضغط على زر "رفع فيديو"
2. **مشاهدة الريلز**: اختر فيديو من القائمة
3. **التقليب**: اسحب لأعلى/أسفل للتنقل
4. **التفاعل**: إعجاب، مشاركة، تحميل

## 🌐 النشر على السيرفر

### Railway
\\`\\`\\`bash
railway login
railway init
railway up
\\`\\`\\`

### Render
1. ارفع المشروع على GitHub
2. اربط Render بالمستودع
3. اختر "Web Service"
4. ضع أوامر البناء من `build.sh`

## 📦 التقنيات المستخدمة

- Django 5.0
- HTML5 + CSS3
- JavaScript (Vanilla)
- Whitenoise
- Gunicorn

## 📄 الترخيص

MIT License

## 👨‍💻 المطور

تم التطوير بواسطة Claude + أنت 🚀
\\`\\`\\`

---

### 1️⃣7️⃣ إنشاء مجلد Templates
```bash
mkdir -p video_share/templates/video_share
```

ضع الملفات التالية في هذا المجلد:
- `video_list.html`
- `video_player.html`
- `upload.html`

*(استخدم الملفات التي تم إنشاؤها سابقاً)*

---

### 1️⃣8️⃣ إنشاء مجلد Media
```bash
mkdir -p media/videos
```

---

## 🚀 أوامر التشغيل السريعة
```bash
# 1. إنشاء المشروع
django-admin startproject video_project .
python manage.py startapp video_share

# 2. تطبيق التعديلات
python manage.py makemigrations
python manage.py migrate

# 3. جمع الملفات الثابتة
python manage.py collectstatic --noinput

# 4. تشغيل السيرفر
python manage.py runserver

# 5. إنشاء superuser
python manage.py createsuperuser
```

---

## 📊 هيكل قاعدة البيانات (اختياري - للمستقبل)

إذا أردت إضافة قاعدة بيانات للفيديوهات:
```python
# video_share/models.py
from django.db import models
from django.contrib.auth.models import User

class Video(models.Model):
    title = models.CharField(max_length=200, verbose_name="العنوان")
    description = models.TextField(blank=True, verbose_name="الوصف")
    file = models.FileField(upload_to='videos/', verbose_name="الملف")
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True)
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = "فيديو"
        verbose_name_plural = "فيديوهات"
    
    def __str__(self):
        return self.title

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'video')
```

---

## ✅ قائمة التحقق النهائية

- [ ] تثبيت Python 3.11+
- [ ] إنشاء البيئة الافتراضية
- [ ] تثبيت المكتبات من requirements.txt
- [ ] إنشاء مشروع Django
- [ ] نسخ جميع الملفات
- [ ] إنشاء مجلدات media و staticfiles
- [ ] تطبيق migrations
- [ ] اختبار رفع فيديو
- [ ] اختبار التقليب بين الفيديوهات
- [ ] اختبار المشاركة والتحميل

---

## 🆘 حل المشاكل الشائعة

### مشكلة: ModuleNotFoundError
```bash
pip install -r requirements.txt
```

## ⚙️ ربط Tailwind مع Django

اتّبع الخطوات التالية لإضافة Tailwind CSS وبنائه إلى `staticfiles/css/tailwind.css`:

1. ثبّت Node.js (إذا لم يكن مثبتًا).

2. من مجلد المشروع (`c:\Users\HP\video_project`) شغّل:

```powershell
# ثبّت الحزم المطلوبة
npm install

# بناء ملف CSS جاهز للإنتاج
npm run build:css

# أو تشغيل وضع التطوير مع المراقبة
npm run dev:css

# بعد بناء CSS، اجمع الملفات الثابتة (اختياري للإنتاج)
python manage.py collectstatic --noinput
```

3. سيتكوّن الملف النهائي في: `staticfiles/css/tailwind.css` وسيتم ربطه تلقائيًا في القوالب عبر `{% static 'css/tailwind.css' %}`.

ملاحظات:
- أثناء التطوير يمكنك تشغيل `npm run dev:css` لمشاهدة التغييرات مباشرة.
- إذا كنت تستخدم بيئة استضافة أو CI/CD، أضف أمر `npm run build:css` قبل `collectstatic` في سكريبت النشر.


### مشكلة: الفيديو لا يعمل
- تحقق من مسار MEDIA_ROOT
- تأكد من وجود مجلد media/videos

### مشكلة: خطأ 500
```bash
python manage.py collectstatic
DEBUG = True  # في settings.py
```

---

🎉 **الآن لديك مشروع كامل جاهز للتشغيل!**