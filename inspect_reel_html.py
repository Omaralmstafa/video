import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE','video_project.settings')
import django
django.setup()
from django.test import Client

client = Client()
resp = client.get('/reels/')
html = resp.content.decode('utf-8')
print('Status:', resp.status_code)

# find first reel-item block
start = html.find('<div class="reel-item')
if start == -1:
    print('No reel-item found')
else:
    end = html.find('</div>', start)
    # to include nested divs, find the closing of the video block by searching ahead
    snippet = html[start:start+600]
    print('--- First reel-item snippet ---')
    print(snippet)
    print('--------------------------------')

# show video tag attributes
import re
m = re.search(r'<video([^>]*)>', html)
if m:
    print('Video tag attrs:', m.group(1))
else:
    print('No <video> tag found')

# check if loader and loading class present at least once
print('Contains .video-loader div:', 'video-loader' in html)
print('Contains reel-item.loading class:', 'reel-item loading' in html)
