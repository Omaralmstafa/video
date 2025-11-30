import os, django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'video_project.settings')
django.setup()

from django.test import Client

client = Client()
response = client.get('/reels/')

html = response.content.decode()

# Check for new JSON format
if 'const videos =' in html:
    print('✅ JSON found in response')
    start = html.find("const videos =") + len("const videos = ")
    end = html.find(";", start)
    json_str = html[start:end].strip()
    
    try:
        videos = json.loads(json_str)
        print(f'✅ {len(videos)} videos found')
        if videos:
            print(f'Video 1: id={videos[0].get("id")}, title={videos[0].get("title")}, likes={videos[0].get("likes")}')
            for i, v in enumerate(videos):
                print(f'  Video {i+1}: ID={v.get("id")}, Title={v.get("title")}')
    except Exception as e:
        print(f'Error parsing: {e}')
        print(f'JSON str (first 200 chars): {json_str[:200]}')
else:
    print('❌ JSON not found')

