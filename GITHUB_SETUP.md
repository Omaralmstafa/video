# 🚀 دليل رفع المشروع إلى GitHub

## الخطوات

### 1. التحقق من Git
```bash
git --version
```

إذا لم يكن مثبتاً، حمّله من [git-scm.com](https://git-scm.com/)

### 2. تهيئة Git في المشروع
```bash
cd video_project
git init
```

### 3. إضافة جميع الملفات
```bash
git add .
```

### 4. إنشاء Commit أولي
```bash
git commit -m "Initial commit: Video sharing project with Django"
```

### 5. إضافة Remote Repository
```bash
git remote add origin https://github.com/Omaralmstafa/video.git
```

### 6. التحقق من Remote
```bash
git remote -v
```

يجب أن ترى:
```
origin  https://github.com/Omaralmstafa/video.git (fetch)
origin  https://github.com/Omaralmstafa/video.git (push)
```

### 7. رفع المشروع
```bash
git branch -M main
git push -u origin main
```

## إذا واجهت مشاكل

### مشكلة: Authentication failed
**الحل**: استخدم Personal Access Token
1. اذهب إلى GitHub → Settings → Developer settings → Personal access tokens
2. أنشئ token جديد
3. استخدمه ككلمة مرور عند الرفع

### مشكلة: Repository not empty
**الحل**: إذا كان المستودع غير فارغ:
```bash
git pull origin main --allow-unrelated-histories
git push -u origin main
```

### مشكلة: Large files
**الحل**: تأكد من `.gitignore` يحتوي على:
- `db.sqlite3`
- `media/`
- `staticfiles/`
- `venv/`
- `__pycache__/`

## بعد الرفع

### 1. تحقق من GitHub
افتح: https://github.com/Omaralmstafa/video

### 2. أضف وصف للمستودع
- اذهب إلى Settings
- أضف وصف: "Django video sharing platform with Reels-style interface"

### 3. أضف Topics
- `django`
- `python`
- `video-sharing`
- `web-app`

### 4. أضف License
- اذهب إلى Settings → General
- اختر "Add license"
- اختر MIT License

## تحديثات مستقبلية

عند إجراء تغييرات:

```bash
git add .
git commit -m "وصف التغييرات"
git push
```

## الأوامر السريعة

```bash
# حالة الملفات
git status

# عرض التغييرات
git diff

# سجل الـ Commits
git log

# سحب التحديثات
git pull
```

---

**ملاحظة**: تأكد من عدم رفع:
- `db.sqlite3`
- ملفات `.env` (إذا كانت تحتوي على معلومات حساسة)
- مجلد `venv/`
- ملفات `__pycache__/`

