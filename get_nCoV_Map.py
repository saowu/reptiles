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

data_dict = {}


def get_info():
    url_community = 'https://coronavirus-tracker-api.herokuapp.com/v2/locations?country_code=CN'
    r_community = requests.get(url_community)
    data_community = BeautifulSoup(r_community.text, 'html.parser')
    jsonObj = json.loads(data_community.decode('utf-8'))
    return jsonObj


def get_taiwan(result):
    url_community = 'https://coronavirus-tracker-api.herokuapp.com/v2/locations?country_code=TW'
    r_community = requests.get(url_community)
    data_community = BeautifulSoup(r_community.text, 'html.parser')
    jsonObj = json.loads(data_community.decode('utf-8'))
    result['台湾'] = jsonObj['latest']['confirmed']


def format_data(json_obj, result):
    for _province in json_obj['locations']:
        result[province2hanzi[_province['province']]] = _province['latest']['confirmed']


if __name__ == '__main__':
    _timestr = str(datetime.datetime.now().strftime('截止：%Y-%m-%d %H:%M:%S'))
    _data_json = get_info()
    get_taiwan(data_dict)
    format_data(_data_json, data_dict)
    provinces = list(data_dict.keys())
    values = list(data_dict.values())
    data_list = [[provinces[i], values[i]] for i in range(len(provinces))]
    _map = Map(init_opts=opts.InitOpts(width="752px", ))
    _map.set_global_opts(
        title_opts=opts.TitleOpts(title="中国nCoV肺炎疫情确诊图", pos_left="left", subtitle=_timestr),
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
    _map.add("中国累计确诊数据", data_list, maptype="china", is_map_symbol_show=False)
    _map.render(path="nCoV_map.html", template_name='nCoV.html')
    print(_timestr, "中国nCoV肺炎疫情确诊图更新成功")
