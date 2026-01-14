# شرح ملف views.py

## الموقع
`video_share/views.py`

## الوظيفة
يحتوي على جميع معالجات الطلبات (views). كل دالة تستقبل request وترجع response.

---

## الدوال الرئيسية

### 1. video_list - عرض قائمة الفيديوهات

```python
def video_list(request):
    """عرض قائمة الفيديوهات من قاعدة البيانات"""
    videos = Video.objects.filter(is_published=True).order_by('-uploaded_at')
    context = {'videos': videos}
    return render(request, 'video_share/video_list.html', context)
```

**الوظيفة:**
- تجلب جميع الفيديوهات المنشورة
- ترتبها حسب تاريخ التحميل (الأحدث أولاً)
- تعرضها في صفحة HTML

**المدخلات:**
- `request`: كائن الطلب من Django

**المخرجات:**
- صفحة HTML مع قائمة الفيديوهات

---

### 2. video_player - مشغل الفيديوهات (Reels)

```python
def video_player(request, video_id=None):
    """عرض صفحة المشغل مع جميع الفيديوهات من قاعدة البيانات"""
    videos = Video.objects.filter(is_published=True).order_by('id')
    current_index = 0
    
    if video_id:
        try:
            current_video = Video.objects.get(id=video_id, is_published=True)
            current_index = list(videos.values_list('id', flat=True)).index(video_id)
        except (Video.DoesNotExist, ValueError):
            current_index = 0
```

**الوظيفة:**
- تعرض جميع الفيديوهات في واجهة Reels
- تبدأ من فيديو محدد إذا تم تمرير `video_id`
- تحول الفيديوهات إلى JSON للاستخدام في JavaScript

**المدخلات:**
- `request`: كائن الطلب
- `video_id`: معرف الفيديو (اختياري)

**المخرجات:**
- صفحة HTML مع مشغل الفيديوهات
- بيانات JSON للفيديوهات

**كيف يعمل:**
1. يجلب جميع الفيديوهات المنشورة
2. يحدد الفهرس الحالي (current_index)
3. يحول الفيديوهات إلى قائمة dictionaries
4. يمرر البيانات للقالب كـ JSON و Python list

---

### 3. stream_video - بث الفيديو

```python
def stream_video(request, video_id):
    """بث الفيديو مع دعم Range requests"""
    try:
        video = Video.objects.get(id=video_id, is_published=True)
    except Video.DoesNotExist:
        return JsonResponse({'error': 'الفيديو غير موجود'}, status=404)
    
    video_path = video.file.path
    
    if not os.path.exists(video_path):
        return JsonResponse({'error': 'ملف الفيديو غير موجود'}, status=404)
    
    video.increment_views()
```

**الوظيفة:**
- تبث الفيديو مع دعم Range requests (للتنقل في الفيديو)
- تزيد عدد المشاهدات
- تدعم التحميل الجزئي (للأداء الأفضل)

**المدخلات:**
- `request`: كائن الطلب (قد يحتوي على HTTP_RANGE)
- `video_id`: معرف الفيديو

**المخرجات:**
- استجابة بث الفيديو (StreamingHttpResponse أو FileResponse)

**كيف يعمل:**
1. يجلب الفيديو من قاعدة البيانات
2. يتحقق من وجود الملف
3. يزيد عدد المشاهدات
4. يتحقق من وجود Range request
5. إذا كان هناك Range، يرسل الجزء المطلوب فقط
6. إذا لم يكن، يرسل الملف كاملاً

**Range Request:**
- يسمح للمتصفح بطلب جزء محدد من الفيديو
- مثال: `Range: bytes=0-1024` (أول 1024 بايت)
- مفيد للتنقل في الفيديو دون تحميله كاملاً

---

### 4. upload_video - رفع فيديو جديد

```python
def upload_video(request):
    """رفع فيديو جديد إلى قاعدة البيانات"""
    if request.method == 'POST':
        title = request.POST.get('title', 'فيديو جديد')
        description = request.POST.get('description', '')
        video_file = request.FILES.get('video')
        
        if video_file:
            video = Video.objects.create(
                title=title,
                description=description,
                file=video_file,
                is_published=True
            )
            
            return JsonResponse({
                'success': True,
                'message': 'تم رفع الفيديو بنجاح',
                'video_id': video.id,
                'video_url': video.get_url()
            })
```

