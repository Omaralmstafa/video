import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE','video_project.settings')
import django
django.setup()
from video_share.models import Video
for v in Video.objects.all():
    print(v.id, bool(v.thumbnail), getattr(v.thumbnail, 'url', None))
