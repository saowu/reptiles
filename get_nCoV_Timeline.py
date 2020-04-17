#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' a test module '

__author__ = 'saowu'

import json
import requests
from bs4 import BeautifulSoup
from pyecharts.charts import Timeline, Bar
import pyecharts.options as opts

province_list = [
    '安徽',
    '北京',
    '重庆',
    '福建',
    '甘肃',
    '广东',
    '广西',
    '贵州',
    '海南',
    '河北',
    '黑龙江',
    '河南',
    '香港',
    '湖北',
    '湖南',
    '内蒙古',
    '江苏',
    '江西',
    '吉林',
    '辽宁',
    '澳门',
    '宁夏',
    '青海',
    '陕西',
    '山东',
    '上海',
    '山西',
    '四川',
    '天津',
    '西藏',
    '新疆',
    '云南',
    '浙江',
    '台湾'
]
total_data = {}
china_confirmed_history = {}
china_deaths_history = {}
china_recovered_history = {}


def get_confirmed_info(url_community, name):
    # 1.爬取api数据
    r_community = requests.get(url_community)
    with open(name, 'w')as _file:
        _file.write(r_community.text)
    data_community = BeautifulSoup(r_community.text, 'html.parser')

    # 2.先爬取到本地，再本地读取，加快速度调试
    # with open(name, 'r')as _file:
    #     r_community = _file.read()
    # data_community = BeautifulSoup(r_community, 'html.parser')

    jsonObj = json.loads(data_community.decode('utf-8'))
    return jsonObj


def format_info(json_obj, result):
    for _country in json_obj['locations']:
        if _country['country'] == 'China':
            for _date in _country['history']:
                if _date not in result:
                    result[_date] = []
                result[_date].append(_country['history'][_date])
    format_taiwan_info(json_obj, result)


def format_taiwan_info(json_obj, result):
    for _country in json_obj['locations']:
        if _country['country_code'] == 'TW':
            for _date in _country['history']:
                if _date not in result:
                    result[_date] = []
                result[_date].append(_country['history'][_date])


# confirmed_info
total_data["confirmed_info"] = china_confirmed_history
# deaths_info
total_data["deaths_info"] = china_deaths_history
# recovered_info
total_data["recovered_info"] = china_recovered_history


def get_date_overlap_chart(day: str) -> Bar:
    def format_date(_list):
        return "20{}年{}月{}日 nCoV肺炎疫情数据".format(_list[2], _list[0], _list[1])

    return (
        Bar()
            .add_xaxis(xaxis_data=province_list)
            .add_yaxis(
            series_name="累计确诊",
            yaxis_data=total_data["confirmed_info"][day],
            label_opts=opts.LabelOpts(is_show=False),
        )
            .add_yaxis(
            series_name="累计死亡",
            yaxis_data=total_data["deaths_info"][day],
            label_opts=opts.LabelOpts(is_show=False),
        )
            .add_yaxis(
            series_name="累计治愈",
            yaxis_data=total_data["recovered_info"][day],
            label_opts=opts.LabelOpts(is_show=False),
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(
                title=format_date(day.split('/')), subtitle="数据来自 Coronavirus Tracker"
            ),
            tooltip_opts=opts.TooltipOpts(
                is_show=True, trigger="axis", axis_pointer_type="shadow"
            )
        )
    )


if __name__ == '__main__':
    confirmed_info = get_confirmed_info('https://coronavirus-tracker-api.herokuapp.com/confirmed', 'confirmed_info')
    deaths_info = get_confirmed_info('https://coronavirus-tracker-api.herokuapp.com/deaths', 'deaths_info')
    recovered_info = get_confirmed_info('https://coronavirus-tracker-api.herokuapp.com/recovered', 'recovered_info')
    format_info(confirmed_info, china_confirmed_history)
    format_info(deaths_info, china_deaths_history)
    format_info(recovered_info, china_recovered_history)
    # 生成时间轴
    timeline = Timeline(init_opts=opts.InitOpts(width="1440px", height="700px"))
    for day in china_confirmed_history.keys():
        timeline.add(get_date_overlap_chart(day=day), time_point=day)
    timeline.add_schema(is_auto_play=True, play_interval=1000)
    timeline.render("nCoV_timeline.html", template_name="nCoV2.html")
