# شرح ملف video_player.html

## الموقع
`video_share/templates/video_share/video_player.html`

## الوظيفة
صفحة مشغل الفيديوهات على نمط Reels/TikTok. تعرض الفيديوهات بشكل عمودي مع إمكانية التنقل بالسحب.

---

## البنية الأساسية

### 1. البيانات من Django
```html
<script>
  const videos = JSON.parse('{{ videos_json|escapejs }}');
  let currentIndex = parseInt('{{ current_index }}' || '0', 10);
</script>
```

**الشرح:**
- `videos_json`: بيانات الفيديوهات من Django كـ JSON
- `current_index`: الفهرس الحالي للفيديو
- `escapejs`: Django filter لتهريب JavaScript (للأمان)

---

## العناصر الرئيسية

### 1. حاوية الفيديوهات
```html
<div class="reels-wrapper" id="reelsWrapper">
  <div class="reels-container" id="reelsContainer">
    {% for video in videos %}
    <div class="reel-item" data-index="{{ forloop.counter0 }}">
      <video muted autoplay playsinline loop>
        <source src="{{ video.url }}" type="video/mp4">
      </video>
    </div>
    {% endfor %}
  </div>
</div>
```

**الخصائص:**
- `muted`: صامت (مطلوب للتشغيل التلقائي)
- `autoplay`: تشغيل تلقائي
- `playsinline`: تشغيل داخل الصفحة (iOS)
- `loop`: تكرار

---

### 2. أزرار التفاعل
```html
<div class="actions-sidebar">
  <button class="action-btn" id="likeBtn">♡</button>
  <button class="action-btn" id="shareBtn">➤</button>
  <button class="action-btn" id="downloadBtn">⬇</button>
  <button class="action-btn" id="soundBtn">🔈</button>
</div>
```

**الوظائف:**
- **likeBtn**: إعجاب بالفيديو
- **shareBtn**: مشاركة الفيديو
- **downloadBtn**: تحميل الفيديو
- **soundBtn**: تشغيل/إيقاف الصوت

---

### 3. معلومات الفيديو
```html
<div class="video-info">
  <div class="video-title" id="videoTitle">{{ videos.0.title }}</div>
  <div class="video-description">اسحب للأعلى أو للأسفل للتنقل</div>
</div>
```

---

## JavaScript - الوظائف الرئيسية

### 1. init() - التهيئة
```javascript
function init() {
  reelItems = Array.from(document.querySelectorAll('.reel-item'));
  
  if (!videos || videos.length === 0) {
    showToast('لا توجد فيديوهات للعرض');
    return;
  }
  
  updateVideoPosition();
  playCurrentVideo();
}
```

**الوظيفة:**
- تجهيز العناصر
- التحقق من وجود فيديوهات
- بدء التشغيل

---

### 2. updateVideoPosition() - تحديث الموضع
```javascript
function updateVideoPosition() {
  reelItems.forEach((item, index) => {
    item.style.top = `${index * 100}vh`;
    if (index === currentIndex) {
      item.classList.add('active');
    } else {
      item.classList.remove('active');
    }
  });
  
  reelsContainer.style.transform = `translateY(-${currentIndex * 100}vh)`;
}
```

**الشرح:**
- يضع كل فيديو في موضعه (100vh لكل فيديو)
- يحدد الفيديو النشط
- يحرك الحاوية للفيديو الحالي

---

### 3. playCurrentVideo() - تشغيل الفيديو الحالي
```javascript
function playCurrentVideo() {
  reelItems.forEach((item, index) => {
    const video = item.querySelector('video');
    if (index === currentIndex) {
      video.play().catch(() => {});
    } else {
      video.pause();
      video.currentTime = 0;
    }
  });
}
```

**الوظيفة:**
- يشغل الفيديو الحالي فقط
- يوقف باقي الفيديوهات

---

### 4. goToVideo() - الانتقال لفيديو
```javascript
function goToVideo(direction) {
  if (isTransitioning) return;
  
  const newIndex = currentIndex + direction;
  if (newIndex < 0 || newIndex >= videos.length) {
    return; // لا يوجد المزيد
  }
  
  isTransitioning = true;
  currentIndex = newIndex;
  updateVideoPosition();
  playCurrentVideo();
  
  setTimeout(() => {
    isTransitioning = false;
  }, 300);
}
```

**المعامل:**
- `direction`: 1 للأسفل، -1 للأعلى

---

## التنقل (Navigation)

### 1. السحب (Touch/Swipe)
```javascript
reelsWrapper.addEventListener('touchstart', (e) => {
  touchStartY = e.touches[0].clientY;
});

reelsWrapper.addEventListener('touchend', (e) => {
  touchEndY = e.changedTouches[0].clientY;
  handleSwipe();
});

function handleSwipe() {
  const swipeDistance = touchStartY - touchEndY;
  const minSwipeDistance = 50;
  
  if (Math.abs(swipeDistance) > minSwipeDistance) {
    if (swipeDistance > 0) {
      goToVideo(1); // سحب لأعلى - التالي
    } else {
      goToVideo(-1); // سحب لأسفل - السابق
    }
  }
}
```

