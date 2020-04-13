#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' a test module '

__author__ = 'saowu'

import json

import requests
import pypinyin
from bs4 import BeautifulSoup
from pyecharts import Map

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
    _data_json = get_info()
    get_taiwan(data_dict)
    format_data(_data_json, data_dict)
    provices = list(data_dict.keys())
    values = list(data_dict.values())
    map = Map("中国地区", '冠状病毒确诊病例', width=800, height=600)
    map.add("确诊病例", provices, values, visual_range=[0, 2000], maptype='china', is_visualmap=True,
            visual_text_color='#000')
    map.render(path="china_map.html")
