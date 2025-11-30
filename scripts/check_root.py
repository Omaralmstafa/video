import os
import sys
from pathlib import Path
import django
from django.test import Client

# Ensure project root is on sys.path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'video_project.settings')
django.setup()

c = Client()
resp = c.get('/')
print('STATUS', resp.status_code)
print('LEN', len(resp.content))
print(resp.content[:1000].decode('utf-8', errors='replace'))
from django.template import loader
import traceback

try:
	tmpl = loader.get_template('video_share/video_list.html')
	s = tmpl.render({'videos': []})
	print('RENDERED_LEN', len(s))
	print(repr(s[:800]))
except Exception:
	traceback.print_exc()
