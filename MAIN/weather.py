from bs4 import BeautifulSoup
from config import CITY
from config import KEY
from config import IMAGES
import requests
import json
import re
import time

# URL = "http://www.weather.com.cn/weather1d/{}.shtml"
#
# def forecast_7days(city):
#     city_code = CITY.get(city)
#
#     forecast7days_html = requests.get(URL.format(city_code))
#     forecast7days_html.encoding = "utf8"
#     soup = BeautifulSoup(forecast7days_html.text, 'lxml')
#
#     text = str(soup.select("#hidden_title")[0])
#     # print(text)
#
#     res = re.search('value="(\S+).*?(\S+).*?(\S+).*?(\d+)/(\d+)', text)
#     date = (res.group(1))
#     week = (res.group(2))
#     weather = (res.group(3))
#     temp1 = (res.group(4))
#     temp2 = (res.group(5))
#
#     if temp1 < temp2:
#         lowest_temp = temp1
#         highest_temp = temp2
#     else:
#         lowest_temp = temp2
#         highest_temp = temp1
#
#     # return (date, week, weather, lowest_temp, highest_temp)
#     print(date, week, weather, lowest_temp, highest_temp)
#
# forecast_7days("深圳")

URL = 'https://restapi.amap.com/v3/weather/weatherInfo?city={}&key={}&extensions={}'
date = {
    "1": "星期一",
    "2": "星期二",
    "3": "星期三",
    "4": "星期四",
    "5": "星期五",
    "6": "星期六",
    "7": "星期天",
}

def rightNow(city):
    city_code = CITY.get(city)
    if city_code == None:
        return None

    data = requests.get(URL.format(city_code, KEY, 'base')).json()
    if data['count'] == '0':
        return None

    rData = data['lives'][0]
    weather = rData['weather'] + IMAGES.get(rData['weather'])
    # for k, v in IMAGES.items():
    #     if k == rData['weather']:
    #         weather = rData['weather']+v
    temperature = rData['temperature'] + "℃"
    wind = rData['winddirection'] + "风 " + rData['windpower'] + "级"
    humidity = rData['humidity'] + "%"
    time = rData['reporttime']
    time = re.search("^\d+-(\d+)-(\d+)\s(\d+:\d+)", time)
    time = time.group(1) + "月" + time.group(2) + "日 " + time.group(3) + "实况"

    message = city + "\n" + \
              time + "\n" + \
              "天气：" + weather + "\n" + \
              "温度：" + temperature + "\n" + \
              "风力：" + wind + "\n" + \
              "湿度：" + humidity

    return message

def forecastAll(city):
    city_code = CITY.get(city)
    if city_code == None:
        return None

    data = requests.get(URL.format(city_code, KEY, 'all')).json()
    if data['count'] == '0':
        return None

    todayData = data['forecasts'][0]['casts'][0]
    tomorrowData = data['forecasts'][0]['casts'][1]
    todaydate = re.search("^\d+-(\d+)-(\d+)", todayData['date'])
    todayweekday = date.get(todayData['week'])
    todaydate = todaydate.group(1) + "月" + todaydate.group(2) + "日 " + todayweekday
    todayweather = todayData['dayweather'] + "转" + todayData['nightweather'] if todayData['dayweather'] != todayData['nightweather'] else todayData['dayweather']
    todaytemp = todayData['nighttemp'] + "-" + todayData['daytemp'] + "℃"
    todaywind = todayData['daywind'] + " " + todayData['daypower'] + "级"

    tomorrowdate = re.search("^\d+-(\d+)-(\d+)", tomorrowData['date'])
    tomorrowweekday = date.get(tomorrowData['week'])
    tomorrowdate = tomorrowdate.group(1) + "月" + tomorrowdate.group(2) + "日 " + tomorrowweekday
    tomorrowweather = tomorrowData['dayweather'] + "转" + tomorrowData['nightweather'] if tomorrowData['dayweather'] != tomorrowData['nightweather'] else tomorrowData['dayweather']
    tomorrowtemp = tomorrowData['nighttemp'] + "-" + tomorrowData['daytemp'] + "℃"
    tomorrowwind = tomorrowData['daywind'] + " " + tomorrowData['daypower'] + "级"

    rightnow = rightNow(city)
    todayres = "今天：\n" + \
               todaydate + "\n" + \
               "天气：" + todayweather + "\n" + \
               "温度：" + todaytemp + "\n" + \
               "风力：" + todaywind

    tomorrowres = "明天：\n" + \
                  tomorrowdate + "\n" + \
                  "天气：" + tomorrowweather + "\n" + \
                  "温度：" + tomorrowtemp + "\n" + \
                  "风力：" + tomorrowwind

    totalres = "当前天气实况：\n" + rightnow + "\n\n" + todayres + "\n\n" + tomorrowres

    return totalres
if __name__ == '__main__':
    forecastAll('深圳市')
