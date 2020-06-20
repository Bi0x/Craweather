import requests
import re
import time, random
#import pprint
#from bs4 import BeautifulSoup

fakeHeaders = [
    {
        'User-Agent': 'User-Agent:Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'
    }, {
        'User-Agent': 'User-Agent:Mozilla/5.0(Macintosh;U;IntelMacOSX10_6_8;en-us)AppleWebKit/534.50(KHTML,likeGecko)Version/5.1Safari/534.50'
    }, {
        'User-Agent': 'User-Agent:Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;360SE)'
    }
]


def regexSearcher(htmlPage, regexParser):
    temperatureRegex = re.compile(regexParser, re.DOTALL)
    return temperatureRegex.findall(htmlPage)


def weatherTranslate(str):
    if '雨' in str:
        return 'rainy'
    if '晴' in str:
        return 'sunny'
    if '阴' or '多云' in str:
        return 'cloudy'
    raise Exception

# http://www.tianqihoubao.com/
def getFromTianqihoubao(nowYear=2020, nowMonth=1, city="jinhua"):
    result = {}
    result['days'] = []
    result['sunny'] = 0
    result['cloudy'] = 0
    result['rainy'] = 0
    url = "http://www.tianqihoubao.com/lishi/%s/month/" % city
    url += str(nowYear) + str(nowMonth).rjust(2, '0') + ".html"
    #print(url)
    htmlPage = requests.get(url).text
    temparetureParser = "<td>\s*(\d*)℃\s*/\s*(\d*)℃\s*</td>"
    result['tempareture'] = regexSearcher(htmlPage, temparetureParser)
    weatherParser = ">\s*\d*年\d*月(\d*)日\s*</a>\s*</td>\s*<td>\s*([\u4e00-\u9fa5]*)\s*/([\u4e00-\u9fa5]*)"
    resTmp = regexSearcher(htmlPage, weatherParser)
    for i in resTmp:
        result[weatherTranslate(i[1])] += 1
        result[weatherTranslate(i[2])] += 1
        result['days'].append(i[0])
    # pprint.pprint(result)
    # 由于每天的天气都是XX转XX，统计的合计天数会翻倍，故全部除 2
    result['sunny'] = 2
    result['cloudy'] /= 2
    result['rainy'] /= 2
    #print(result)
    return result

# http://lishi.tianqi.com/
def getFromTianqi(nowYear=2020, nowMonth=1, city="jinhua"):
    result = {}
    result['days'] = []
    result['tempareture'] = []
    result['sunny'] = 0
    result['cloudy'] = 0
    result['rainy'] = 0
    url = "http://lishi.tianqi.com/%s/" % city
    url += str(nowYear) + str(nowMonth).rjust(2, '0') + ".html"
    #print(url)
    #time.sleep(1)
    htmlPage = requests.get(url, headers=fakeHeaders[random.randint(0, 2)]).text
    #soup = BeautifulSoup(htmlPage, 'html.parser')
    #print(soup.find_all(class_='thrui'))
    temparetureParser = '<div class="th\d*">\d*-\d*-(\d*).[\u4e00-\u9fa5]*.</div>\s*<div class="th\d*">(\d*)℃</div>\s*<div class="th\d*">(\d*)℃</div>\s*<div class="th\d*">([\u4e00-\u9fa5]*)</div>'
    for i in regexSearcher(htmlPage, temparetureParser):
        tmp = (i[1], i[2])
        result[weatherTranslate(i[3])] += 1
        result['tempareture'].append(tmp)
        result['days'].append(i[0])
    #print(result)
    return result

