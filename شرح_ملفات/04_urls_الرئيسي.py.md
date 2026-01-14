# شرح ملف urls.py (الرئيسي)

## الموقع
`video_project/urls.py`

## الوظيفة
هذا هو ملف التوجيه الرئيسي للمشروع. يحدد كيفية توجيه الطلبات (URLs) إلى التطبيقات المختلفة.

---

## شرح الكود

### 1. الاستيرادات (Imports)
```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
```

- **admin**: لوحة إدارة Django
- **path, include**: وظائف لتحديد المسارات
- **settings**: إعدادات المشروع
- **static**: لخدمة الملفات الثابتة

---

### 2. قائمة المسارات (urlpatterns)
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('video_share.urls')),
]
```

#### المسار الأول: لوحة الإدارة
```python
path('admin/', admin.site.urls)
```
- **المسار**: `/admin/`
- **الوظيفة**: يفتح لوحة إدارة Django
- **الاستخدام**: لإدارة قاعدة البيانات من المتصفح

#### المسار الثاني: التطبيق الرئيسي
```python
path('', include('video_share.urls'))
```
- **المسار**: `/` (الجذر)
- **الوظيفة**: يوجه جميع الطلبات إلى `video_share.urls`
- **الاستخدام**: جميع صفحات الموقع تمر عبر هذا المسار

---

### 3. خدمة الملفات في وضع التطوير
```python
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

**الشرح:**
- يعمل فقط في وضع التطوير (`DEBUG = True`)
- يخدم ملفات الميديا (`/media/`) من مجلد `media/`
- يخدم الملفات الثابتة (`/static/`) من مجلد `staticfiles/`

**لماذا؟**
- في الإنتاج، يجب استخدام خادم ويب (nginx) أو CDN لخدمة هذه الملفات
- في التطوير، Django يخدمها تلقائياً

---

## كيفية عمل التوجيه

### مثال 1: طلب `/admin/`
```
المستخدم يطلب: http://127.0.0.1:8000/admin/
↓
Django يبحث في urlpatterns
↓
يجد: path('admin/', admin.site.urls)
↓
يوجه إلى: لوحة الإدارة
```

### مثال 2: طلب `/`
```
المستخدم يطلب: http://127.0.0.1:8000/
↓
Django يبحث في urlpatterns
↓
يجد: path('', include('video_share.urls'))
↓
ينتقل إلى: video_share/urls.py
↓
يبحث في urlpatterns هناك
```

### مثال 3: طلب `/reels/`
```
المستخدم يطلب: http://127.0.0.1:8000/reels/
↓
Django يبحث في urlpatterns الرئيسي
↓
يجد: path('', include('video_share.urls'))
↓
ينتقل إلى: video_share/urls.py
↓
يجد: path('reels/', views.video_player)
↓
يستدعي: views.video_player()
```

---

## إضافة مسارات جديدة

إذا أردت إضافة مسار جديد:

```python
from django.urls import path, include
from . import views  # إذا كان في نفس المجلد

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('video_share.urls')),
    path('api/', include('api.urls')),  # مثال: إضافة API
    path('about/', views.about),  # مثال: صفحة عن الموقع
]
```

---

## ملاحظات مهمة

1. **الترتيب مهم**: Django يبحث من الأعلى للأسفل، ضع المسارات الأكثر تحديداً أولاً

2. **include**: يستخدم لتقسيم المسارات على عدة ملفات (تنظيم أفضل)

3. **static files**: في الإنتاج، استخدم nginx أو CDN

4. **DEBUG**: تأكد من تعطيل خدمة الملفات الثابتة في الإنتاج

---

## البنية الكاملة

```
المستخدم يطلب URL
    ↓
video_project/urls.py (هذا الملف)
    ↓
يحدد أي تطبيق يجب استخدامه
    ↓
video_share/urls.py
    ↓
يحدد أي view يجب استدعاؤه
    ↓
views.py
    ↓
يعالج الطلب ويرجع response
```

---

## أمثلة على المسارات

| URL | المسار | الوظيفة |
|-----|--------|---------|
| `/admin/` | `path('admin/', ...)` | لوحة الإدارة |
| `/` | `path('', include(...))` | ينتقل لـ video_share |
| `/reels/` | في video_share/urls.py | مشغل الفيديوهات |
| `/upload/` | في video_share/urls.py | صفحة الرفع |

