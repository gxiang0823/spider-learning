# 使用url获取网站首页源码
import urllib.request

# （1）定义一个url

url = 'http://www.baidu.com'

# （2）模拟浏览器向服务器发出请求 response响应
response = urllib.request.urlopen(url)

# （3）获取响应中的源码
content = response.read().decode('utf-8')

# （4）打印
print(content)
