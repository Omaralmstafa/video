# شرح ملف video_detail.html

## الموقع
`video_share/templates/video_share/video_detail.html`

## الوظيفة
صفحة HTML تعرض تفاصيل فيديو واحد: المشغل، العنوان، الوصف، الإحصائيات، والأزرار.

---

## البنية الأساسية

### 1. رأس الصفحة
```html
<title>{{ video.title }} - ريلز</title>
```

**الشرح:**
- يعرض عنوان الفيديو في عنوان الصفحة
- `{{ video.title }}`: عنوان الفيديو من Django

---

### 2. الهيدر
```html
<div class="header">
  <a href="{% url 'video_share:video_list' %}" class="back-btn">←</a>
  <h1>{{ video.title }}</h1>
  <div style="width: 40px;"></div>
</div>
```

**الوظيفة:**
- زر للعودة للقائمة
- عنوان الفيديو
- مساحة فارغة للتوازن

---

## مشغل الفيديو

### 1. HTML
```html
<div class="video-player">
  <video controls preload="metadata" playsinline>
    <source src="{% url 'video_share:stream_video' video.id %}" type="video/mp4">
    متصفحك لا يدعم تشغيل الفيديو
  </video>
</div>
```

**الخصائص:**
- `controls`: أزرار التحكم (تشغيل، إيقاف، صوت، إلخ)
- `preload="metadata"`: يحمّل معلومات الفيديو فقط
- `playsinline`: تشغيل داخل الصفحة (iOS)

**المصدر:**
- `{% url 'video_share:stream_video' video.id %}`: رابط بث الفيديو
- يدعم Range requests للتنقل في الفيديو

---

## تفاصيل الفيديو

### 1. العنوان
```html
<h2 class="video-title">{{ video.title }}</h2>
```

---

### 2. الإحصائيات (Meta)
```html
<div class="video-meta">
  <div class="meta-item">
    <span>👁️</span>
    <span>{{ video.views }} مشاهدة</span>
  </div>
  <div class="meta-item">
    <span>❤️</span>
    <span>{{ video.likes }} إعجاب</span>
  </div>
  <div class="meta-item">
    <span>📅</span>
    <span>{{ video.uploaded_at|date:"d M Y" }}</span>
  </div>
</div>
```

**الشرح:**
- عدد المشاهدات
- عدد الإعجابات
- تاريخ التحميل (بتنسيق محدد)

---

### 3. الوصف
```html
{% if video.description %}
<div class="video-description">{{ video.description }}</div>
{% endif %}
```

**الشرح:**
- يظهر فقط إذا كان هناك وصف
- `{% if %}`: Django template tag للتحقق

---

## الأزرار (Actions)

### 1. HTML
```html
<div class="actions">
  <button class="action-btn" id="detailLikeBtn" data-id="{{ video.id }}">
    ❤️ إعجاب
  </button>
  <a href="{% url 'video_share:stream_video' video.id %}?download=true" 
     class="action-btn primary" id="detailDownloadBtn">
    ⬇️ تحميل
  </a>
</div>
```

**الوظائف:**
- **إعجاب**: يزيد عدد الإعجابات
- **تحميل**: يحمّل ملف الفيديو

---

## JavaScript - الإعجاب

### 1. معالج الإعجاب
```javascript
document.addEventListener('DOMContentLoaded', () => {
  const likeBtn = document.getElementById('detailLikeBtn');
  
  if (likeBtn) {
    likeBtn.addEventListener('click', async () => {
      const id = likeBtn.dataset.id;
      
      try {
        const csrftoken = getCookie('csrftoken');
        const res = await fetch(`/api/like/${id}/`, {
          method: 'POST',
          headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json'
          }
        });
        
        const data = await res.json();
        if (data.success) {
          alert('تم الإعجاب! ❤️');
          // تحديث العدد
          const likesEl = document.querySelector('.meta-item span + span');
          if (likesEl) {
            likesEl.textContent = `${data.likes} إعجاب`;
          }
        }
      } catch (e) {
        alert('حدث خطأ: ' + e);
      }
    });
  }
});
```

**الشرح:**
- `DOMContentLoaded`: يعمل بعد تحميل HTML
- `getCookie('csrftoken')`: يحصل على CSRF token
- `fetch()`: يرسل طلب POST للخادم
- يحدث العدد المحلي بعد النجاح

---

## شريط التقدم السفلي

### 1. HTML
```html
<div class="bottom-progress" id="bottomProgressDetail">
  <div class="track" id="bottomTrackDetail">
    <div class="fill" id="bottomProgressFillDetail"></div>
  </div>
  <div class="time" id="bottomTimeDetail">0:00 / 0:00</div>
</div>
```

---

### 2. JavaScript - التحديث
```javascript
if (videoEl) {
  videoEl.addEventListener('timeupdate', () => {
    const pct = (videoEl.currentTime / (videoEl.duration || 1)) * 100;
    if (bottomFill) {
      bottomFill.style.width = pct + '%';
    }
    if (bottomTime) {
      bottomTime.textContent = `${formatTime(videoEl.currentTime)} / ${formatTime(videoEl.duration)}`;
    }
  });
}
```

**الوظيفة:**
- يتتبع تقدم الفيديو
- يعرض الوقت الحالي / الوقت الكلي
- يحدث شريط التقدم

---

## التنقل في الفيديو (Seek)

### 1. النقر على الشريط
```javascript
if (bottomTrack) {
  bottomTrack.addEventListener('click', (e) => {
    const rect = bottomTrack.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const pct = Math.max(0, Math.min(1, x / rect.width));
    if (videoEl.duration) {
      videoEl.currentTime = videoEl.duration * pct;
    }
  });
}
```

**الشرح:**
- يحسب موضع النقر
- يحولها إلى نسبة مئوية
- يضع الفيديو في الوقت المطلوب

