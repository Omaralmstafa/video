# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, FileResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.conf import settings
from .models import Video
import os
import mimetypes
import json

def video_list(request):
    """عرض قائمة الفيديوهات من قاعدة البيانات"""
    videos = Video.objects.filter(is_published=True).order_by('-uploaded_at')
    context = {'videos': videos}
    return render(request, 'video_share/video_list.html', context)


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
    
    # تحويل الفيديوهات إلى تنسيق يمكن للقالب استخدامه
    videos_list = []
    for video in videos:
        videos_list.append({
            'id': video.id,
            'filename': video.file.name.split('/')[-1],
            'url': video.get_url(),
            'title': video.title,
            'description': video.description or '',
            'views': video.views,
            'likes': video.likes,
        })
    
    context = {
        # pass both Python list for template loop and JSON string for JS
        'videos': videos_list,
        'videos_json': json.dumps(videos_list, ensure_ascii=False),
        'current_index': current_index,
        'video_id': video_id or ''
    }
    return render(request, 'video_share/video_player.html', context)


def stream_video(request, video_id):
    """بث الفيديو مع دعم Range requests"""
    try:
        video = Video.objects.get(id=video_id, is_published=True)
    except Video.DoesNotExist:
        return JsonResponse({'error': 'الفيديو غير موجود'}, status=404)
    
    video_path = video.file.path
    
    if not os.path.exists(video_path):
        return JsonResponse({'error': 'ملف الفيديو غير موجود'}, status=404)
    
    # زيادة عدد المشاهدات
    video.increment_views()
    
    file_size = os.path.getsize(video_path)
    content_type = mimetypes.guess_type(video_path)[0] or 'video/mp4'
    
    # دعم Range requests للفيديو
    range_header = request.META.get('HTTP_RANGE', '').strip()
    
    if range_header:
        range_match = range_header.replace('bytes=', '').split('-')
        start = int(range_match[0]) if range_match[0] else 0
        end = int(range_match[1]) if range_match[1] else file_size - 1
        
        def file_iterator(file_obj, chunk_size=8192, start=0, end=None):
            file_obj.seek(start)
            remaining = (end - start + 1) if end else file_size - start
            while remaining > 0:
                chunk = file_obj.read(min(chunk_size, remaining))
                if not chunk:
                    break
                remaining -= len(chunk)
                yield chunk
        
        response = StreamingHttpResponse(
            file_iterator(open(video_path, 'rb'), start=start, end=end),
            status=206,
            content_type=content_type
        )
        response['Content-Range'] = f'bytes {start}-{end}/{file_size}'
        response['Content-Length'] = str(end - start + 1)
        response['Accept-Ranges'] = 'bytes'
    else:
        response = FileResponse(
            open(video_path, 'rb'),
            content_type=content_type
        )
        response['Content-Length'] = str(file_size)
        response['Accept-Ranges'] = 'bytes'
    
    # إضافة CORS headers
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
    response['Access-Control-Allow-Headers'] = 'Range'
    
    return response


def upload_video(request):
    """رفع فيديو جديد أو عدة فيديوهات إلى قاعدة البيانات"""
    if request.method == 'POST':
        # دعم رفع متعدد
        video_files = request.FILES.getlist('video')  # getlist للعديد من الملفات
        
        if not video_files:
            return JsonResponse({
                'success': False,
                'message': 'لم يتم تحديد ملف فيديو'
            }, status=400)
        
        uploaded_videos = []
        errors = []
        
        for video_file in video_files:
            try:
                # استخدام اسم الملف كعنوان افتراضي
                title = request.POST.get('title', '') or video_file.name.rsplit('.', 1)[0]
                description = request.POST.get('description', '')
                
                video = Video.objects.create(
                    title=title,
                    description=description,
                    file=video_file,
                    is_published=True
                )
                
                uploaded_videos.append({
                    'id': video.id,
                    'title': video.title,
                    'url': video.get_url()
                })
            except Exception as e:
                errors.append(f'خطأ في رفع {video_file.name}: {str(e)}')
        
        if uploaded_videos:
            return JsonResponse({
                'success': True,
                'message': f'تم رفع {len(uploaded_videos)} فيديو بنجاح',
                'videos': uploaded_videos,
                'errors': errors if errors else None
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'فشل رفع جميع الفيديوهات',
                'errors': errors
            }, status=400)
    
    return render(request, 'video_share/upload.html')


def video_detail(request, video_id):
    """عرض تفاصيل فيديو محدد"""
    video = get_object_or_404(Video, id=video_id, is_published=True)
    return render(request, 'video_share/video_detail.html', {'video': video})

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

def delete_video(request, video_id):
    """حذف فيديو"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        video = Video.objects.get(id=video_id)
        video_title = video.title
        
        # حذف الملف من النظام
        if video.file:
            try:
                file_path = video.file.path
                if os.path.exists(file_path):
                    os.remove(file_path)
            except Exception as e:
                # إذا فشل حذف الملف، نتابع حذف السجل
                print(f"Warning: Could not delete file: {str(e)}")
        
        # حذف الصورة المصغرة إن وجدت
        if video.thumbnail:
            try:
                thumbnail_path = video.thumbnail.path
                if os.path.exists(thumbnail_path):
                    os.remove(thumbnail_path)
            except Exception as e:
                print(f"Warning: Could not delete thumbnail: {str(e)}")
        
        # حذف السجل من قاعدة البيانات
        video.delete()
        
        return JsonResponse({
            'success': True,
            'message': f'تم حذف الفيديو "{video_title}" بنجاح'
        })
    except Video.DoesNotExist:
        return JsonResponse({'error': 'الفيديو غير موجود'}, status=404)
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error deleting video: {error_details}")
        return JsonResponse({
            'success': False,
            'error': f'حدث خطأ أثناء الحذف: {str(e)}'
        }, status=500)
