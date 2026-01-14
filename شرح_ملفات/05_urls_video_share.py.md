# شرح ملف urls.py (video_share)

## الموقع
`video_share/urls.py`

## الوظيفة
يحدد جميع مسارات تطبيق مشاركة الفيديوهات. يربط URLs مع views.

---

## شرح الكود

### 1. الاستيرادات
```python
from django.urls import path
from . import views
```

- **path**: وظيفة لإنشاء مسار
- **views**: استيراد جميع views من نفس المجلد

---

### 2. اسم التطبيق
```python
app_name = 'video_share'
```

**الوظيفة:**
- يعطي اسم للتطبيق
- يُستخدم في القوالب: `{% url 'video_share:video_list' %}`

**الاستخدام:**
```python
# في القوالب
{% url 'video_share:video_list' %}

# في Python
reverse('video_share:video_list')
```

---

### 3. قائمة المسارات (urlpatterns)

#### المسار 1: الصفحة الرئيسية
```python
path('', views.video_list, name='video_list'),
```
- **URL**: `/` (بعد الجذر)
- **View**: `views.video_list`
- **الاسم**: `video_list`
- **الوظيفة**: يعرض قائمة الفيديوهات

**الوصول:**
```
http://127.0.0.1:8000/
```

---

#### المسار 2: مشغل الريلز (جميع الفيديوهات)
```python
path('reels/', views.video_player, name='video_player_all'),
```
- **URL**: `/reels/`
- **View**: `views.video_player`
- **الاسم**: `video_player_all`
- **الوظيفة**: يعرض مشغل الفيديوهات من البداية

**الوصول:**
```
http://127.0.0.1:8000/reels/
```

---

#### المسار 3: مشغل الريلز (فيديو محدد)
```python
path('reels/<int:video_id>/', views.video_player, name='video_player'),
```
- **URL**: `/reels/1/` (1 هو video_id)
- **View**: `views.video_player`
- **الاسم**: `video_player`
- **المعامل**: `<int:video_id>` - رقم الفيديو
- **الوظيفة**: يعرض مشغل الفيديوهات من فيديو محدد

**الوصول:**
```
http://127.0.0.1:8000/reels/5/  # يبدأ من الفيديو رقم 5
```

**كيف يعمل:**
- `<int:video_id>` يلتقط الرقم من URL
- يمرره كمعامل لـ `views.video_player(request, video_id=5)`

---

#### المسار 4: بث الفيديو
```python
path('stream/<int:video_id>/', views.stream_video, name='stream_video'),
```
- **URL**: `/stream/1/`
- **View**: `views.stream_video`
- **الوظيفة**: يبث ملف الفيديو (للتشغيل)

**الوصول:**
```html
<video src="{% url 'video_share:stream_video' video.id %}"></video>
```

**النتيجة:**
```
http://127.0.0.1:8000/stream/1/
```

---

#### المسار 5: تفاصيل الفيديو
```python
path('video/<int:video_id>/', views.video_detail, name='video_detail'),
```
- **URL**: `/video/1/`
- **View**: `views.video_detail`
- **الوظيفة**: يعرض صفحة تفاصيل فيديو واحد

**الوصول:**
```
http://127.0.0.1:8000/video/1/
```

---

#### المسار 6: إعجاب بالفيديو (API)
```python
path('api/like/<int:video_id>/', views.like_video, name='like_video'),
```
- **URL**: `/api/like/1/`
- **View**: `views.like_video`
- **الوظيفة**: API لتسجيل إعجاب (POST request)
- **الاستخدام**: يُستدعى من JavaScript

**الوصول:**
```javascript
fetch('/api/like/1/', {
    method: 'POST',
    headers: {
        'X-CSRFToken': csrftoken
    }
})
```

---

#### المسار 7: رفع فيديو
```python
path('upload/', views.upload_video, name='upload_video'),
```
- **URL**: `/upload/`
- **View**: `views.upload_video`
- **الوظيفة**: يعرض صفحة رفع فيديو (GET) أو يستقبل ملف (POST)

**الوصول:**
```
http://127.0.0.1:8000/upload/
```

---

## أنواع المعاملات في المسارات

### 1. int - عدد صحيح
```python
path('video/<int:video_id>/', ...)
```
- يلتقط: `/video/123/`
- `video_id = 123` (int)

### 2. str - نص
```python
path('user/<str:username>/', ...)
```
- يلتقط: `/user/ahmed/`
- `username = 'ahmed'` (string)

### 3. slug - نص مع شرطات
```python
path('post/<slug:slug>/', ...)
```
- يلتقط: `/post/my-awesome-post/`
- `slug = 'my-awesome-post'`

### 4. uuid - معرف فريد
```python
path('file/<uuid:file_id>/', ...)
```
- يلتقط: `/file/550e8400-e29b-41d4-a716-446655440000/`

---

## استخدام الأسماء في القوالب

### في HTML
```html
<!-- بدلاً من -->
<a href="/reels/1/">مشاهدة</a>

<!-- استخدم -->
<a href="{% url 'video_share:video_player' video.id %}">مشاهدة</a>
```

**المزايا:**
- إذا غيرت URL، لا تحتاج لتغيير القوالب
- Django يجد المسار تلقائياً

---

## استخدام الأسماء في Python

```python
from django.urls import reverse

# الحصول على URL
url = reverse('video_share:video_player', args=[1])
# النتيجة: '/reels/1/'

# إعادة توجيه
return redirect('video_share:video_list')
```

---

## ترتيب المسارات

**مهم:** Django يبحث من الأعلى للأسفل، ضع المسارات الأكثر تحديداً أولاً:

```python
# ✅ صحيح
path('reels/<int:video_id>/', ...),  # محدد
path('reels/', ...),                  # عام

# ❌ خطأ (لن يعمل reels/<int:video_id>/)
path('reels/', ...),                  # عام
path('reels/<int:video_id>/', ...),  # محدد (لن يصل له)
```

---

## خريطة المسارات الكاملة

```
/                          → video_list (قائمة الفيديوهات)
/reels/                    → video_player (مشغل من البداية)
/reels/5/                  → video_player (مشغل من فيديو 5)
/stream/5/                 → stream_video (بث الفيديو)
/video/5/                  → video_detail (تفاصيل الفيديو)
/api/like/5/               → like_video (إعجاب - POST)
/upload/                   → upload_video (رفع فيديو)
```

---

## ملاحظات مهمة

1. **الأسماء مهمة**: استخدم أسماء واضحة ووصفية
2. **app_name**: يساعد في تجنب التعارض بين التطبيقات
3. **المعاملات**: استخدم أنواع واضحة (`int`, `str`, `slug`)
4. **الترتيب**: المسارات المحددة أولاً
5. **URL patterns**: يمكن استخدام regex للمسارات المعقدة

---

## إضافة مسار جديد

```python
urlpatterns = [
    # ... المسارات الموجودة ...
    
    # مثال: صفحة بحث
    path('search/', views.search_videos, name='search'),
    
    # مثال: حذف فيديو
    path('delete/<int:video_id>/', views.delete_video, name='delete_video'),
]
```