**الوظيفة:**
- تستقبل ملف فيديو من المستخدم
- تحفظه في قاعدة البيانات
- ترجع استجابة JSON

**المدخلات:**
- `request.POST`: البيانات النصية (title, description)
- `request.FILES`: ملف الفيديو

**المخرجات:**
- إذا POST: JSON response
- إذا GET: صفحة HTML للرفع

**كيف يعمل:**
1. يتحقق من نوع الطلب (POST أو GET)
2. إذا كان POST:
   - يجلب البيانات من الطلب
   - يتحقق من وجود ملف فيديو
   - ينشئ سجل جديد في قاعدة البيانات
   - يحفظ الملف في `media/videos/`
   - يرجع JSON بنجاح
3. إذا كان GET:
   - يعرض صفحة الرفع

---

### 5. video_detail - تفاصيل فيديو

```python
def video_detail(request, video_id):
    """عرض تفاصيل فيديو محدد"""
    video = get_object_or_404(Video, id=video_id, is_published=True)
    return render(request, 'video_share/video_detail.html', {'video': video})
```

**الوظيفة:**
- تعرض صفحة تفاصيل فيديو واحد
- تستخدم `get_object_or_404` (ترجع 404 إذا لم يوجد الفيديو)

**المدخلات:**
- `request`: كائن الطلب
- `video_id`: معرف الفيديو

**المخرجات:**
- صفحة HTML مع تفاصيل الفيديو

---

### 6. like_video - تسجيل إعجاب

```python
def like_video(request, video_id):
    """تسجيل إعجاب بالفيديو"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        video = Video.objects.get(id=video_id, is_published=True)
        video.likes += 1
        video.save()
        return JsonResponse({
            'success': True,
            'likes': video.likes
        })
    except Video.DoesNotExist:
        return JsonResponse({'error': 'الفيديو غير موجود'}, status=404)
```

**الوظيفة:**
- تزيد عدد الإعجابات على فيديو
- ترجع JSON بالعدد الجديد

**المدخلات:**
- `request`: كائن الطلب (يجب أن يكون POST)
- `video_id`: معرف الفيديو

**المخرجات:**
- JSON response مع عدد الإعجابات الجديد

**كيف يعمل:**
1. يتحقق من نوع الطلب (يجب أن يكون POST)
2. يجلب الفيديو من قاعدة البيانات
3. يزيد عدد الإعجابات
4. يحفظ التغيير
5. يرجع JSON

---

## أنواع الاستجابات المستخدمة

### 1. render - عرض HTML
```python
return render(request, 'template.html', {'data': data})
```
- يعرض قالب HTML مع البيانات

### 2. JsonResponse - استجابة JSON
```python
return JsonResponse({'success': True, 'data': data})
```
- ترجع بيانات JSON (للاستخدام مع JavaScript)

### 3. StreamingHttpResponse - بث الملفات
```python
return StreamingHttpResponse(file_iterator(), content_type='video/mp4')
```
- تبث الملفات بشكل تدريجي (للأداء الأفضل)

### 4. FileResponse - إرسال ملف
```python
return FileResponse(open(file_path, 'rb'), content_type='video/mp4')
```
- ترسل ملف كامل

### 5. get_object_or_404 - جلب كائن أو 404
```python
video = get_object_or_404(Video, id=video_id)
```
- تجلب كائن من قاعدة البيانات أو ترجع 404 إذا لم يوجد

---

## ملاحظات مهمة

1. **CSRF Protection**: Django يحمي تلقائياً من CSRF، لكن يجب إضافة token في الطلبات POST

2. **File Upload**: الملفات المرفوعة تُحفظ في `media/` حسب `upload_to` في النموذج

3. **Error Handling**: استخدم try/except للتعامل مع الأخطاء

4. **Performance**: استخدم `update_fields` عند حفظ لتحديث حقول محددة فقط

5. **Security**: تحقق دائماً من صلاحيات المستخدم قبل العمليات الحساسة

