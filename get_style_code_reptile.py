#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' a test module '

__author__ = 'saowu'

# 加header伪装成浏览器
import os
import re

import requests
from bs4 import BeautifulSoup

user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36"
headers = {'User-Agent': user_agent}

address = "https://blog.crj0b.com/whoami/index.html"
ip = "https://blog.crj0b.com/"

localpath = "/Users/saowu/Downloads/source/"


def get_data():
    format_data(address)


def format_data(href):
    global response
    try:
        response = requests.get(href, headers=headers)
        response.encoding = 'utf-8'
    except Exception as e:
        print("请求错误:", e, 'path:', href)

    _filename = os.path.split(href)
    with open(localpath + _filename[1], 'w') as _file:
        _file.write(response.text)

    _soup = BeautifulSoup(response.text, 'html.parser')
    # print(_soup)

    re_compile = re.compile(r'^((\.\./)|(\./)|(/[0-9a-zA-Z])|[0-9a-zA-Z])')

    _links = _soup.find_all('link', href=re_compile)
    for _link in _links:
        wirte_file(_link['href'])

    _scripts = _soup.find_all('script', src=re_compile)
    for _script in _scripts:
        wirte_file(_script['src'])

    _imgs = _soup.find_all('img', src=re_compile)
    for _img in _imgs:
        wirte_file(_img['src'])

    _ahref = _soup.find_all('a', href=re_compile)
    for _a in _ahref:
        print(_a['href'])


def wirte_file(href):
    global ip
    if 'http' in href:
        return
    if '../' in href:
        file_url = href.replace('../', ip)
    elif './' in href:
        file_url = href.replace('./', ip)
    else:
        file_url = ip + href

    print(file_url)

    _response = requests.get(file_url)

    _filepath = localpath + href.replace('./', "")

    _filedir = os.path.split(_filepath)
    if not os.path.exists(_filedir[0]):
        os.makedirs(_filedir[0])
    isTextType = re.search("^(text/)", _response.headers['Content-Type'])
    if isTextType is None:
        with open(_filepath, 'wb') as _file:
            for chunk in _response.iter_content(chunk_size=1024):
                if chunk:
                    _file.write(chunk)
    else:
        with open(_filepath, 'w') as _file:
            _file.write(_response.text)


if __name__ == '__main__':
    get_data()
