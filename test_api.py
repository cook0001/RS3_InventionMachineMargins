import urllib.request
import json

def test():
    req = urllib.request.Request(
        'https://api.weirdgloop.org/exchange/history/rs/latest?id=561|37430',
        headers={'User-Agent': 'TestApp/1.0'}
    )
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        print(data)

test()
