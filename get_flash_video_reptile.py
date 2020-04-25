#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' reptile module '

__author__ = 'saowu'

'''
flash播放器视频源文件爬取,支持.ts .m3u8
'''

import logging, os, urllib, socket, requests
from multiprocessing.pool import Pool
from time import sleep

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.WARNING, filename='.get_flash_video.log', format=LOG_FORMAT)

user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36"
headers = {'User-Agent': user_agent}
# 下载目录
out_filepath = '/Users/saowu/Downloads/other1/'
# 切片文件类型
file_type = '.ts'


def get_url(index):
    '''合成下载路径

    Args:
        index: 索引

    Returns:下载路径

    '''
    return "http://hls.cntv.myalicdn.com/asp/hls/450/0303000a/3/default/8bfe1a3f8dc54d13b99887d8c07e575d/%d.ts" % index


def download_ts(index):
    '''获取并下载ts文件

    Args:
        index: 索引

    Returns:

    '''
    response = requests.get(get_url(index), headers=headers, stream=True)
    if not response.status_code == 200:
        print('下载异常或完毕，请关闭进程')
    else:
        with open(out_filepath + str(index) + file_type, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
    response.close()


def work(index):
    '''多进程任务函数

    Args:
        index: 索引

    Returns:

    '''

    try:
        download_ts(index)
        print(str(index) + ".ts  success")
        sleep(1)
    except urllib.error.URLError as e:
        logging.WARNING(e)
        download_ts(index)
    except socket.timeout as e2:
        logging.WARNING(e2)
        download_ts(index)


def merge_file(filepath, outfile):
    '''合并.ts .m3u8文件

    Args:
        filepath: 合并文件夹路径
        outfile: 生成文件路径

    Returns:

    '''
    _outfile = open(outfile, 'ab+')
    paths = list(filter(lambda s: not s[0] == '.', os.listdir(filepath)))
    # .ts or .m3u8
    if paths[0][-3:] == '.ts':
        paths.sort(key=lambda x: int(x[:-3]))
    else:
        paths.sort(key=lambda x: int(x[:-5]))

    for name in paths:
        with open(filepath + name, 'rb')as _readfile:
            _outfile.write(_readfile.read())
    _outfile.close()
    print('合并完毕', outfile)


if __name__ == '__main__':

    # 防止远端主机重置此连接
    socket.setdefaulttimeout(20)
    # 定义进程池
    p = Pool(4)
    # 视频切片数量(需要给定)
    for i in range(0, 120):
        # 异步调用
        p.apply_async(work, args=(i,))
    print('Waiting for all subprocesses done...')
    p.close()
    p.join()

    # 合并切片文件
    merge_file(out_filepath, "/Users/saowu/Downloads/result.mp4")
