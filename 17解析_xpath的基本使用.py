from lxml import etree

# xpath 解析
# (1)   本地文件            etree.parse()
# (2)   服务器响应数据       etree.HTML()

# xpath解析本地文件
tree = etree.parse('17解析_xpath的基本使用.html')


