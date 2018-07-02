# -*- coding: utf-8 -*-
'''
基础操作接口
'''
import json
import requests
from pandas.io.json import json_normalize
from lixinger_openapi.token import get_token

STOCK_FUNDAMENTAL_INFO_URL = "https://www.lixinger.com/api/open/a/stock/fundamental-info"
STOCK_FS_INFO_URL = "https://www.lixinger.com/api/open/a/stock/fs-info"
INDICE_FUNDAMENTAL_INFO_URL = "https://www.lixinger.com/api/open/a/indice/fundamental-info"

HK_STOCK_FUNDAMENTAL_INFO_URL = "https://www.lixinger.com/api/open/h/stock/fundamental-info"
HK_STOCK_FS_INFO_URL = "https://www.lixinger.com/api/open/h/stock/fs-info"
HK_INDICE_FUNDAMENTAL_INFO_URL = "https://www.lixinger.com/api/open/h/indice/fundamental-info"

def basic_query_info(url, date, startDate, endDate, stockCodes, metrics):
    '''
    基础接口，返回json结构
    上层接口的参数列表和返回结果类型都一致，可重用统一底层接口
    '''
    if get_token() is None or metrics is None:
        return None
    query = {}
    if date is not None:
        query["date"] = date
    if startDate is not None:
        query["startDate"] = startDate
    if endDate is not None:
        query["endDate"] = endDate
    if stockCodes is not None:
        query["stockCodes"] = stockCodes
    query["token"] = get_token()
    query["metrics"] = metrics
    headers = {"Content-Type": "application/json"}
    response = requests.post(url=url, data=json.dumps(query), headers=headers)
    if response.status_code != 200:
        return None
    return response.json()

def basic_query_info_df(url, date, startDate, endDate, stockCodes, metrics):
    '''
    基础接口，返回字典结构
    key     value       type
    code    返回值       int
    data    返回结果     dataframe
    msg     返回消息     string
    '''
    return_value = {'code': -1, 'data': None, 'msg': ''}
    rlt = basic_query_info(url, date, startDate, endDate, stockCodes, metrics)
    if rlt is None:
        return_value['msg'] = 'query failed.'
    else:
        return_value['code'] = rlt['code']
        return_value['data'] = json_normalize(rlt['data'])
        return_value['msg'] = rlt['msg']
    return return_value
