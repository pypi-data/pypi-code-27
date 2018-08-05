#!/usr/bin/python3
# encoding: utf-8
import time


def get_timestamp(tag=13):
    '''
    TODO 获取10位和13位的常用网站的时间戳
    '''
    if tag == 10:
        return int(time.time())
    else:
        return int(round(time.time() * 1000))


def timestamp2Date(timestamp):
    if len(str(timestamp)) == 10:
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))
    else:
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp / 1000))

if __name__ == '__main__':
    print(get_timestamp())
    print(get_timestamp(tag=10))
    print(timestamp2Date(1527348609))
