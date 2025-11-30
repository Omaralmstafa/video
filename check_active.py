import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'video_project.settings')
django.setup()
from django.test import Client

client = Client()
resp = client.get('/reels/')
html = resp.content.decode()
print('Status:', resp.status_code)
print('Contains "reel-item active":', 'reel-item active' in html)
# Print first occurrence context
idx = html.find('reel-item')
if idx!=-1:
    print('\nFirst reel-item snippet:\n')
    print(html[idx:idx+400])
else:
    print('No reel-item in HTML')
