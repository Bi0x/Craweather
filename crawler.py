import requests, re, pprint
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
def getFromTianqihoubao(startYear=2020, startMonth=1, duration=5, city="jinhua"):
    result = {}
    result['tempareture'] = []
    result['sunny'] = []
    result['cloudy'] = []
    result['rainy'] = []
    for now in range(duration):
        url = "http://www.tianqihoubao.com/lishi/%s/month/" % city
        url += str(startYear) + str(startMonth + now).rjust(2, '0') + ".html"
        htmlPage =  requests.get(url).text
        temparetureParser = "<td>\s*(\d*)℃\s*/\s*(\d*)℃\s*</td>"
        result['tempareture'].append(regexSearcher(htmlPage, temparetureParser))
        weatherParser = "<td>\s*([\u4e00-\u9fa5]*)\s*/([\u4e00-\u9fa5]*)"
        resTmp = regexSearcher(htmlPage, weatherParser)
        result['sunny'].append(0)
        result['cloudy'].append(0)
        result['rainy'].append(0)
        # 由于每天的天气都是XX转XX，故统计的合计天数会翻倍
        for i in resTmp:
            result[weatherTranslate(i[0])][now] += 1
            result[weatherTranslate(i[1])][now] += 1
        pprint.pprint(result)

getFromTianqihoubao()