**الشرح:**
- يسجل نقطة البداية والنهاية
- يحسب المسافة
- ينتقل للفيديو التالي/السابق

---

### 2. عجلة الماوس (Wheel)
```javascript
reelsWrapper.addEventListener('wheel', (e) => {
  e.preventDefault();
  
  clearTimeout(wheelTimeout);
  wheelTimeout = setTimeout(() => {
    if (e.deltaY > 0) {
      goToVideo(1); // التمرير لأسفل
    } else {
      goToVideo(-1); // التمرير لأعلى
    }
  }, 100);
});
```

---

### 3. لوحة المفاتيح (Keyboard)
```javascript
document.addEventListener('keydown', (e) => {
  if (e.key === 'ArrowDown') {
    goToVideo(1);
  } else if (e.key === 'ArrowUp') {
    goToVideo(-1);
  } else if (e.key === ' ') {
    togglePlayPause();
  }
});
```

---

## التفاعلات (Interactions)

### 1. الإعجاب (Like)
```javascript
likeBtn.addEventListener('click', async () => {
  const videoId = videos[currentIndex].id;
  
  try {
    const csrftoken = getCookie('csrftoken');
    const response = await fetch(`/api/like/${videoId}/`, {
      method: 'POST',
      headers: {
        'X-CSRFToken': csrftoken,
        'Content-Type': 'application/json'
      }
    });
    
    const data = await response.json();
    if (data.success) {
      videos[currentIndex].likes = data.likes;
      updateLikeButton();
      showToast('تم الإعجاب ❤️');
    }
  } catch (e) {
    showToast('حدث خطأ');
  }
});
```

**الشرح:**
- يرسل طلب POST للخادم
- يمرر CSRF token (للأمان)
- يحدث العدد المحلي

---

### 2. المشاركة (Share)
```javascript
function openShareMenu() {
  shareMenu.classList.add('active');
  shareOverlay.classList.add('active');
}

// مشاركة واتساب
whatsappShareEl.addEventListener('click', () => {
  const videoUrl = videos[currentIndex].url;
  const text = encodeURIComponent('شاهد هذا الفيديو!');
  const url = encodeURIComponent(window.location.origin + videoUrl);
  window.open(`https://wa.me/?text=${text}${url}`, '_blank');
});
```

---

### 3. التحميل (Download)
```javascript
async function downloadVideo() {
  const videoUrl = videos[currentIndex].url;
  
  downloadProgress.classList.add('show');
  
  try {
    const response = await fetch(videoUrl);
    const blob = await response.blob();
    
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = videos[currentIndex].filename;
    a.click();
    
    showToast('اكتمل التحميل ✓');
  } catch (err) {
    showToast('فشل التحميل ✗');
  }
}
```

**الشرح:**
- يحمّل الفيديو كـ blob
- ينشئ رابط تحميل
- يبدأ التحميل تلقائياً

---

### 4. الصوت (Sound)
```javascript
function toggleSound() {
  const activeVideo = document.querySelector('.reel-item.active video');
  activeVideo.muted = !activeVideo.muted;
  
  if (activeVideo.muted) {
    soundBtn.textContent = '🔈';
  } else {
    soundBtn.textContent = '🔊';
    activeVideo.play();
  }
}
```

---

## شريط التقدم (Progress Bar)

### 1. التقدم العلوي
```javascript
video.addEventListener('timeupdate', () => {
  if (item.classList.contains('active')) {
    const progress = (video.currentTime / video.duration) * 100;
    progressBarFill.style.width = progress + '%';
  }
});
```

### 2. التقدم السفلي
```javascript
bottomTime.textContent = `${formatTime(video.currentTime)} / ${formatTime(video.duration)}`;
```

**دالة formatTime:**
```javascript
function formatTime(s) {
  const m = Math.floor(s / 60);
  const sec = Math.floor(s % 60).toString().padStart(2, '0');
  return `${m}:${sec}`;
}
```

---

## CSS المهم

### 1. التموضع
```css
.reel-item {
  position: absolute;
  width: 100%;
  height: 100vh;
  top: 0;
}
```

### 2. الانتقال
```css
.reels-container {
  transition: transform 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}
```

### 3. الفيديو
```css
video {
  width: 100%;
  height: 100%;
  object-fit: cover; /* يملأ الشاشة */
}
```

---

## ملاحظات مهمة

1. **الأداء**: يحمّل فيديو واحد فقط في كل مرة
2. **التجاوب**: يعمل على جميع الأجهزة
3. **الأمان**: CSRF protection للإعجاب
4. **التجربة**: انتقالات سلسة وتفاعل سريع

---

## تحسينات محتملة

### 1. Preload الفيديو التالي
```javascript
const nextVideo = reelItems[currentIndex + 1]?.querySelector('video');
if (nextVideo) {
  nextVideo.preload = 'auto';
}
```

### 2. Cache الفيديوهات
```javascript
// استخدام Service Worker للكاش
```

### 3. Analytics
```javascript
// تتبع المشاهدات
function trackView(videoId) {
  fetch(`/api/view/${videoId}/`, { method: 'POST' });
}
```

