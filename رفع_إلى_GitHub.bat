@echo off
echo ========================================
echo   رفع المشروع إلى GitHub
echo ========================================
echo.

REM التحقق من Git
git --version >nul 2>&1
if errorlevel 1 (
    echo [خطأ] Git غير مثبت!
    echo يرجى تثبيت Git من: https://git-scm.com/
    pause
    exit /b 1
)

echo [1/7] تهيئة Git...
git init

echo.
echo [2/7] إضافة جميع الملفات...
git add .

echo.
echo [3/7] إنشاء Commit...
git commit -m "Initial commit: Video sharing project with Django - Ready for Render deployment"

echo.
echo [4/7] إضافة Remote Repository...
git remote remove origin 2>nul
git remote add origin https://github.com/Omaralmstafa/video.git

echo.
echo [5/7] التحقق من Remote...
git remote -v

echo.
echo [6/7] تغيير Branch إلى main...
git branch -M main

echo.
echo [7/7] رفع المشروع إلى GitHub...
echo.
echo يرجى إدخال بيانات GitHub:
echo - اسم المستخدم: Omaralmstafa
echo - كلمة المرور: استخدم Personal Access Token
echo.
echo إذا لم يكن لديك Token:
echo 1. اذهب إلى: https://github.com/settings/tokens
echo 2. اضغط "Generate new token (classic)"
echo 3. اختر الصلاحيات: repo
echo 4. انسخ الـ Token واستخدمه ككلمة مرور
echo.
pause

git push -u origin main

if errorlevel 1 (
    echo.
    echo [خطأ] فشل الرفع!
    echo.
    echo الحلول المقترحة:
    echo 1. تحقق من اسم المستخدم وكلمة المرور
    echo 2. استخدم Personal Access Token بدلاً من كلمة المرور
    echo 3. تأكد من وجود المستودع على GitHub
    echo.
) else (
    echo.
    echo ========================================
    echo   ✓ تم رفع المشروع بنجاح!
    echo ========================================
    echo.
    echo يمكنك الآن زيارة:
    echo https://github.com/Omaralmstafa/video
    echo.
)

pause

