import requests
import re, time
#import pprint
from bs4 import BeautifulSoup


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


def getFromTianqihoubao(nowYear=2020, nowMonth=1, duration=5, city="jinhua"):
    result = {}
    result['tempareture'] = []
    result['sunny'] = []
    result['cloudy'] = []
    result['rainy'] = []
    for k in range(duration):
        if nowMonth > 12:
            nowYear += 1
            nowMonth = 1
        url = "http://www.tianqihoubao.com/lishi/%s/month/" % city
        url += str(nowYear) + str(nowMonth).rjust(2, '0') + ".html"
        print(url)
        htmlPage = requests.get(url).text
        temparetureParser = "<td>\s*(\d*)℃\s*/\s*(\d*)℃\s*</td>"
        result['tempareture'].append(
            regexSearcher(htmlPage, temparetureParser)
        )
        weatherParser = "<td>\s*([\u4e00-\u9fa5]*)\s*/([\u4e00-\u9fa5]*)"
        resTmp = regexSearcher(htmlPage, weatherParser)
        result['sunny'].append(0)
        result['cloudy'].append(0)
        result['rainy'].append(0)
        # 由于每天的天气都是XX转XX，故统计的合计天数会翻倍
        for i in resTmp:
            result[weatherTranslate(i[0])][k] += 1
            result[weatherTranslate(i[1])][k] += 1
        # pprint.pprint(result)
        nowMonth += 1
    return result

# http://lishi.tianqi.com/


def getFromTianqi(nowYear=2020, nowMonth=1, duration=1, city="jinhua"):
    result = {}
    result['tempareture'] = []
    result['sunny'] = []
    result['cloudy'] = []
    result['rainy'] = []
    for k in range(duration):
        if nowMonth > 12:
            nowYear += 1
            nowMonth = 1
        url = "http://lishi.tianqi.com/%s/" % city
        url += str(nowYear) + str(nowMonth).rjust(2, '0') + ".html"
        print(url)
        headers = {
            'User-Agent': 'User-Agent:Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'
        }
        time.sleep(1)
        htmlPage = requests.get(url, headers=headers).text
        #soup = BeautifulSoup(htmlPage, 'html.parser')
        


getFromTianqi()
