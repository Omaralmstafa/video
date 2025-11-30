#!/usr/bin/env python
"""
Test script to verify button HTML structure and JavaScript initialization
"""
import os
import sys
import django

sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'video_project.settings')
django.setup()

from django.test import Client
from bs4 import BeautifulSoup
import re
import json

def test_reels_page():
    client = Client()
    response = client.get('/reels/')
    
    print("=" * 80)
    print("TESTING /reels/ PAGE")
    print("=" * 80)
    
    # Basic checks
    print(f"\n✓ Status Code: {response.status_code}")
    print(f"✓ Content Length: {len(response.content)}")
    print(f"✓ Content Type: {response.get('Content-Type')}")
    
    # Parse HTML
    html = response.content.decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    
    # Find buttons
    buttons = {
        'likeBtn': soup.find('button', {'id': 'likeBtn'}),
        'shareBtn': soup.find('button', {'id': 'shareBtn'}),
        'downloadBtn': soup.find('button', {'id': 'downloadBtn'}),
        'menuBtn': soup.find('button', {'id': 'menuBtn'}),
    }
    
    print("\n📌 BUTTON ELEMENTS:")
    for name, btn in buttons.items():
        status = "✓ FOUND" if btn else "✗ MISSING"
        print(f"  {name}: {status}")
        if btn:
            print(f"    - Classes: {btn.get('class', [])}")
            print(f"    - Text: {btn.get_text()[:20]}")
    
    # Find share menu items
    share_items = {
        'whatsappShare': soup.find('div', {'id': 'whatsappShare'}),
        'telegramShare': soup.find('div', {'id': 'telegramShare'}),
        'copyLink': soup.find('div', {'id': 'copyLink'}),
        'nativeShare': soup.find('div', {'id': 'nativeShare'}),
    }
    
    print("\n🔗 SHARE MENU ITEMS:")
    for name, item in share_items.items():
        status = "✓ FOUND" if item else "✗ MISSING"
        print(f"  {name}: {status}")
    
    # Check JavaScript
    print("\n🎬 JAVASCRIPT CHECK:")
    script_tags = soup.find_all('script')
    print(f"  ✓ Script tags: {len(script_tags)}")
    
    main_script = None
    for script in script_tags:
        if script.string and 'const videos' in script.string:
            main_script = script.string
            break
    
    if main_script:
        print(f"  ✓ Main script found ({len(main_script)} bytes)")
        
        # Check for key functions
        key_functions = [
            'init()',
            'updateVideoPosition()',
            'playCurrentVideo()',
            'goToVideo(',
            'handleSwipe()',
            'togglePlayPause()',
            'downloadVideo()',
            'openShareMenu()',
        ]
        
        print("\n  🔍 Key Functions:")
        for func in key_functions:
            found = func in main_script
            status = "✓" if found else "✗"
            print(f"    {status} {func}")
        
        # Check for event listeners
        listeners = [
            'likeBtn.addEventListener',
            'shareBtn.addEventListener',
            'downloadBtn.addEventListener',
            'reelsWrapper.addEventListener',
        ]
        
        print("\n  📡 Event Listeners:")
        for listener in listeners:
            found = listener in main_script
            status = "✓" if found else "✗"
            print(f"    {status} {listener}")
        
        # Extract and check videos data
        match = re.search(r"const videos = JSON\.parse\('([^']+)'\s*\|\|", main_script)
        if match:
            videos_json = match.group(1)
            try:
                # Unescape the JSON
                videos_json = videos_json.replace('\u0027', '"').replace('\\u002D', '-')
                videos = json.loads(videos_json)
                print(f"\n  📹 Videos count: {len(videos)}")
                for i, v in enumerate(videos):
                    print(f"    {i+1}. {v.get('title', 'No title')} - {v.get('filename', 'No filename')}")
            except Exception as e:
                print(f"    ✗ Error parsing videos: {e}")
    else:
        print("  ✗ Main script not found")
    
    print("\n" + "=" * 80)
    print("TEST COMPLETE")
    print("=" * 80)

if __name__ == '__main__':
    test_reels_page()
