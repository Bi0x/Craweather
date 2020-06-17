import matplotlib.pyplot as plt
import calendar
from crawler import *


def getDays(year, month):
    days31 = [1, 3, 5, 7, 8, 10, 12]
    days30 = [4, 6, 9, 11]
    if month in days31:
        return 31
    if month in days30:
        return 30
    if year % 4 == 0 and year % 100 != 0:
        return 29
    if year % 100 == 0 and year % 400 == 0:
        return 29
    return 28


nowYear = 2020
nowMonth = 1
durationLong = 1
city = 'jinhua'
result = getFromTianqihoubao(duration=durationLong)
for k in range(durationLong):
    if nowMonth > 12:
        nowYear += 1
        nowMonth = 1
    tmpDays = getDays(nowYear, nowMonth)
    x_lines = [x for x in range(1, tmpDays + 1)]
    y_lines = [int(x[0]) for x in result['tempareture'][k]]
    title = city.title() + " Tempareture in " + \
        calendar.month_abbr[nowMonth] + ' ' + str(nowYear)
    plt.figure(k + 1)
    plt.title(title)
    plt.xlabel("Day")
    plt.ylabel("Temp/℃")
    plt.plot(x_lines, y_lines, color='blue', marker='o')
    plt.draw()
    nowMonth += 1
plt.show()
