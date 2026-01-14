# شرح ملف upload.html

## الموقع
`video_share/templates/video_share/upload.html`

## الوظيفة
صفحة HTML لرفع فيديوهات جديدة. تدعم السحب والإفلات، المعاينة، ومؤشر التقدم.

---

## البنية الأساسية

### 1. النموذج (Form)
```html
<form id="uploadForm" enctype="multipart/form-data">
  <input type="hidden" name="csrfmiddlewaretoken" value="{{ csrf_token }}">
  <input type="file" id="videoFile" name="video" accept="video/*" required>
</form>
```

**الخصائص:**
- `enctype="multipart/form-data"`: مطلوب لرفع الملفات
- `csrfmiddlewaretoken`: حماية CSRF
- `accept="video/*"`: يقبل ملفات الفيديو فقط
- `required`: إلزامي

---

## منطقة الرفع (Upload Area)

### 1. HTML
```html
<div class="upload-area" id="uploadArea">
  <div class="upload-icon">🎬</div>
  <h3>اسحب الفيديو هنا</h3>
  <p>أو انقر للاختيار من جهازك</p>
  <div class="file-types">MP4, WebM, MOV • حتى 500 ميجا</div>
  <input type="file" id="videoFile" name="video" accept="video/*" required>
</div>
```

**الوظيفة:**
- منطقة مرئية للسحب والإفلات
- زر مخفي لاختيار الملف

---

### 2. JavaScript - السحب والإفلات
```javascript
uploadArea.addEventListener('dragover', (e) => {
  e.preventDefault();
  uploadArea.classList.add('dragover');
});

uploadArea.addEventListener('drop', (e) => {
  e.preventDefault();
  uploadArea.classList.remove('dragover');
  if (e.dataTransfer.files.length) {
    handleFileSelect(e.dataTransfer.files[0]);
  }
});
```

**الشرح:**
- `dragover`: عند السحب فوق المنطقة
- `drop`: عند إفلات الملف
- `preventDefault()`: يمنع السلوك الافتراضي (فتح الملف)

---

## اختيار الملف

### 1. النقر على المنطقة
```javascript
uploadArea.addEventListener('click', () => {
  videoFile.click();
});
```

**الوظيفة:**
- عند النقر على المنطقة، يفتح نافذة اختيار الملف

---

### 2. تغيير الملف
```javascript
videoFile.addEventListener('change', (e) => {
  if (e.target.files.length) {
    handleFileSelect(e.target.files[0]);
  }
});
```

---

## معالجة الملف المختار

### 1. handleFileSelect()
```javascript
function handleFileSelect(file) {
  // التحقق من النوع
  if (!file.type.startsWith('video/')) {
    showMessage('الرجاء اختيار ملف فيديو', 'error');
    return;
  }
  
  // التحقق من الحجم (500 MB)
  const maxSize = 500 * 1024 * 1024;
  if (file.size > maxSize) {
    showMessage('حجم الملف يجب أن يكون أقل من 500 ميجا', 'error');
    return;
  }
  
  selectedFile = file;
  
  // عرض معلومات الملف
  const size = (file.size / (1024 * 1024)).toFixed(2);
  fileName.textContent = file.name;
  fileDetails.textContent = `${size} ميجا • ${file.type.split('/')[1].toUpperCase()}`;
  
  // معاينة الفيديو
  const url = URL.createObjectURL(file);
  previewVideo.src = url;
  previewContainer.classList.add('show');
  uploadArea.style.display = 'none';
}
```

**الخطوات:**
1. التحقق من نوع الملف
2. التحقق من الحجم
3. حفظ الملف
4. عرض المعلومات
5. عرض المعاينة

---

## معاينة الفيديو

### 1. HTML
```html
<div class="preview-container" id="previewContainer">
  <video class="preview-video" id="previewVideo" controls muted></video>
  <div class="preview-overlay">
    <div class="file-name" id="fileName"></div>
    <div class="file-details" id="fileDetails"></div>
  </div>
  <button type="button" class="change-video" id="changeVideo">تغيير الفيديو</button>
</div>
```

**الخصائص:**
- `controls`: أزرار التحكم
- `muted`: صامت (للتشغيل التلقائي)

---

### 2. عرض المعاينة
```javascript
const url = URL.createObjectURL(file);
previewVideo.src = url;
```

**الشرح:**
- `URL.createObjectURL()`: ينشئ رابط مؤقت للملف
- يجب تحرير الرابط بعد الاستخدام: `URL.revokeObjectURL(url)`

---

## رفع الفيديو

### 1. إرسال النموذج
```javascript
uploadForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  
  if (!selectedFile) {
    showMessage('الرجاء اختيار ملف فيديو', 'error');
    return;
  }
  
  const formData = new FormData();
  formData.append('video', selectedFile);
  
  // ... إرسال الطلب
});
```

