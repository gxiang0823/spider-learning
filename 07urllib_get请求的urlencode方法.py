import urllib.request
import urllib.parse

# urlencode应用场景：多个参数的时候

# http://www.baidu.com/s?wd=周杰伦&sex=男

base_url = 'https://www.baidu.com/s?'

data = {
    'wd': '周杰伦',
    'sex': '男',
    'location': '中国台湾省'
}

data = urllib.parse.urlencode(data)

url = base_url + data

headers = {
'Cookie': 'BDUSS_BFESS=U9ZbWJnSDJnemFnWlNCRFktT1B6Z1luWlQxeXBHeUF1ZVl1RHpmRXpReW9ZQnhrRVFBQUFBJCQAAAAAAAAAAAEAAADUV3GMzuHS1MfkzqrX7QAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKjT9GOo0~RjM; BD_UPN=12314753; BAIDUID=4E189A4FC08CB40DF5ABD473EDAE10F5:FG=1; MCITY=-289%3A; H_WISE_SIDS_BFESS=39661_40171_40210_40217_40222_40294_40290_40289_40284_40317_40079_40364_40351_40367_40378_40411; BIDUPSID=4E189A4FC08CB40DF5ABD473EDAE10F5; PSTM=1711174449; BA_HECTOR=a580a105a585258gal01a524oltk1i1j1ms1i1s; ZFY=yhKD2q5t:B0lMMn99cDe4KBdcz6dmkdoadH1KsOHd7Lg:C; BAIDUID_BFESS=4E189A4FC08CB40DF5ABD473EDAE10F5:FG=1; BD_CK_SAM=1; PSINO=5; delPer=0; RT="z=1&dm=baidu.com&si=iofi77wn32k&ss=lv0bf3bc&sl=s&tt=b5y&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=u4ym&ul=vyu7&hd=vyzi"; ab_sr=1.0.1_NTQwNTRhNWI5ZmEyMjkwMTg2Nzc4Yjg3M2U3YzgyMDJlNjQwZTZmYjQ2ZTVlYjJhN2Y2NDBjM2M3NjNlNjJiMWQ0ZDk3ZDVmNzcxMjQ4OWQ1ODRkMjVhYzc2MmIyMTk3NjNkYmY0NDMxOGJiYjljMGYzNjMxOGVjYTA5ODJmZGU4NGVkNzA3ZmM1MDVhYzcyOTZlMGE4YTViOTgyOTA0OGUxYTI2MzA4YTdmNzkzMDlkNTQ5MjY1NzAzOGRmYWJl; H_PS_PSSID=40171_40367_40378_40506_40511_40512_60040_60029_60033_60046; H_WISE_SIDS=40171_40367_40378_40506_40511_40512_60040_60029_60033_60046; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_PS_645EC=cb97RlxHD9oWzWylbwY7iFAfy6LUji20Km57L9wiM32bIc%2Fr%2BxI4RJndUj2q%2FKZe5mLs; BDRCVFR[feWj1Vr5u3D]=mk3SLVN4HKm; BDSVRTM=20',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0'
}

request = urllib.request.Request(url=url, headers=headers)

response = urllib.request.urlopen(request)

print(response.read().decode('utf-8'))