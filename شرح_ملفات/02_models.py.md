# شرح ملف models.py

## الموقع
`video_share/models.py`

## الوظيفة
يحدد بنية قاعدة البيانات. كل class يمثل جدول في قاعدة البيانات.

---

## النموذج الرئيسي: Video

### تعريف النموذج
```python
class Video(models.Model):
    """نموذج الفيديو في قاعدة البيانات"""
```

### الحقول (Fields)

#### 1. العنوان (title)
```python
title = models.CharField(
    max_length=200,
    verbose_name='العنوان',
    help_text='عنوان الفيديو'
)
```
- نوع: نص قصير (CharField)
- الطول الأقصى: 200 حرف
- إلزامي: نعم (افتراضياً)

#### 2. الوصف (description)
```python
description = models.TextField(
    blank=True,
    null=True,
    verbose_name='الوصف',
    help_text='وصف الفيديو (اختياري)'
)
```
- نوع: نص طويل (TextField)
- اختياري: نعم (blank=True, null=True)

#### 3. ملف الفيديو (file)
```python
file = models.FileField(
    upload_to='videos/',
    verbose_name='ملف الفيديو'
)
```
- نوع: ملف (FileField)
- يتم حفظه في: `media/videos/`
- إلزامي: نعم

#### 4. الصورة المصغرة (thumbnail)
```python
thumbnail = models.ImageField(
    upload_to='thumbnails/',
    blank=True,
    null=True,
    verbose_name='صورة مصغرة'
)
```
- نوع: صورة (ImageField)
- يتم حفظه في: `media/thumbnails/`
- اختياري: نعم

#### 5. تاريخ التحميل (uploaded_at)
```python
uploaded_at = models.DateTimeField(
    auto_now_add=True,
    verbose_name='تاريخ التحميل'
)
```
- نوع: تاريخ ووقت (DateTimeField)
- يُضبط تلقائياً عند الإنشاء (auto_now_add=True)

#### 6. تاريخ التحديث (updated_at)
```python
updated_at = models.DateTimeField(
    auto_now=True,
    verbose_name='تاريخ التحديث'
)
```
- نوع: تاريخ ووقت (DateTimeField)
- يُحدّث تلقائياً عند كل تعديل (auto_now=True)

#### 7. عدد المشاهدات (views)
```python
views = models.IntegerField(
    default=0,
    verbose_name='عدد المشاهدات'
)
```
- نوع: عدد صحيح (IntegerField)
- القيمة الافتراضية: 0

#### 8. عدد الإعجابات (likes)
```python
likes = models.IntegerField(
    default=0,
    verbose_name='عدد الإعجابات'
)
```
- نوع: عدد صحيح (IntegerField)
- القيمة الافتراضية: 0

#### 9. حالة النشر (is_published)
```python
is_published = models.BooleanField(
    default=True,
    verbose_name='منشور'
)
```
- نوع: منطقي (BooleanField)
- القيمة الافتراضية: True (منشور)

---

## إعدادات النموذج (Meta)

```python
class Meta:
    ordering = ['-uploaded_at']  # ترتيب حسب التاريخ (الأحدث أولاً)
    verbose_name = 'فيديو'  # الاسم في لوحة الإدارة
    verbose_name_plural = 'فيديوهات'  # الاسم في الجمع
```

---

## الدوال المساعدة (Methods)

### 1. __str__
```python
def __str__(self):
    return self.title
```
- يُستخدم لعرض اسم الفيديو في لوحة الإدارة
- مثال: "فيديو رائع"

### 2. get_url
```python
def get_url(self):
    """الحصول على رابط الفيديو"""
    return self.file.url
```
- يُرجع رابط الوصول لملف الفيديو
- مثال: `/media/videos/video1.mp4`

### 3. increment_views
```python
def increment_views(self):
    """زيادة عدد المشاهدات"""
    self.views += 1
    self.save(update_fields=['views'])
```
- يزيد عدد المشاهدات بواحد
- يحفظ التغيير في قاعدة البيانات
- `update_fields=['views']` يحفظ الحقل المحدد فقط (أسرع)

### 4. toggle_like
```python
def toggle_like(self):
    """تبديل الإعجاب"""
    self.likes += 1 if self.likes >= 0 else -1
    self.save(update_fields=['likes'])
```
- يزيد الإعجابات (يمكن تحسينه ليدعم إلغاء الإعجاب)

---

## كيفية الاستخدام

### إنشاء فيديو جديد
```python
video = Video.objects.create(
    title='فيديو رائع',
    description='وصف الفيديو',
    file=uploaded_file
)
```

### جلب الفيديوهات
```python
# جميع الفيديوهات المنشورة
videos = Video.objects.filter(is_published=True)

# فيديو محدد
video = Video.objects.get(id=1)

# ترتيب حسب المشاهدات
videos = Video.objects.order_by('-views')
```

### تحديث فيديو
```python
video = Video.objects.get(id=1)
video.views += 1
video.save()
```

### حذف فيديو
```python
video = Video.objects.get(id=1)
video.delete()
```

---

## العلاقات مع الجداول الأخرى

حالياً النموذج بسيط ولا يحتوي على علاقات. يمكن إضافة:
- علاقة مع المستخدم (ForeignKey)
- علاقة مع التصنيفات (ManyToMany)
- علاقة مع التعليقات (ForeignKey)

---

## ملاحظات مهمة

1. بعد تعديل النموذج، يجب إنشاء migration:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. الملفات المرفوعة تُحفظ في `media/` حسب `upload_to`

3. استخدم `blank=True` للحقول الاختيارية في النماذج

4. استخدم `null=True` للحقول التي يمكن أن تكون فارغة في قاعدة البيانات

