import matplotlib.pyplot as plt
import calendar
from crawler import *

nowYear = 2020
nowMonth = 1
durationLong = 5
city = 'jinhua'
rainy = []
sunny = []
cloudy = []
for k in range(durationLong):
    if nowMonth > 12:
        nowYear += 1
        nowMonth = 1
    try:
        result = getFromTianqi(nowYear, nowMonth)
    except:
        result = getFromTianqihoubao(nowYear, nowMonth)
    x_line = result['days']
    highTemp_line = [int(x[0]) for x in result['tempareture']]
    lowTemp_line = [int(x[1]) for x in result['tempareture']]
    rainy.append(result['rainy'])
    sunny.append(result['sunny'])
    cloudy.append(result['cloudy'])
    title = city.title() + " Tempareture in " + \
        calendar.month_abbr[nowMonth] + ' ' + str(nowYear)    
    '''
    #温度折线图
    plt.figure(k + 1)
    plt.title(title)
    plt.xlabel("Day")
    plt.ylabel("Temp/℃")
    plt.tick_params(labelsize=6)
    plt.plot(x_line, highTemp_line, color='blue', marker='o', label='Highest Temp')
    plt.plot(x_line, lowTemp_line, color='green', marker='^', label='Lowest Temp')
    plt.legend()
    '''
    nowMonth += 1

xlabel = [calendar.month_abbr[(x % 12) + 1] for x in range(durationLong)]
x1_line = range(1, durationLong + 1)
x2_line = [x + 0.25 for x in x1_line]
x3_line = [x + 0.25 for x in x2_line]
plt.figure("Total Weather")
plt.title("Weather Crawler Result")
plt.bar(x1_line, rainy, width=0.2, label="Rainy", color="orange")
plt.bar(x2_line, sunny, width=0.2, label="Sunny", color="red")
plt.bar(x3_line, cloudy, width=0.2, label="Cloudy", color="brown")
plt.xticks([x + 0.25 for x in x1_line], xlabel)
plt.tick_params(labelsize=60/durationLong)
plt.legend()
plt.show()