---

## زر الصوت

### 1. HTML
```html
<button id="soundBtnDetail" class="btn">🔈</button>
```

### 2. JavaScript
```javascript
if (soundBtn && videoEl) {
  soundBtn.addEventListener('click', (e) => {
    e.preventDefault();
    videoEl.muted = !videoEl.muted;
    soundBtn.textContent = videoEl.muted ? '🔈' : '🔊';
    if (!videoEl.muted) {
      videoEl.play().catch(() => {});
    }
  });
}
```

**الوظيفة:**
- يبدل بين الصامت والمسموع
- يغير الأيقونة
- يشغل الفيديو عند تفعيل الصوت

---

## CSS المهم

### 1. مشغل الفيديو
```css
.video-player {
  width: 100%;
  background: #000;
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 20px;
}

video {
  width: 100%;
  height: 100%;
  max-height: 80vh;
  object-fit: contain;
}
```

**الشرح:**
- `object-fit: contain`: يحافظ على النسبة دون قص
- `max-height: 80vh`: حد أقصى 80% من ارتفاع الشاشة

---

### 2. تفاصيل الفيديو
```css
.video-details {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
}

.video-title {
  font-size: 22px;
  font-weight: 600;
  color: #262626;
  margin-bottom: 12px;
  word-break: break-word;
}
```

---

### 3. الإحصائيات
```css
.video-meta {
  display: flex;
  gap: 20px;
  color: #65676b;
  font-size: 14px;
  margin-bottom: 16px;
  padding-bottom: 16px;
  border-bottom: 1px solid #e5e7eb;
}
```

---

### 4. الأزرار
```css
.action-btn {
  flex: 1;
  padding: 10px 16px;
  border: 1px solid #dbdbdb;
  background: #fff;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
}

.action-btn.primary {
  background: #0095f6;
  color: #fff;
  border-color: #0095f6;
}
```

---

### 5. التجاوب (Responsive)
```css
@media (max-width: 768px) {
  video {
    object-fit: cover;
    max-height: 100vh;
  }
}
```

**الشرح:**
- على الشاشات الصغيرة: يملأ الشاشة (`cover`)

---

## شريط التقدم السفلي

### 1. CSS
```css
.bottom-progress {
  position: fixed;
  left: 12px;
  right: 12px;
  bottom: 62px;
  max-width: 960px;
  margin: 0 auto;
  z-index: 41;
}

.bottom-progress .track {
  height: 6px;
  background: rgba(0,0,0,0.06);
  border-radius: 6px;
  overflow: hidden;
  cursor: pointer;
}

.bottom-progress .fill {
  height: 100%;
  background: #0095f6;
  width: 0%;
}
```

---

## دالة formatTime

```javascript
function formatTime(s) {
  if (!isFinite(s)) return '0:00';
  const m = Math.floor(s / 60);
  const sec = Math.floor(s % 60).toString().padStart(2, '0');
  return `${m}:${sec}`;
}
```

**مثال:**
- `65` → `"1:05"`
- `125` → `"2:05"`

---

## معالجة الأخطاء

### 1. فيديو غير موجود
```html
{% if video %}
  <!-- محتوى الفيديو -->
{% else %}
  <div class="error">
    ❌ الفيديو غير موجود
  </div>
{% endif %}
```

---

## ملاحظات مهمة

1. **الأداء**: `preload="metadata"` يحمّل معلومات فقط
2. **التجاوب**: يعمل على جميع الأجهزة
3. **التنقل**: يمكن التنقل بالنقر على الشريط
4. **الصوت**: يمكن التحكم بالصوت
5. **الإعجاب**: يتحدث تلقائياً بعد النجاح

---

## تحسينات محتملة

### 1. التعليقات
```html
<!-- إضافة قسم للتعليقات -->
<div class="comments">
  <!-- ... -->
</div>
```

### 2. فيديوهات مشابهة
```html
<!-- إضافة فيديوهات مشابهة -->
<div class="related-videos">
  <!-- ... -->
</div>
```

### 3. مشاركة
```html
<!-- إضافة أزرار مشاركة -->
<div class="share-buttons">
  <!-- واتساب، تيليجرام، إلخ -->
</div>
```

### 4. تقييم
```html
<!-- إضافة نظام تقييم بالنجوم -->
<div class="rating">
  <!-- ... -->
</div>
```

---

## كيفية عمل الصفحة

### 1. الطلب
```
المستخدم يطلب: http://127.0.0.1:8000/video/1/
```

### 2. المعالجة
```python
# في views.py
def video_detail(request, video_id):
    video = get_object_or_404(Video, id=video_id, is_published=True)
    return render(request, 'video_share/video_detail.html', {'video': video})
```

### 3. العرض
- Django يجلب الفيديو من قاعدة البيانات
- يمرره للقالب
- القالب يعرضه في HTML

---

## الأمان

### 1. CSRF Protection
```html
<form style="display:none">{% csrf_token %}</form>
```

**الوظيفة:**
- يضمن وجود CSRF token في الصفحة
- مطلوب للطلبات POST

---

## إمكانية الوصول (Accessibility)

### 1. ARIA Labels
```html
<button id="detailLikeBtn" aria-label="إعجاب">❤️ إعجاب</button>
```

**الوظيفة:**
- يساعد قارئات الشاشة
- يوضح وظيفة الزر

---

## ملخص

هذه الصفحة تعرض:
- ✅ مشغل فيديو كامل الميزات
- ✅ معلومات الفيديو
- ✅ إحصائيات (مشاهدات، إعجابات)
- ✅ أزرار تفاعل (إعجاب، تحميل)
- ✅ شريط تقدم
- ✅ تحكم بالصوت
- ✅ تنقل في الفيديو

