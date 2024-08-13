# 适用的场景：数据采集的时候需要绕过登录，然后进入到某个页面
# 个人信息页面是utf-8  但是还是报了编码错误，因为并没有进入到个人信息页面，而是跳转到了登陆页面
# 那么登陆页面不是utf-8 所以报错

import urllib.request

# https://weibo.com/u/6754144834

url = 'https://weibo.com/u/6754144834'

headers = {
    # ':authority': 'weibo.com',
    # ':method': 'GET',
    # ':path': '/ajax/profile/info?uid=6754144834',
    # ':scheme': 'https',
    'Accept': 'application/json, text/plain, */*',
    # 'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Client-Version': 'v2.44.82',
    # Cookie中携带着你的登录信息，如果有登录之后的Cookie   那么我们可以携带者Cookie进入任何页面
    'Cookie': 'SINAGLOBAL=3655480495601.08.1680760796765; XSRF-TOKEN=9t1O7GM6C_RqdoNP9PqD2BSo; SUB=_2A25LGLl5DeRhGeBJ7lYQ9CrEyDiIHXVoV7SxrDV8PUNbmtAGLVT7kW9NRlfV_SGGUT6aJfkpR90f3pb_rLCinS17; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWvFdhzqzDPDp84F1Nx4Ni85NHD95QcS0-XeKBX1heXWs4DqcjMi--NiK.Xi-2Ri--ciKnRi-zNSoMfSh2XShn0S5tt; PC_TOKEN=a003068794; ariaDefaultTheme=default; ariaFixed=true; ariaReadtype=1; ariaMouseten=null; ariaStatus=false; WBPSESS=X_bkPZg1Qn8OD9rsyODJCvCDbFjSNA9rPo90MSq_o3ne9cxA3rXle-OZKg3urNk5RyN7oq0lbDeYfeUTTYTkNb3w8RftgbYpmbjc5nhQTnA-kCT2HmrwVtheS4bm5ePIirdvaUlw7ks3HFuv6bEKXw==',
    # Referer判断当前路径是不是由上一个路径进来的     一般情况下   是做图片的防盗链
    'Referer': 'https://weibo.com/u/6754144834',
    'Sec-Ch-Ua': '"Microsoft Edge";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Server-Version': 'v2024.04.11.2',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0',
    'X-Requested-With': 'XMLHttpRequest',
    'X-Xsrf-Token': '9t1O7GM6C_RqdoNP9PqD2BSo',
    }

request = urllib.request.Request(url=url, headers=headers)

response = urllib.request.urlopen(request)

content = response.read().decode('utf-8')

# print(content)

with open('weibo.html', 'w', encoding='utf-8') as fp:
    fp.write(content)


