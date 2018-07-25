# -*- coding: utf-8 -*-
"""
Created on 2016-12-22
@author: MG
"""
import pandas as pd
import requests
import json
from datetime import datetime, date

STR_FORMAT_DATE = '%Y-%m-%d'
STR_FORMAT_DATETIME_WIND = '%Y-%m-%d %H:%M:%S'  # 2017-03-06 00:00:00.005000
UN_AVAILABLE_DATETIME = datetime.strptime('1900-01-01', STR_FORMAT_DATE)
UN_AVAILABLE_DATE = UN_AVAILABLE_DATETIME.date()


def format_2_date_str(dt) -> str:
    if dt is None:
        return None
    dt_type = type(dt)
    if dt_type == str:
        return dt
    elif dt_type == date:
        if dt > UN_AVAILABLE_DATE:
            return dt.strftime(STR_FORMAT_DATE)
        else:
            return None
    elif dt_type == datetime:
        if dt > UN_AVAILABLE_DATETIME:
            return dt.strftime(STR_FORMAT_DATE)
        else:
            return None
    else:
        return dt


def format_2_datetime_str(dt) -> str:
    if dt is None:
        return None
    dt_type = type(dt)
    if dt_type == str:
        return dt
    elif dt_type == date:
        if dt > UN_AVAILABLE_DATE:
            return dt.strftime(STR_FORMAT_DATE)
        else:
            return None
    elif dt_type == datetime:
        if dt > UN_AVAILABLE_DATETIME:
            return dt.strftime(STR_FORMAT_DATETIME_WIND)
        else:
            return None
    else:
        return dt


class APIError(Exception):
    def __init__(self, status, ret_dic):
        self.status = status
        self.ret_dic = ret_dic

    def __str__(self):
        return "APIError:status=POST / {} {}".format(self.status, self.ret_dic)


class IFinDInvoker:
    def __init__(self, url_str):
        self.url = url_str
        self.header = {'Content-Type': 'application/json'}

    def _url(self, path: str) -> str:
        return self.url + path

    def _public_post(self, path: str, req_data: str) -> list:

        # print('self._url(path):', self._url(path))
        ret_data = requests.post(self._url(path), data=req_data, headers=self.header)
        ret_dic = ret_data.json()

        if ret_data.status_code != 200:
            raise APIError(ret_data.status_code, ret_dic)
        else:
            return ret_dic

    def THS_DateSerial(self, thscode, jsonIndicator, jsonparam, globalparam, begintime, endtime) -> pd.DataFrame:
        """
        日期序列
        :param thscode:同花顺代码，可以是单个代码也可以是多个代码，代码之间用逗号(‘,’)隔开。例如 600004.SH,600007.SH
        :param jsonIndicator:指标，可以是单个指标也可以是多个指标，指标指标用 分号(‘;’)隔开。例如 ths_close_price_stock;ths_open_price_stock
        :param jsonparam:参数，可以是默认参数也根据说明可以对参数进行自定义赋值，参数和参数之间用逗号 (‘ , ’) 隔开， 参 数 的 赋 值 用 冒 号 (‘:’) 。 例 如 100;100
        :param globalparam:参数，可以是默认参数也根据说明可以对参数进行自定义赋值，参数和参数之间用逗号 (‘, ’) 隔开， 参 数 的 赋 值 用 冒 号 (‘:’) 。 例 如 Days:Tradedays,Fill:Previous,Interval:D
        :param begintime:开始时间，时间格式为 YYYY-MM-DD，例如 2018-06-24
        :param endtime:截止时间，时间格式为 YYYY-MM-DD，例如 2018-07-24
        :return:
        """
        path = 'THS_DateSerial/'
        req_data_dic = {"thscode": thscode, "jsonIndicator": jsonIndicator,
                        "jsonparam": jsonparam, "globalparam": globalparam,
                        "begintime": format_2_date_str(begintime),
                        "endtime": format_2_date_str(endtime)
                        }
        req_data = json.dumps(req_data_dic)
        json_dic = self._public_post(path, req_data)
        df = pd.DataFrame(json_dic)
        return df


if __name__ == "__main__":
    # url_str = "http://10.0.5.65:5000/wind/"
    url_str = "http://localhost:5000/iFind/"
    invoker = IFinDInvoker(url_str)

    try:
        data_df = invoker.THS_DateSerial(
            "600004.SH,600007.SH", "ths_close_price_stock;ths_open_price_stock", "100;100",
            "Days:Tradedays,Fill:Previous,Interval:D", "2018-06-24", "2018-07-24"
        )
        print(data_df)
    except APIError as exp:
        if exp.status == 500:
            print('APIError.status:', exp.status, exp.ret_dic['message'])
        else:
            print(exp.ret_dic.setdefault('error_code', ''), exp.ret_dic['message'])
    # date_str = rest.tdaysoffset(1, '2017-3-31')
    # print(date_str)
