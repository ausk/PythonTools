#!/usr/bin/python3
# 2017.08.16 14:37:31 CST
import urllib.request, urllib.parse
import time, calendar, random
import os, sys, re, json

## 初始化 ...
os.chdir(os.path.abspath(os.path.dirname(__file__)))
#from data import data
#from data_all import data
cities = data["cities"]
codes  = data["codes"]

LINE_DOT = "."*50
LINE_EQ  = "="*50
weekdays={0:"周一",1:"周二",2:"周三",3:"周四",4:"周五",5:"周六",6:"周日"}
headers = {
    "Host": "widget.seniverse.com",
    "Referer": "https://www.seniverse.com/widget/get",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"
}

## 日期转换周几
def date2weekday(date):
    y,m,d = [int(x) for x in date.strip().split("-")]
    weekday = weekdays[calendar.weekday(y, m, d)]
    return weekday

## 获取天气
def getCityWeather(city="Wuhan"):
    ## 获取hash
    (xloc, xhash, xpy, xhz) = cities.get(city.capitalize(), cities.get("Wuhan"))

    ## 请求信息
    xcbk =  "jsonp_{}_{}".format(int(time.time()*1000), int(random.random()*1E5))
    url = "https://widget.seniverse.com/api/weather?flavor=slim&location={xloc}&geolocation=disabled&language=zh-chs&unit=c&theme=chameleon&container=tp-weather-widget&bubble=enabled&alarmType=badge&hash={xhash}&_glance=enable&_container=tp-weather-widget&callback={xcbk}".format(xloc = xloc,  xhash = xhash , xcbk = xcbk)
    try:
        req = urllib.request.Request(url, data = None, headers = headers)
        res = urllib.request.urlopen(req).read().decode("utf-8")
    except Exception as exc:
        print("无法获取天气信息")
        print(exc)
        return
    js = json.loads(re.findall("(?<={}\().*?(?=\);)".format(xcbk),res)[0])

    ## 解析信息
    weather = js["weather"]
    now = weather["now"]       # 当前天气
    air = weather["air"]       # 空气质量
    loc = weather["location"]  # 城市位置
    days = weather["daily"]    # 最近5天天气
    alarms = weather["alarms"] # 警报

    xid, xname, xpath = loc["id"], loc["name"], loc["path"]
    aqi, aqi_name = air["city"]["aqi"], air["city"]["quality"]
    xaqi = "空气质量{}({})".format(aqi_name, aqi)
    print(LINE_EQ)
    print("{}\n{}".format( xpath, xaqi) )

    for idx, alarm in enumerate(alarms, start=1):
        xlevel = alarm["level"]
        xdate = alarm["pub_date"]
        xdesc = alarm["description"]
        xtype = alarm["type"]
        print(LINE_DOT)
        print("[{:02d}] {} {} {}".format(idx, xtype, xlevel, xdate))
        print(xdesc)

    print(LINE_DOT)
    for day in days:
        date= day["date"]
        date2 = date + " "+ date2weekday(date)
        high, low = day["high"], day["low"]
        code_night, code_day = day["code_night"], day["code_day"]
        print("{}; {}°C ~ {}°C; {}=>{}".format(date2, low, high, codes[code_night][1], codes[code_day][1] ))

    print(LINE_EQ)

if __name__ == "__main__":
    argv = sys.argv
    city = len(argv)==2 and argv[1] or "Wuhan"
    getCityWeather(city)

