import requests
BASE = 'http://127.0.0.1:8000'

def check_get(path):
    url = BASE + path
    print(f'GET {path} ->', end=' ')
    r = requests.get(url, timeout=5)
    print(r.status_code)
    return r

def has_element_simple(html, token):
    """Simple substring check for element id/class/tag token in HTML."""
    return token in html

def main():
    paths = ['/reels/', '/video/1/', '/']
    # Use a session to capture cookies (CSRF)
    session = requests.Session()
    for p in paths:
        try:
            url = BASE + p
            print(f'GET {p} ->', end=' ')
            r = session.get(url, timeout=5)
            print(r.status_code)
            if r.status_code == 200 and p == '/reels/':
                ok = has_element_simple(r.text, 'bottomProgress')
                print('  bottomProgress present:', ok)
                ok2 = ('Add Video' in r.text) or ('addVideoBtn' in r.text) or ('upload' in r.text)
                print('  Add Video link present:', ok2)
            if r.status_code == 200 and p.startswith('/video/'):
                ok = has_element_simple(r.text, 'bottomProgressDetail')
                print('  bottomProgressDetail present:', ok)
        except Exception as e:
            print('  ERROR', e)

    # Try like API for id 1 (POST) using CSRF cookie if available
    like_url = BASE + '/api/like/1/'
    print('POST /api/like/1/ ->', end=' ')
    try:
        csrftoken = session.cookies.get('csrftoken', '')
        headers = {}
        if csrftoken:
            headers['X-CSRFToken'] = csrftoken
        r = session.post(like_url, headers=headers, timeout=5)
        print(r.status_code)
        try:
            print('  json:', r.json())
        except Exception:
            print('  non-json response')
    except Exception as e:
        print('  ERROR', e)

if __name__ == '__main__':
    main()
