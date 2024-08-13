
import random
import urllib.request

proxies_pool = [
    {'http': '27.159.188.41:8899'},
    {'http': '27.159.188.41:7788'},
    {'http': '27.159.188.41:6677'},
    {'http': '27.159.188.41:5566'},
    {'http': '27.159.188.41:4455'},
]

proxies = random.choice(proxies_pool)


url = 'http://www.baidu.com/s?wd=ip'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0'
}

request = urllib.request.Request(url=url, headers=headers)

handler = urllib.request.ProxyHandler(proxies)

opener = urllib.request.build_opener(handler)

response = opener.open(request)

