import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'video_project.settings')
django.setup()

from django.test import Client
from video_share.models import Video
import json
import re

# Check if videos exist
videos = Video.objects.filter(is_published=True)
print(f'Total videos: {videos.count()}')

for v in videos[:3]:
    print(f'  ID {v.id}: {v.title}')
    print(f'    URL: {v.get_url()}')
    print(f'    File: {v.file.name}')
    print()

# Now test the view
client = Client()
response = client.get('/reels/')
html = response.content.decode()

# Extract JSON data
match = re.search(r'const videos = (\[.*?\]);', html, re.DOTALL)
if match:
    try:
        json_str = match.group(1)
        videos_json = json.loads(json_str)
        print(f'JSON videos parsed: {len(videos_json)}')
        if videos_json:
            v = videos_json[0]
            print(f'First video in JSON:')
            print(f'  Title: {v.get("title")}')
            print(f'  URL: {v.get("url")}')
            print(f'  Likes: {v.get("likes")}')
    except Exception as e:
        print(f'Error parsing JSON: {e}')
