#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' reptile module '

__author__ = 'saowu'

import logging
import requests
from bs4 import BeautifulSoup

'''
爬取小说文本（起点中文网免费文本）
'''

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.INFO, filename='my.log', format=LOG_FORMAT)

# 加header伪装成浏览器
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36"
cookie = "_qda_uuid=7c45e907-c770-d953-aca1-2517e23d5765; e1=%7B%22pid%22%3A%22qd_P_vipread%22%2C%22eid%22%3A%22%22%7D; e2=%7B%22pid%22%3A%22qd_P_vipread%22%2C%22eid%22%3A%22qd_R113%22%2C%22l1%22%3A3%7D; _csrfToken=4DGxRl2o7Aoqz2tbgc26L3Jzn37eoyAaPuHytmjn; newstatisticUUID=1582080881_1275796745; qdrs=0%7C3%7C0%7C0%7C1; showSectionCommentGuide=1; qdgd=1; rcr=1979049; bc=1979049; pageOps=1; lrbc=1979049%7C33357566%7C1; ywkey=ywIySbCdOsl4; ywguid=786021717; ywopenid=BBE91EE9461C58F9904BD2387FA094A7"
headers = {'User-Agent': user_agent, "Cookie": cookie}

ip_adress_path = 'https:'
path = '//read.qidian.com/chapter/f3c3YK2k5Ypxo3Pbs2jtrw2/zW2ue59I_x5Ms5iq0oQwLQ2'


def set_url():
    return ip_adress_path + path


def get_data():
    global path

    try:
        response = requests.get(set_url(), headers=headers)
    except Exception as e:
        print("请求错误:", e, 'path:', path)

    soup = BeautifulSoup(response.text, 'html.parser')

    try:
        path = soup.find_all('a', string='下一章')[0]['href']
    except IndexError as e:
        print("已到末章")
        return False

    title = soup.find_all('h3', class_='j_chapterName')[0].find_all('span', class_='content-wrap')[0].text
    content = soup.find_all('div', class_='read-content j_readContent')

    wirte_file(title, str(content))
    return True


def wirte_file(title, content):
    with open('/Users/saowu/Downloads/xiaosuo/' + title + '.txt', 'w') as _file:
        _file.write(content)
    print(title)


if __name__ == '__main__':
    flag = True
    while flag:
        flag = get_data()
    print('下载结束')
