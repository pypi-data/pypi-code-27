#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2018/7/24 15:49
@File    : ifind_rest_service.py
@contact : mmmaaaggg@163.com
@desc    :
"""
from flask import request, Flask
from flask_restplus import Resource, Api, reqparse
import pandas as pd
import logging
from datetime import datetime, date
from ifind_rest.exceptions import RequestError
import iFinDPy as ifind
from ifind_rest.config import config
logger = logging.getLogger(__name__)
STR_FORMAT_DATE = '%Y-%m-%d'
STR_FORMAT_DATETIME_WIND = '%Y-%m-%d %H:%M:%S'  # 2017-03-06 00:00:00
UN_AVAILABLE_DATETIME = datetime.strptime('1900-01-01', STR_FORMAT_DATE)
UN_AVAILABLE_DATE = UN_AVAILABLE_DATETIME.date()
app = Flask(__name__)
api = Api(app,
          title='同花顺 iFind Rest API',
          version='0.0.1',
          description='',
          )
header = {'Content-Type': 'application/json'}
rec = api.namespace('iFind', description='同花顺iFind接口')
# parser
data_serial_parser = reqparse.RequestParser().add_argument(
    'thscode', type=str, help="同花顺代码，可以是单个代码也可以是多个代码，代码之间用逗号(‘,’)隔开。例如 600004.SH,600007.SH"
).add_argument(
    'jsonIndicator', type=str, help="指标，可以是单个指标也可以是多个指标，指标指标用 分号(‘;’)隔开。例如 ths_close_price_stock;ths_open_price_stock"
).add_argument(
    'jsonparam', type=str, help="参数，可以是默认参数也根据说明可以对参数进行自定义赋值，参数和参数之间用逗号 (‘ , ’) 隔开， 参 数 的 赋 值 用 冒 号 (‘:’) 。 例 如 100;100"
).add_argument(
    'globalparam', type=str, help="参数，可以是默认参数也根据说明可以对参数进行自定义赋值，参数和参数之间用逗号 (‘, ’) 隔开， 参 数 的 赋 值 用 冒 号 (‘:’) 。 例 如 Days:Tradedays,Fill:Previous,Interval:D"
).add_argument(
    'begintime', type=str, help="开始时间，时间格式为 YYYY-MM-DD，例如 2018-06-24"
).add_argument(
    'endtime', type=str, help="截止时间，时间格式为 YYYY-MM-DD，例如 2018-07-24"
)


def format_2_date_str(dt):
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


def format_2_datetime_str(dt):
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


@rec.route('/THS_DateSerial/')
class THSDateSerial(Resource):

    @rec.expect(data_serial_parser)
    def post(self):
        """
        日期序列
        """
        # data_dic = request.json
        args = data_serial_parser.parse_args()
        logger.info('/THS_DateSerial/ args:%s' % args)
        ret_data = ifind.THS_DateSerial(**args)
        error_code = ret_data['errorcode']
        if error_code != 0:
            msg = ret_data['errmsg']
            logger.error('THS_DateSerial(%s) ErrorCode=%d %s' % (args, error_code, msg))
            raise RequestError(msg, None, error_code)

        tables = ret_data['tables']
        table_count = len(tables)
        data_df_list = []
        for nth_table in range(table_count):
            table = tables[nth_table]
            date_list = table['time']
            date_len = len(date_list)
            if date_len > 0:
                data = table['table']
                data_df = pd.DataFrame(data, index=date_list)
                data_df['ths_code'] = table['thscode']
                data_df_list.append(data_df)
        ret_df = pd.concat(data_df_list)
        ret_df.index.rename('time', inplace=True)
        ret_df.reset_index(inplace=True)
        # print('ret_df\n', ret_df)
        ret_dic = ret_df.to_dict()
        # print('ret_dic:\n', ret_dic)
        return ret_dic


def start_service():
    ths_login = ifind.THS_iFinDLogin(config.THS_LOGIN_USER_NAME, config.THS_LOGIN_PASSWORD)
    if ths_login == 0 or ths_login == -201:
        logger.info('成功登陆')
        try:
            app.run(host="0.0.0.0", debug=True)
        finally:
            ifind.THS_iFinDLogout()
            logger.info('成功登出')
    else:
        logger.error("登录失败")


if __name__ == '__main__':

    start_service()
