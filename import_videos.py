#!/usr/bin/env python
"""
سكريبت لنقل الفيديوهات من مجلد media/videos إلى قاعدة البيانات
"""
import os
import sys
import django

sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'video_project.settings')
django.setup()

from django.conf import settings
from django.core.files.base import ContentFile
from video_share.models import Video

def import_videos():
    videos_dir = os.path.join(settings.MEDIA_ROOT, 'videos')
    
    if not os.path.exists(videos_dir):
        print(f"❌ مجلد الفيديوهات غير موجود: {videos_dir}")
        return
    
    print(f"📂 البحث عن الفيديوهات في: {videos_dir}")
    
    imported_count = 0
    skipped_count = 0
    
    for filename in os.listdir(videos_dir):
        if filename.endswith(('.mp4', '.webm', '.ogg', '.avi', '.mkv')):
            file_path = os.path.join(videos_dir, filename)
            
            # تحقق من وجود الفيديو في قاعدة البيانات
            if Video.objects.filter(file__endswith=filename).exists():
                print(f"⏭️  تم تخطي: {filename} (موجود بالفعل)")
                skipped_count += 1
                continue
            
            # الحصول على اسم الفيديو (بدون امتداد)
            title = filename.rsplit('.', 1)[0]
            file_size = os.path.getsize(file_path)
            file_size_mb = file_size / (1024 * 1024)
            
            # قراءة الملف وحفظه في النموذج
            try:
                with open(file_path, 'rb') as f:
                    file_content = ContentFile(f.read(), name=filename)
                    
                    video = Video.objects.create(
                        title=title,
                        description=f"فيديو تم استيراده - {filename}",
                        is_published=True
                    )
                    video.file.save(filename, file_content, save=True)
                    
                    print(f"✅ تم استيراد: {filename} (ID: {video.id}) - {file_size_mb:.2f} MB")
                    imported_count += 1
            except Exception as e:
                print(f"❌ خطأ أثناء استيراد {filename}: {e}")
    
    print(f"\n📊 النتائج:")
    print(f"  ✅ تم استيراد: {imported_count}")
    print(f"  ⏭️  تم تخطي: {skipped_count}")
    print(f"  📹 إجمالي الفيديوهات في قاعدة البيانات: {Video.objects.count()}")

if __name__ == '__main__':
    import_videos()

