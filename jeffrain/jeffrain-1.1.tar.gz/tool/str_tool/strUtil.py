#!/usr/bin/python3
# encoding: utf-8
import re


def parse_jsonp(jsonp_str):
    '''
    TODO 获取json
    LIMIT 开头不能有空格
    '''
    try:
        result = re.search('^[^(]*?\((.*)\)[^)]*$', jsonp_str)
        if result:
            print(result.group(0))
            return result.group(1)
        else:
            result = re.search('=(.*?);', jsonp_str)
            print(result.group(1))
            return result.group(1)
    except:
        raise ValueError('Invalid JSONP')


if __name__ == "__main__":
    jsonp_str = '___json___={"result":true,"data":{"message":0,"anim":0,"cartoon":0,"fiction":0,"commentNotice":0,"systemNotice":0,"subscribe":0,"total":0}};'
    parse_jsonp(jsonp_str)
