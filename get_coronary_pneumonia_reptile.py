#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' reptile module '

__author__ = 'saowu'

import logging

import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.INFO, filename='my.log', format=LOG_FORMAT)

# 加header伪装成浏览器
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) " \
             "Chrome/80.0.3987.100 Safari/537.36 "
headers = {'User-Agent': user_agent}


def get_city_info():
    """
    获取全国省市信息
    Returns:DataFrame

    """
    url_position = 'https://ncov.html5.qq.com/api/getPosition'
    r_position = requests.get(url_position, headers=headers)
    data_position = BeautifulSoup(r_position.text, 'html.parser')
    json1bj = json.loads(data_position.decode('utf-8'))
    data = []
    for i in json1bj['position']:
        for j in json1bj['position'][i]:
            for k in json1bj['position'][i][j]:
                dict1 = {'province': i, 'city': j, 'district': k}
                data.append(dict1)
    return pd.DataFrame(data)


def get_info(province, city, district):
    """
    获取地区疫情信息
    Args:
        province: 省
        city: 市
        district: 县（区）

    Returns:json

    """
    url_community = 'https://ncov.html5.qq.com/api/getCommunity?province=' + str(province) + '&city=' + str(
        city) + '&district=' + str(district)
    r_community = requests.get(url_community, headers=headers)
    data_community = BeautifulSoup(r_community.text, 'html.parser')
    jsonObj = json.loads(data_community.decode('utf-8'))
    return jsonObj


def format_data(info, result):
    """

    Args:格式化疫情信息
        info: 疫情信息
        result:结果集

    Returns:None

    """
    for i in info['community']:
        for j in info['community'][i]:
            for k in info['community'][i][j]:
                for x in info['community'][i][j][k]:
                    if len(x['article_source']) > 0:
                        for y in x['article_source']:
                            dict1 = {'province': x['province'], 'city': x['city'], 'district': x['district'],
                                     'street': x['street'], 'community': x['community'],
                                     'full_address': x['full_address'],
                                     'lat': x['lat'], 'lng': x['lng'], 'title': y['title'], 'url': y['url']}
                    else:
                        dict1 = {'province': x['province'], 'city': x['city'], 'district': x['district'],
                                 'street': x['street'], 'community': x['community'], 'full_address': x['full_address'],
                                 'lat': x['lat'], 'lng': x['lng'], 'title': '', 'url': ''}
                    result.append(dict1)


if __name__ == '__main__':
    result = []
    all_community = pd.DataFrame(
        columns=['province', 'city', 'district', 'street', 'community', 'full_address', 'lat', 'lng'])
    df = get_city_info()
    print('开始爬取......')
    for row in df.itertuples(index=True, name='province'):
        try:
            print(row.province, row.city, row.district)
            info = get_info(row.province, row.city, row.district)
            format_data(info, result)
        except Exception as e:
            logging.log(logging.WARNING, e)
        continue

    all_community = pd.DataFrame(result)
    all_community.to_csv('/Users/saowu/Downloads/冠状肺炎.csv')
    print('数据爬取完毕，已输出csv')
