import urllib.request

url = 'http://www.baidu.com'

response = urllib.request.urlopen(url)
# 一个类型六个方法
# response是HTTPResponse类型的数据
# print(type(response))

# 一字节一字节的去读数据
# content = response.read()
# print(content)

# 返回多少个字节
# content = response.read(5)
# print(content)

# 读取一行
# content = response.readline()
# print(content)

# 读取全部内容，按行读
# content = response.readlines()
# print(content)

# 返回状态码 如果是200证明逻辑没有问题
# print(response.getcode())

# 返回url地址
# print(response.geturl())

# 返回状态信息
# print(response.getheaders())