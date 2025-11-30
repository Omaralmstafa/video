import requests

BASE = 'http://127.0.0.1:8000'

def check(path):
    try:
        r = requests.get(BASE + path, timeout=5)
        print(path, r.status_code, 'len=', len(r.text))
        return r.status_code == 200
    except Exception as e:
        print(path, 'ERROR', e)
        return False

if __name__ == '__main__':
    paths = ['/reels/', '/']
    for p in paths:
        check(p)
