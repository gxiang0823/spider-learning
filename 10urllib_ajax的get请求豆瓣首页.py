# get 请求
# 获取豆瓣电影第一页 并以json文件保存到本地
import urllib.request

url = 'https://movie.douban.com/j/chart/top_list?type=10&interval_id=100%3A90&action=&start=0&limit=20'

headers = {
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0'
}

# （1）请求对象的定制
request = urllib.request.Request(url=url, headers=headers)

# （2）获取相应的数据
response = urllib.request.urlopen(request)
content = response.read().decode('utf-8')

# print(content)

# （3）数据下载到本地
# open方法默认情况下使用的是gbk编码  如果我们想要保存汉字，那么需要在open方法中指定编码方式为utf-8
# encoding = 'utf-8'
# fp = open('douban.json', 'w', encoding='utf-8')
# fp.write(content)
# fp.close()

with open('douban1.json', 'w', encoding='utf-8') as fp:
    fp.write(content)


