#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' a test module '

__author__ = 'saowu'

import datetime
import json
import requests
from bs4 import BeautifulSoup
from pyecharts.charts import Map
from pyecharts import options as opts

province2hanzi = {
    'Anhui': '安徽',
    'Beijing': '北京',
    'Chongqing': '重庆',
    'Fujian': '福建',
    'Gansu': '甘肃',
    'Guangdong': '广东',
    'Guangxi': '广西',
    'Guizhou': '贵州',
    'Hainan': '海南',
    'Hebei': '河北',
    'Heilongjiang': '黑龙江',
    'Henan': '河南',
    'Hong Kong': '香港',
    'Hubei': '湖北',
    'Hunan': '湖南',
    'Inner Mongolia': '内蒙古',
    'Jiangsu': '江苏',
    'Jiangxi': '江西',
    'Jilin': '吉林',
    'Liaoning': '辽宁',
    'Macau': '澳门',
    'Ningxia': '宁夏',
    'Qinghai': '青海',
    'Shaanxi': '陕西',
    'Shandong': '山东',
    'Shanghai': '上海',
    'Shanxi': '山西',
    'Sichuan': '四川',
    'Tianjin': '天津',
    'Tibet': '西藏',
    'Xinjiang': '新疆',
    'Yunnan': '云南',
    'Zhejiang': '浙江'
}

china_confirmed_info = {}
china_deaths_info = {}
china_recovered_info = {}
china_existing_info = {}


def get_confirmed_info(url_community, name):
    # 1.爬取api数据
    # r_community = requests.get(url_community)
    # with open(name, 'w')as _file:
    #     _file.write(r_community.text)
    # data_community = BeautifulSoup(r_community.text, 'html.parser')

    # 2.先爬取到本地，再本地读取，加快速度调试
    with open(name, 'r')as _file:
        r_community = _file.read()
    data_community = BeautifulSoup(r_community, 'html.parser')

    jsonObj = json.loads(data_community.decode('utf-8'))
    return jsonObj


def format_info(json_obj, result):
    for _country in json_obj['locations']:
        if _country['country'] == 'China':
            result[province2hanzi[_country['province']]] = _country['latest']
    format_taiwan_info(json_obj, result)


def format_taiwan_info(json_obj, result):
    for _country in json_obj['locations']:
        if _country['country_code'] == 'TW':
            result['台湾'] = _country['latest']


if __name__ == '__main__':
    # 当前时间戳
    _time_str = str(datetime.datetime.now().strftime('截止：%Y-%m-%d %H:%M:%S'))

    confirmed_info = get_confirmed_info('https://coronavirus-tracker-api.herokuapp.com/confirmed', 'confirmed_info')
    deaths_info = get_confirmed_info('https://coronavirus-tracker-api.herokuapp.com/deaths', 'deaths_info')
    recovered_info = get_confirmed_info('https://coronavirus-tracker-api.herokuapp.com/recovered', 'recovered_info')
    format_info(confirmed_info, china_confirmed_info)
    format_info(deaths_info, china_deaths_info)
    format_info(recovered_info, china_recovered_info)
    # 计算现存
    for province in china_confirmed_info:
        china_existing_info[province] = (
                china_confirmed_info[province] - china_deaths_info[province] - china_recovered_info[province])
    # 格式化数据
    provinces = list(china_existing_info.keys())
    values = list(china_existing_info.values())
    data_list = [[provinces[i], values[i]] for i in range(len(provinces))]

    _map = Map(init_opts=opts.InitOpts(width="801px", ))
    _map.set_global_opts(
        title_opts=opts.TitleOpts(title="中国nCoV肺炎疫情现存确诊图", pos_left="left", subtitle=_time_str),
        visualmap_opts=opts.VisualMapOpts(
            is_piecewise=True,
            pieces=[
                {"max": 0, "label": "0人", "color": "#FFFFFF"},
                {"min": 1, "max": 9, "label": "1-10人", "color": "#FFEBCD"},
                {"min": 10, "max": 99, "label": "10-99人", "color": "#FFA07A"},
                {"min": 100, "max": 499, "label": "100-499人", "color": "#EE5C42"},
                {"min": 500, "max": 999, "label": "500-999人", "color": "#CD3333"},
                {"min": 1000, "max": 10000, "label": "1000-10000人", "color": "#A52A2A"},
                {'min': 10000, "label": ">10000人", "color": "#8B0000"}
            ])
    )
    _map.add("中国现存确诊数据", data_list, maptype="china", is_map_symbol_show=False)
    _map.render(path="nCoV_map.html", template_name='nCoV_map.html')
    print(_time_str, "中国nCoV肺炎疫情现存确诊图更新成功")
