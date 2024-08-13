import urllib.request

url = 'http://www.baidu.com'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0'
}

request = urllib.request.Request(url=url, headers=headers)

# handler   build_opener   open
# (1)   获取handler对象
handler = urllib.request.HTTPHandler()

# (2)   通过handler来获取opener对象
opener = urllib.request.build_opener(handler)

# (3)   调用open方法
response = opener.open(request)

content = response.read().decode('utf-8')

print(content)