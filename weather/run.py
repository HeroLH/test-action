# --coding: utf-8 --
"""
   Created by Lin Vision at 2021/11/17.
   Copyright (c) 2013-present, XiaMen DianChu Technology Co.,Ltd.
   Description:
   Changelog: all notable changes to this file will be documented
"""
import pytz, datetime
import requests, json, re
from bs4 import BeautifulSoup
from dataclasses import dataclass


@dataclass
class WeatherTodayDto:
    """
    当天天气数据结构
    """
    weaid: str
    weatid: str  # 天气ID，可对照 weather.wtype 接口中 weaid
    days: str
    week: str
    cityno: str
    citynm: str
    cityid: str
    temperature: str  # 当日温度区间 (注: 夜间只有一个温度如24℃/24℃)
    temperature_curr: str  # 当前温度
    temp_high: str  # 最高温度
    temp_low: str  # 最低温度
    humidity: str  # 湿度
    aqi: str  # pm2.5 说明详见weather.pm25
    weather: str  # 天气
    weather_icon: str  # 气象图标
    wind: str  # 风向
    winp: str  # 风力


def request_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        return None


def get_param_dict(url):
    param_list = url.strip().split('?')[1].split('&')
    param_dict = {}
    for item in param_list:
        param_dict[item.split('=')[0]] = item.split('=')[1]
    return param_dict


def parse_test_exp_result(html):
    test_link_list = re.findall('<a target="_blank" href=".*?">.*?</a> \(示例中sign会不定期调整\)', html)
    if len(test_link_list) != 1:
        raise Exception("测试链接获取有误")
    soup = BeautifulSoup(test_link_list[0], "lxml")
    url = soup.find('a').get("href")
    data = get_param_dict(url)
    data["url"] = url
    return data


def parse_weather_result(url):
    data = None
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
    except requests.RequestException as err:
        raise Exception("请求天气数据报错: ", err)

    if data.get("success") != "1":
        print(f"请求地址为：{url}")
        print(f"响应体为： {data}")
        raise Exception(f"请求天气数据报错, 响应code 为 {data.get('msg', '')}， 错误信息为 {data.get('success', '')}")

    result = data.get('result', {})
    if "weather_icon1" in result:
        del result["weather_icon1"]
    if "humi_high" in result:
        del result["humi_high"]
    if "humi_low" in result:
        del result["humi_low"]
    if "weatid1" in ["weatid1"]:
        del result["weatid1"]
    if "windid" in result:
        del result["windid"]
    if "winpid" in result:
        del result["winpid"]
    if "weather_curr" in result:
        del result["weather_curr"]
    if "temp_curr" in result:
        del result["temp_curr"]
    if "weather_iconid" in result:
        del result["weather_iconid"]

    return WeatherTodayDto(**data.get('result', {}))


def main():
    url = "https://www.nowapi.com/api/weather.today"
    html = request_url(url)
    test_exp_param = parse_test_exp_result(html)  # 得到测试用例的数据
    print(f"获得测试用 token 数据：{test_exp_param}")

    wea_id = 2955  # 厦门湖里
    get_weather_url = f"http://api.k780.com/?app=weather.today&weaId={wea_id}&appkey={test_exp_param.get('appkey', '')}&sign={test_exp_param.get('sign', '')}&format=json"
    weather_info = parse_weather_result(get_weather_url)

    tz = pytz.timezone('Asia/Shanghai')
    update_time = datetime.datetime.now(tz).strftime("%H:%M:%S")

    line = '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s' % (
        weather_info.days,
        update_time,
        weather_info.week,
        weather_info.citynm,
        weather_info.weather,
        weather_info.temperature,
        weather_info.temperature_curr,
        weather_info.temp_high,
        weather_info.temp_low,
        weather_info.humidity,
        weather_info.aqi,
        weather_info.weather_icon,
        weather_info.wind,
        weather_info.winp,
    )
    print(line)


if __name__ == "__main__":
    main()
