import urllib.request

url = 'http://www.baidu.com/s?wd=ip'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0'
}

request = urllib.request.Request(url=url, headers=headers)

proxies = {
    'http': '27.159.188.41:8899'
}

handler = urllib.request.ProxyHandler(proxies=proxies)

opener = urllib.request.build_opener(handler)

response = opener.open(request)

# response = urllib.request.urlopen(request)

content = response.read().decode('utf-8')

with open('ipaddress.html', 'w', encoding='utf-8') as fp:
    fp.write(content)