#!/bin/bash

echo "========================================"
echo "  رفع المشروع إلى GitHub"
echo "========================================"
echo ""

# التحقق من Git
if ! command -v git &> /dev/null; then
    echo "[خطأ] Git غير مثبت!"
    echo "يرجى تثبيت Git من: https://git-scm.com/"
    exit 1
fi

echo "[1/7] تهيئة Git..."
git init

echo ""
echo "[2/7] إضافة جميع الملفات..."
git add .

echo ""
echo "[3/7] إنشاء Commit..."
git commit -m "Initial commit: Video sharing project with Django - Ready for Render deployment"

echo ""
echo "[4/7] إضافة Remote Repository..."
git remote remove origin 2>/dev/null
git remote add origin https://github.com/Omaralmstafa/video.git

echo ""
echo "[5/7] التحقق من Remote..."
git remote -v

echo ""
echo "[6/7] تغيير Branch إلى main..."
git branch -M main

echo ""
echo "[7/7] رفع المشروع إلى GitHub..."
echo ""
echo "يرجى إدخال بيانات GitHub:"
echo "- اسم المستخدم: Omaralmstafa"
echo "- كلمة المرور: استخدم Personal Access Token"
echo ""

git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "========================================"
    echo "  ✓ تم رفع المشروع بنجاح!"
    echo "========================================"
    echo ""
    echo "يمكنك الآن زيارة:"
    echo "https://github.com/Omaralmstafa/video"
    echo ""
else
    echo ""
    echo "[خطأ] فشل الرفع!"
    echo ""
    echo "الحلول المقترحة:"
    echo "1. تحقق من اسم المستخدم وكلمة المرور"
    echo "2. استخدم Personal Access Token بدلاً من كلمة المرور"
    echo "3. تأكد من وجود المستودع على GitHub"
    echo ""
fi

