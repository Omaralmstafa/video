import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'video_project.settings')
django.setup()

from django.test import Client
from video_share.models import Video

client = Client()
response = client.get('/reels/')

print(f"✅ Page Status: {response.status_code}")

# Check videos in DB
videos = Video.objects.filter(is_published=True)
print(f"✅ Videos in DB: {videos.count()}")
for v in videos[:2]:
    print(f"   - ID {v.id}: {v.title} (likes: {v.likes})")

html = response.content.decode()
print(f"✅ HTML size: {len(html)} bytes")
print(f"✅ Contains 'const videos =': {'const videos =' in html}")
print(f"✅ Contains 'reel-item': {'reel-item' in html}")
print(f"✅ Contains video player: {'playsinline' in html}")

# Try to like a video
print("\n--- Testing Like API ---")
response = client.post('/api/like/1/')
print(f"✅ Like API Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"✅ Response: {data}")
else:
    print(f"❌ Error: {response.content}")
