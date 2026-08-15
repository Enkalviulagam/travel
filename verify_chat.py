import json, urllib.request

req = urllib.request.Request(
    'http://127.0.0.1:8000/chat',
    data=json.dumps({'messages':[{'role':'user','content':'hi'}]}).encode(),
    headers={'Content-Type':'application/json','User-Agent':'test'},
    method='POST',
)
try:
    with urllib.request.urlopen(req, timeout=30) as r:
        body = r.read().decode()
        print('status', r.status)
        print(body[:400])
except Exception as e:
    print(type(e).__name__, e)