**الشرح:**
- `preventDefault()`: يمنع إرسال النموذج العادي
- `FormData`: كائن لإرسال الملفات
- `append('video', file)`: يضيف الملف

---

### 2. XMLHttpRequest مع التقدم
```javascript
const xhr = new XMLHttpRequest();

// تتبع التقدم
xhr.upload.addEventListener('progress', (e) => {
  if (e.lengthComputable) {
    const percent = Math.round((e.loaded / e.total) * 100);
    progressBarFill.style.width = percent + '%';
    progressPercent.textContent = percent + '%';
  }
});

// عند الانتهاء
xhr.addEventListener('load', () => {
  if (xhr.status === 200) {
    const response = JSON.parse(xhr.responseText);
    showMessage('✓ تم رفع الفيديو بنجاح!', 'success');
    setTimeout(() => {
      window.location.href = '{% url "video_share:video_list" %}';
    }, 1500);
  }
});

// إرسال الطلب
const csrftoken = getCookie('csrftoken');
xhr.open('POST', '{% url "video_share:upload_video" %}');
xhr.setRequestHeader('X-CSRFToken', csrftoken);
xhr.send(formData);
```

**الشرح:**
- `xhr.upload.addEventListener('progress')`: يتتبع تقدم الرفع
- `xhr.setRequestHeader('X-CSRFToken')`: يضيف CSRF token
- `xhr.send(formData)`: يرسل البيانات

---

## شريط التقدم (Progress Bar)

### 1. HTML
```html
<div class="progress-container" id="progressContainer">
  <div class="progress-label">
    <span>جاري الرفع...</span>
    <span id="progressPercent">0%</span>
  </div>
  <div class="progress-bar">
    <div class="progress-bar-fill" id="progressBarFill"></div>
  </div>
</div>
```

---

### 2. التحديث
```javascript
xhr.upload.addEventListener('progress', (e) => {
  if (e.lengthComputable) {
    const percent = Math.round((e.loaded / e.total) * 100);
    progressBarFill.style.width = percent + '%';
    progressPercent.textContent = percent + '%';
  }
});
```

---

## الرسائل (Messages)

### 1. HTML
```html
<div class="message" id="message"></div>
```

### 2. JavaScript
```javascript
function showMessage(text, type) {
  message.textContent = text;
  message.className = `message ${type} show`;
}
```

**الأنواع:**
- `success`: نجاح (أخضر)
- `error`: خطأ (أحمر)
- `info`: معلومات (أزرق)

---

## CSS المهم

### 1. منطقة الرفع
```css
.upload-area {
  border: 3px dashed #d1d5db;
  border-radius: 16px;
  padding: 50px 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
}

.upload-area:hover,
.upload-area.dragover {
  border-color: #667eea;
  background: #f0f4ff;
}
```

**الشرح:**
- `dashed`: حدود متقطعة
- `cursor: pointer`: مؤشر يد
- `.dragover`: عند السحب فوقها

---

### 2. معاينة الفيديو
```css
.preview-container {
  display: none;
  margin-top: 20px;
  border-radius: 16px;
  overflow: hidden;
}

.preview-container.show {
  display: block;
}
```

---

### 3. شريط التقدم
```css
.progress-bar {
  width: 100%;
  height: 8px;
  background: #e0e0e0;
  border-radius: 4px;
  overflow: hidden;
}

.progress-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  width: 0%;
  transition: width 0.3s;
}
```

---

## CSRF Token

### 1. الحصول على Token
```javascript
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) {
    return parts.pop().split(';').shift();
  }
  return '';
}

const csrftoken = getCookie('csrftoken');
```

**الشرح:**
- Django يضع CSRF token في cookie
- يجب إرساله مع كل طلب POST

---

## التحقق من الملف

### 1. النوع
```javascript
if (!file.type.startsWith('video/')) {
  showMessage('الرجاء اختيار ملف فيديو', 'error');
  return;
}
```

### 2. الحجم
```javascript
const maxSize = 500 * 1024 * 1024; // 500 MB
if (file.size > maxSize) {
  showMessage('حجم الملف يجب أن يكون أقل من 500 ميجا', 'error');
  return;
}
```

---

## ملاحظات مهمة

1. **الحجم**: حد أقصى 500 MB (يمكن تعديله)
2. **النوع**: يقبل جميع أنواع الفيديو
3. **CSRF**: مطلوب للأمان
4. **التقدم**: يعرض نسبة الرفع
5. **المعاينة**: قبل الرفع

---

## تحسينات محتملة

### 1. ضغط الفيديو
```javascript
// استخدام WebCodecs API
```

### 2. رفع متعدد
```javascript
// رفع عدة فيديوهات دفعة واحدة
```

### 3. استئناف الرفع
```javascript
// إذا انقطع الاتصال، استئناف من حيث توقف
```

### 4. التحقق من المحتوى
```javascript
// فحص الفيديو قبل الرفع (مثل NSFW)
```

