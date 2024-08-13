import urllib.request
import urllib.parse
import json
url = 'https://fanyi.baidu.com/v2transapi?from=en&to=zh'

headers = {
        # 'Accept': '*/*',
        # 'Accept-Encoding': 'gzip, deflate, br, zstd',
        # 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        # 'Acs-Token': '1713096057874_1713148376394_SXAhlfozYe39XMmYvkdSnME88QeB2VI59m4k9BCH2DH4IJ0573WMIDnDVYuQfhsywOTpcsJcU4/tII7++3j+jl3AuRQHa5rTxig3UbjWPDSjCqVNC2TCFFTjxRvthCm98DtFeqMOGtHHm626T8BdM1sWkihPRXHPt1raubd3ysC63mCNjieAlhGYp0mGvfdKqEuJTi5nIRh1oQfVcC2thBNaei62cLzKiCkGMUmdeWu/H4EH2aRcbBLEnth6gLwRJM84qPxBJqFj8xABuE5Poh5MOWjksNYg0ntojEv9un3bMEJtiSU4YbyTepQpzCPKP2COepoUfmJovdYZx1U7ZW2gdjUJBO908CSmCNO9c6jCqtaAxbayKwmURevqqo6vtrNcndY+7m3HpLMNJcawCjHyQlsc6j5G3iCwpGyWryVZ2dTA46021BvKb3r0u4CdItJcaSP+WTKddYC4YJO1KwXRfoVu6xrYlQ+3oYZlGliSsAcqHiGLZSiy1bkp0Ay7',
        # 'Connection': 'keep-alive',
        # 'Content-Length': '152',
        # 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'BDUSS_BFESS=U9ZbWJnSDJnemFnWlNCRFktT1B6Z1luWlQxeXBHeUF1ZVl1RHpmRXpReW9ZQnhrRVFBQUFBJCQAAAAAAAAAAAEAAADUV3GMzuHS1MfkzqrX7QAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKjT9GOo0~RjM; BAIDUID=4E189A4FC08CB40DF5ABD473EDAE10F5:FG=1; MCITY=-289%3A; H_WISE_SIDS_BFESS=39661_40171_40210_40217_40222_40294_40290_40289_40284_40317_40079_40364_40351_40367_40378_40411; BIDUPSID=4E189A4FC08CB40DF5ABD473EDAE10F5; PSTM=1711174449; H_PS_PSSID=40171_40367_40378_40506_40511_40512_40397_60040_60029_60033_60046; H_WISE_SIDS=40171_40367_40378_40506_40511_40512_40397_60040_60029_60033_60046; BA_HECTOR=a580a105a585258gal01a524oltk1i1j1ms1i1s; ZFY=yhKD2q5t:B0lMMn99cDe4KBdcz6dmkdoadH1KsOHd7Lg:C; BAIDUID_BFESS=4E189A4FC08CB40DF5ABD473EDAE10F5:FG=1; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; PSINO=5; delPer=0; smallFlowVersion=old; RT="z=1&dm=baidu.com&si=iofi77wn32k&ss=lv0bf3bc&sl=s&tt=b5y&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=u4ym&ul=vyu7&hd=vyzi"; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1713148370; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1713148370; APPGUIDE_10_7_2=1; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; ab_sr=1.0.1_NTQwNTRhNWI5ZmEyMjkwMTg2Nzc4Yjg3M2U3YzgyMDJlNjQwZTZmYjQ2ZTVlYjJhN2Y2NDBjM2M3NjNlNjJiMWQ0ZDk3ZDVmNzcxMjQ4OWQ1ODRkMjVhYzc2MmIyMTk3NjNkYmY0NDMxOGJiYjljMGYzNjMxOGVjYTA5ODJmZGU4NGVkNzA3ZmM1MDVhYzcyOTZlMGE4YTViOTgyOTA0OGUxYTI2MzA4YTdmNzkzMDlkNTQ5MjY1NzAzOGRmYWJl',
        # 'Host': 'fanyi.baidu.com',
        # 'Origin': 'https://fanyi.baidu.com',
        # 'Referer': 'https://fanyi.baidu.com/',
        # 'Sec-Ch-Ua': '"Microsoft Edge";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        # 'Sec-Ch-Ua-Mobile': '?0',
        # 'Sec-Ch-Ua-Platform': '"Windows"',
        # 'Sec-Fetch-Dest': 'empty',
        # 'Sec-Fetch-Mode': 'cors',
        # 'Sec-Fetch-Site': 'same-origin',
        # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0',
        # 'X-Requested-With': 'XMLHttpRequest',
}

data = {
        'from': 'en',
        'to': 'zh',
        'query': 'love',
        'transtype': 'realtime',
        'simple_means_flag': '3',
        'sign': '198772.518981',
        'token': '30186ece624eb40c95a08610cc5f5602',
        'domain': 'common'
}

data = urllib.parse.urlencode(data).encode('utf-8')

request = urllib.request.Request(url=url, data=data, headers=headers)

response = urllib.request.urlopen(request)

content = response.read().decode('utf-8')

obj = json.loads(content)

print(obj)



