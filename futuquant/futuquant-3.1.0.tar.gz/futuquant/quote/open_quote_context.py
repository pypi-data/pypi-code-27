# -*- coding: utf-8 -*-
"""
    Market quote and trade context setting
"""

import datetime
import math
from time import sleep

import pandas as pd
from futuquant.common.open_context_base import OpenContextBase, ContextStatus
from futuquant.quote.quote_query import *

MAX_KLINE_SUB_COUNT = 100

class OpenQuoteContext(OpenContextBase):
    """行情上下文对象类"""

    def __init__(self, host='127.0.0.1', port=11111):
        """
        初始化Context对象
        :param host: host地址
        :param port: 端口
        """
        self._ctx_subscribe = {}
        super(OpenQuoteContext, self).__init__(host, port, True)

    def close(self):
        """
        关闭上下文对象。

        .. code:: python

            from futuquant import *
            quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
            quote_ctx.close()
        """
        super(OpenQuoteContext, self).close()

    def on_api_socket_reconnected(self):
        """for API socket reconnected"""
        # auto subscriber
        resub_count = 0
        subtype_list = []
        code_list = []

        resub_dict = copy(self._ctx_subscribe)
        subtype_all_cnt = len(resub_dict.keys())
        subtype_cur_cnt = 0

        ret_code = RET_OK
        ret_msg = ''

        for subtype in resub_dict.keys():
            subtype_cur_cnt += 1
            code_set = resub_dict[subtype]
            code_list_new = [code for code in code_set]
            if len(code_list_new) == 0:
                continue

            if len(code_list) == 0:
                code_list = code_list_new
                subtype_list = [subtype]

            is_need_sub = False
            if code_list == code_list_new:
                if subtype not in subtype_list:
                    subtype_list.append(subtype)   # 合并subtype请求
            else:
                ret_code, ret_msg = self._reconnect_subscribe(code_list, subtype_list)
                logger.debug("reconnect subscribe code_count={} ret_code={} ret_msg={} subtype_list={} code_list={}".format(
                    len(code_list), ret_code, ret_msg, subtype_list, code_list))
                if ret_code != RET_OK:
                    break

                resub_count += len(code_list)
                code_list = code_list_new
                subtype_list = [subtype]

            # 循环即将结束
            if subtype_cur_cnt == subtype_all_cnt and len(code_list):
                ret_code, ret_msg = self._reconnect_subscribe(code_list, subtype_list)
                logger.debug("reconnect subscribe code_count={} ret_code={} ret_msg={} subtype_list={} code_list={}".format(len(code_list), ret_code, ret_msg, subtype_list, code_list))
                if ret_code != RET_OK:
                    break
                resub_count += len(code_list)
                code_list = []
                subtype_list = []

        logger.debug("reconnect subscribe all code_count={} ret_code={} ret_msg={}".format(resub_count, ret_code, ret_msg))

        # 重定阅失败，重连
        if ret_code != RET_OK:
            logger.error("reconnect subscribe error, close connect and retry!!")
            self._status = ContextStatus.Start
            self._wait_reconnect()
        return ret_code, ret_msg

    def get_trading_days(self, market, start_date=None, end_date=None):
        """get the trading days"""
        if market is None or is_str(market) is False:
            error_str = ERROR_STR_PREFIX + "the type of market param is wrong"
            return RET_ERROR, error_str

        ret, msg, start_date, end_date = normalize_start_end_date(start_date, end_date, 365)
        if ret != RET_OK:
            return ret, msg

        query_processor = self._get_sync_query_processor(
            TradeDayQuery.pack_req, TradeDayQuery.unpack_rsp)

        # the keys of kargs should be corresponding to the actual function arguments
        kargs = {
            'market': market,
            'start_date': start_date,
            'end_date': end_date,
            'conn_id': self.get_sync_conn_id()
        }
        ret_code, msg, trade_day_list = query_processor(**kargs)

        if ret_code != RET_OK:
            return RET_ERROR, msg

        return RET_OK, trade_day_list

    def get_stock_basicinfo(self, market, stock_type=SecurityType.STOCK):
        """
        获取指定市场中特定类型的股票基本信息
        :param market: 市场类型，futuquant.common.constsnt.Market
        :param stock_type: 股票类型， futuquant.common.constsnt.SecurityType
        :return: (ret_code, content)
                ret_code 等于RET_OK时， content为Pandas.DataFrame数据, 否则为错误原因字符串, 数据列格式如下
            =================   ===========   ==============================================================================
            参数                  类型                        说明
            =================   ===========   ==============================================================================
            code                str            股票代码
            name                str            名字
            lot_size            int            每手数量
            stock_type          str            股票类型，参见SecurityType
            stock_child_type    str            涡轮子类型，参见WrtType
            stock_owner         str            正股代码
            listing_date        str            上市时间
            stock_id            int            股票id
            =================   ===========   ==============================================================================

        :example:

            .. code-block:: python

            from futuquant import *
            quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
            print(quote_ctx.get_stock_basicinfo(Market.HK, SecurityType.WARRANT))
            quote_ctx.close()
        """
        param_table = {'market': market, 'stock_type': stock_type}
        for x in param_table:
            param = param_table[x]
            if param is None or is_str(param) is False:
                error_str = ERROR_STR_PREFIX + "the type of %s param is wrong" % x
                return RET_ERROR, error_str

        query_processor = self._get_sync_query_processor(
            StockBasicInfoQuery.pack_req, StockBasicInfoQuery.unpack_rsp)
        kargs = {
            "market": market,
            'stock_type': stock_type,
            'conn_id': self.get_sync_conn_id()
        }

        ret_code, msg, basic_info_list = query_processor(**kargs)
        if ret_code != RET_OK:
            return ret_code, msg

        col_list = [
            'code', 'name', 'lot_size', 'stock_type', 'stock_child_type',
            "stock_owner", "listing_date", "stock_id"
        ]

        basic_info_table = pd.DataFrame(basic_info_list, columns=col_list)

        return RET_OK, basic_info_table

    def get_multiple_history_kline(self,
                                   codelist,
                                   start=None,
                                   end=None,
                                   ktype=KLType.K_DAY,
                                   autype=AuType.QFQ):
        """
        获取多只股票的历史k线数据

        :param codelist: 股票代码列表，list或str。例如：['HK.00700', 'HK.00001']，'HK.00700,HK.00001'
        :param start: 起始时间，例如2017-06-20
        :param end: 结束时间
        :param ktype: k线类型，参见KLType
        :param autype: 复权类型，参见AuType
        :return: 成功时返回(RET_OK, [data])，data是DataFrame数据, 数据列格式如下

            =================   ===========   ==============================================================================
            参数                  类型                        说明
            =================   ===========   ==============================================================================
            code                str            股票代码
            time_key            str            k线时间
            open                float          开盘价
            close               float          收盘价
            high                float          最高价
            low                 float          最低价
            pe_ratio            float          市盈率
            turnover_rate       float          换手率
            volume              int            成交量
            turnover            float          成交额
            change_rate         float          涨跌幅
            last_close          float          昨收价
            =================   ===========   ==============================================================================

            失败时返回(RET_ERROR, data)，其中data是错误描述字符串

        """
        if is_str(codelist):
            codelist = codelist.split(',')
        elif isinstance(codelist, list):
            pass
        else:
            return RET_ERROR, "code list must be like ['HK.00001', 'HK.00700'] or 'HK.00001,HK.00700'"
        result = []
        for code in codelist:
            ret, data = self.get_history_kline(code, start, end, ktype, autype)
            if ret != RET_OK:
                return RET_ERROR, 'get history kline error {},{},{},{}'.format(code, start, end, ktype)
            result.append(data)
        return 0, result

    def get_history_kline(self,
                          code,
                          start=None,
                          end=None,
                          ktype=KLType.K_DAY,
                          autype=AuType.QFQ,
                          fields=[KL_FIELD.ALL]):
        """
        得到本地历史k线，需先参照帮助文档下载k线

        :param code: 股票代码
        :param start: 开始时间，例如2017-06-20
        :param end:  结束时间
        :param ktype: k线类型， 参见 KLType 定义
        :param autype: 复权类型, 参见 AuType 定义
        :param fields: 需返回的字段列表，参见 KL_FIELD 定义 KL_FIELD.ALL  KL_FIELD.OPEN ....
        :return: (ret, data)

                ret == RET_OK 返回pd dataframe数据，data.DataFrame数据, 数据列格式如下

                ret != RET_OK 返回错误字符串

            =================   ===========   ==============================================================================
            参数                  类型                        说明
            =================   ===========   ==============================================================================
            code                str            股票代码
            time_key            str            k线时间
            open                float          开盘价
            close               float          收盘价
            high                float          最高价
            low                 float          最低价
            pe_ratio            float          市盈率
            turnover_rate       float          换手率
            volume              int            成交量
            turnover            float          成交额
            change_rate         float          涨跌幅
            last_close          float          昨收价
            =================   ===========   ==============================================================================

        :example:

        .. code:: python

            from futuquant import *
            quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
            print(quote_ctx.get_history_kline('HK.00700', start='2017-06-20', end='2017-06-22'))
            quote_ctx.close()
        """

        if start is not None and is_str(start) is False:
            error_str = ERROR_STR_PREFIX + "the type of start param is wrong"
            return RET_ERROR, error_str

        if end is not None and is_str(end) is False:
            error_str = ERROR_STR_PREFIX + "the type of end param is wrong"
            return RET_ERROR, error_str

        req_fields = unique_and_normalize_list(fields)
        if not fields:
            req_fields = copy(KL_FIELD.ALL_REAL)
        req_fields = KL_FIELD.normalize_field_list(req_fields)
        if not req_fields:
            error_str = ERROR_STR_PREFIX + "the type of fields param is wrong"
            return RET_ERROR, error_str

        if autype is None:
            autype = 'None'

        param_table = {'code': code, 'ktype': ktype, 'autype': autype}
        for x in param_table:
            param = param_table[x]
            if param is None or is_str(param) is False:
                error_str = ERROR_STR_PREFIX + "the type of %s param is wrong" % x
                return RET_ERROR, error_str

        # format start end date
        ret, msg, req_start, end = normalize_start_end_date(start, end, 365)
        if ret != RET_OK:
            return ret, msg

        max_kl_num = 1000
        data_finish = False
        list_ret = []
        # 循环请求数据，避免一次性取太多超时
        while not data_finish:
            kargs = {
                "code": code,
                "start_date": req_start,
                "end_date": end,
                "ktype": ktype,
                "autype": autype,
                "fields": copy(req_fields),
                "max_num": max_kl_num,
                "conn_id": self.get_sync_conn_id()
            }
            query_processor = self._get_sync_query_processor(
                HistoryKlineQuery.pack_req, HistoryKlineQuery.unpack_rsp)
            ret_code, msg, content = query_processor(**kargs)
            if ret_code != RET_OK:
                return ret_code, msg

            list_kline, has_next, next_time = content
            data_finish = (not has_next) or (not next_time)
            req_start = next_time
            for dict_item in list_kline:
                list_ret.append(dict_item)

        # 表头列
        col_list = ['code']
        for field in req_fields:
            str_field = KL_FIELD.DICT_KL_FIELD_STR[field]
            if str_field not in col_list:
                col_list.append(str_field)

        kline_frame_table = pd.DataFrame(list_ret, columns=col_list)

        return RET_OK, kline_frame_table

    def get_autype_list(self, code_list):
        """
        获取给定股票列表的复权因子

        :param code_list: 股票列表，例如['HK.00700']
        :return: (ret, data)

                ret == RET_OK 返回pd dataframe数据，data.DataFrame数据, 数据列格式如下

                ret != RET_OK 返回错误字符串

                =====================   ===========   ==============================================================
                参数                      类型                        说明
                =====================   ===========   ==============================================================
                code                    str            股票代码
                ex_div_date             str            除权除息日
                split_ratio             float          拆合股比例； double，例如，对于5股合1股为1/5，对于1股拆5股为5/1
                per_cash_div            float          每股派现
                per_share_div_ratio     float          每股送股比例
                per_share_trans_ratio   float          每股转增股比例
                allotment_ratio         float          每股配股比例
                allotment_price         float          配股价
                stk_spo_ratio           float          增发比例
                stk_spo_price           float          增发价格
                forward_adj_factorA     float          前复权因子A
                forward_adj_factorB     float          前复权因子B
                backward_adj_factorA    float          后复权因子A
                backward_adj_factorB    float          后复权因子B
                =====================   ===========   ==============================================================

        """
        code_list = unique_and_normalize_list(code_list)

        for code in code_list:
            if code is None or is_str(code) is False:
                error_str = ERROR_STR_PREFIX + "the type of param in code_list is wrong"
                return RET_ERROR, error_str

        query_processor = self._get_sync_query_processor(
            ExrightQuery.pack_req, ExrightQuery.unpack_rsp)
        kargs = {
            "stock_list": code_list,
            "conn_id": self.get_sync_conn_id()
        }
        ret_code, msg, exr_record = query_processor(**kargs)
        if ret_code == RET_ERROR:
            return ret_code, msg

        col_list = [
            'code', 'ex_div_date', 'split_ratio', 'per_cash_div',
            'per_share_div_ratio', 'per_share_trans_ratio', 'allotment_ratio',
            'allotment_price', 'stk_spo_ratio', 'stk_spo_price',
            'forward_adj_factorA', 'forward_adj_factorB',
            'backward_adj_factorA', 'backward_adj_factorB'
        ]

        exr_frame_table = pd.DataFrame(exr_record, columns=col_list)

        return RET_OK, exr_frame_table

    def get_market_snapshot(self, code_list):
        """
        获取市场快照

        :param code_list: 股票列表
        :return: (ret, data)

                ret == RET_OK 返回pd dataframe数据，data.DataFrame数据, 数据列格式如下

                ret != RET_OK 返回错误字符串

                =======================   =============   ==============================================================
                参数                       类型                        说明
                =======================   =============   ==============================================================
                code                       str            股票代码
                update_time                str            更新时间(yyyy-MM-dd HH:mm:ss)
                last_price                 float          最新价格
                open_price                 float          今日开盘价
                high_price                 float          最高价格
                low_price                  float          最低价格
                prev_close_price           float          昨收盘价格
                volume                     int            成交数量
                turnover                   float          成交金额
                turnover_rate              float          换手率
                suspension                 bool           是否停牌(True表示停牌)
                listing_date               str            上市日期 (yyyy-MM-dd)
                circular_market_val        float          流通市值
                total_market_val           float          总市值
                wrt_valid                  bool           是否是窝轮
                wrt_conversion_ratio       float          换股比率
                wrt_type                   str            窝轮类型，参见WrtType
                wrt_strike_price           float          行使价格
                wrt_maturity_date          str            格式化窝轮到期时间
                wrt_end_trade              str            格式化窝轮最后交易时间
                wrt_code                   str            窝轮对应的正股
                wrt_recovery_price         float          窝轮回收价
                wrt_street_vol             float          窝轮街货量
                wrt_issue_vol              float          窝轮发行量
                wrt_street_ratio           float          窝轮街货占比
                wrt_delta                  float          窝轮对冲值
                wrt_implied_volatility     float          窝轮引伸波幅
                wrt_premium                float          窝轮溢价
                lot_size                   int            每手股数
                issued_shares              int            发行股本
                net_asset                  int            资产净值
                net_profit                 int            净利润
                earning_per_share          float          每股盈利
                outstanding_shares         int            流通股本
                net_asset_per_share        float          每股净资产
                ey_ratio                   float          收益率
                pe_ratio                   float          市盈率
                pb_ratio                   float          市净率
                price_spread               float          当前摆盘价差亦即摆盘数据的买档或卖档的相邻档位的报价差
                =======================   =============   ==============================================================
        """
        code_list = unique_and_normalize_list(code_list)
        if not code_list:
            error_str = ERROR_STR_PREFIX + "the type of code param is wrong"
            return RET_ERROR, error_str

        query_processor = self._get_sync_query_processor(
            MarketSnapshotQuery.pack_req, MarketSnapshotQuery.unpack_rsp)
        kargs = {
            "stock_list": code_list,
            "conn_id": self.get_sync_conn_id()
        }

        ret_code, msg, snapshot_list = query_processor(**kargs)
        if ret_code == RET_ERROR:
            return ret_code, msg

        col_list = [
            'code',
            'update_time',
            'last_price',
            'open_price',
            'high_price',
            'low_price',
            'prev_close_price',
            'volume',
            'turnover',
            'turnover_rate',
            'suspension',
            'listing_date',
            'circular_market_val',
            'total_market_val',
            'wrt_valid',
            'wrt_conversion_ratio',
            'wrt_type',
            'wrt_strike_price',
            'wrt_maturity_date',
            'wrt_end_trade',
            'wrt_code',
            'wrt_recovery_price',
            'wrt_street_vol',
            'wrt_issue_vol',
            'wrt_street_ratio',
            'wrt_delta',
            'wrt_implied_volatility',
            'wrt_premium',
            'lot_size',
            # 2017.11.6 add
            'issued_shares',
            'net_asset',
            'net_profit',
            'earning_per_share',
            'outstanding_shares',
            'net_asset_per_share',
            'ey_ratio',
            'pe_ratio',
            'pb_ratio',
            # 2017.1.25 add
            'price_spread',
        ]

        snapshot_frame_table = pd.DataFrame(snapshot_list, columns=col_list)

        return RET_OK, snapshot_frame_table

    def get_rt_data(self, code):
        """
        获取指定股票的分时数据

        :param code: 股票代码，例如，HK.00700，US.APPL
        :return: (ret, data)

                ret == RET_OK 返回pd dataframe数据，data.DataFrame数据, 数据列格式如下

                ret != RET_OK 返回错误字符串

                =====================   ===========   ==============================================================
                参数                      类型                        说明
                =====================   ===========   ==============================================================
                code                    str            股票代码
                time                    str            时间(yyyy-MM-dd HH:mm:ss)
                data_status             bool           数据状态；正确为True，伪造为False
                opened_mins             int            零点到当前多少分钟
                cur_price               float          当前价格
                last_close              float          昨天收盘的价格
                avg_price               float          平均价格
                volume                  float          成交量
                turnover                float          成交金额
                =====================   ===========   ==============================================================
        """
        if code is None or is_str(code) is False:
            error_str = ERROR_STR_PREFIX + "the type of param in code is wrong"
            return RET_ERROR, error_str

        query_processor = self._get_sync_query_processor(
            RtDataQuery.pack_req, RtDataQuery.unpack_rsp)
        kargs = {
            "code": code,
            "conn_id": self.get_sync_conn_id()
        }

        ret_code, msg, rt_data_list = query_processor(**kargs)
        if ret_code == RET_ERROR:
            return ret_code, msg

        for x in rt_data_list:
            x['code'] = code

        col_list = [
            'code', 'time', 'is_blank', 'opened_mins', 'cur_price',
            'last_close', 'avg_price', 'volume', 'turnover'
        ]

        rt_data_table = pd.DataFrame(rt_data_list, columns=col_list)

        return RET_OK, rt_data_table

    def get_plate_list(self, market, plate_class):
        """
        获取板块集合下的子板块列表

        :param market: 市场标识，注意这里不区分沪，深,输入沪或者深都会返回沪深市场的子板块（这个是和客户端保持一致的）参见Market
        :param plate_class: 板块分类，参见Plate
        :return: ret == RET_OK 返回pd dataframe数据，data.DataFrame数据, 数据列格式如下

                ret != RET_OK 返回错误字符串

                =====================   ===========   ==============================================================
                参数                      类型                        说明
                =====================   ===========   ==============================================================
                code                    str            股票代码
                plate_name              str            板块名字
                plate_id                str            板块id
                =====================   ===========   ==============================================================
        """
        param_table = {'market': market, 'plate_class': plate_class}
        for x in param_table:
            param = param_table[x]
            if param is None or is_str(market) is False:
                error_str = ERROR_STR_PREFIX + "the type of market param is wrong"
                return RET_ERROR, error_str

        if market not in MKT_MAP:
            error_str = ERROR_STR_PREFIX + "the value of market param is wrong "
            return RET_ERROR, error_str

        if plate_class not in PLATE_CLASS_MAP:
            error_str = ERROR_STR_PREFIX + "the class of plate is wrong"
            return RET_ERROR, error_str

        query_processor = self._get_sync_query_processor(
            SubplateQuery.pack_req, SubplateQuery.unpack_rsp)
        kargs = {
            'market': market,
            'plate_class': plate_class,
            'conn_id': self.get_sync_conn_id()
        }

        ret_code, msg, subplate_list = query_processor(**kargs)
        if ret_code == RET_ERROR:
            return ret_code, msg

        col_list = ['code', 'plate_name', 'plate_id']

        subplate_frame_table = pd.DataFrame(subplate_list, columns=col_list)

        return RET_OK, subplate_frame_table

    def get_plate_stock(self, plate_code):
        """
        获取特定板块下的股票列表

        :param plate_code: 板块代码, string, 例如，”SH.BK0001”，”SH.BK0002”，先利用获取子版块列表函数获取子版块代码
        :return: (ret, data)

                ret == RET_OK 返回pd dataframe数据，data.DataFrame数据, 数据列格式如下

                ret != RET_OK 返回错误字符串

                =====================   ===========   ==============================================================
                参数                      类型                        说明
                =====================   ===========   ==============================================================
                code                    str            股票代码
                lot_size                int            每手股数
                stock_name              str            股票名称
                stock_owner             str            所属正股的代码
                stock_child_type        str            股票子类型，参见WrtType
                stock_type              str            股票类型，参见SecurityType
                list_time               str            上市时间
                stock_id                int            股票id
                =====================   ===========   ==============================================================
        """
        if plate_code is None or is_str(plate_code) is False:
            error_str = ERROR_STR_PREFIX + "the type of code is wrong"
            return RET_ERROR, error_str

        query_processor = self._get_sync_query_processor(
            PlateStockQuery.pack_req, PlateStockQuery.unpack_rsp)
        kargs = {
            "plate_code": plate_code,
            "conn_id": self.get_sync_conn_id()
        }

        ret_code, msg, plate_stock_list = query_processor(**kargs)
        if ret_code == RET_ERROR:
            return ret_code, msg

        col_list = [
            'code', 'lot_size', 'stock_name', 'stock_owner',
            'stock_child_type', 'stock_type', 'list_time', 'stock_id',
        ]
        plate_stock_table = pd.DataFrame(plate_stock_list, columns=col_list)

        return RET_OK, plate_stock_table

    def get_broker_queue(self, code):
        """
        获取股票的经纪队列

        :param code: 股票代码
        :return: (ret, bid_frame_table, ask_frame_table)或(ret, err_message)

                ret == RET_OK 返回pd dataframe数据，数据列格式如下

                ret != RET_OK 后面两项为错误字符串

                bid_frame_table 经纪买盘数据

                =====================   ===========   ==============================================================
                参数                      类型                        说明
                =====================   ===========   ==============================================================
                code                    str             股票代码
                bid_broker_id           int             经纪买盘id
                bid_broker_name         str             经纪买盘名称
                bid_broker_pos          int             经纪档位
                =====================   ===========   ==============================================================

                ask_frame_table 经纪卖盘数据

                =====================   ===========   ==============================================================
                参数                      类型                        说明
                =====================   ===========   ==============================================================
                code                    str             股票代码
                ask_broker_id           int             经纪卖盘id
                ask_broker_name         str             经纪卖盘名称
                ask_broker_pos          int             经纪档位
                =====================   ===========   ==============================================================
        """
        if code is None or is_str(code) is False:
            error_str = ERROR_STR_PREFIX + "the type of param in code is wrong"
            return RET_ERROR, error_str

        query_processor = self._get_sync_query_processor(
            BrokerQueueQuery.pack_req, BrokerQueueQuery.unpack_rsp)
        kargs = {
            "code": code,
            "conn_id": self.get_sync_conn_id()
        }

        ret_code, ret_msg, content = query_processor(**kargs)
        if ret_code != RET_OK:
            return ret_code, ret_msg, ret_msg

        (_, bid_list, ask_list) = content
        col_bid_list = [
            'code', 'bid_broker_id', 'bid_broker_name', 'bid_broker_pos'
        ]
        col_ask_list = [
            'code', 'ask_broker_id', 'ask_broker_name', 'ask_broker_pos'
        ]

        bid_frame_table = pd.DataFrame(bid_list, columns=col_bid_list)
        ask_frame_table = pd.DataFrame(ask_list, columns=col_ask_list)
        return RET_OK, bid_frame_table, ask_frame_table

    def _check_subscribe_param(self, code_list, subtype_list):

        code_list = unique_and_normalize_list(code_list)
        subtype_list = unique_and_normalize_list(subtype_list)

        if len(code_list) == 0:
            msg = ERROR_STR_PREFIX + 'code_list is null'
            return RET_ERROR, msg, code_list, subtype_list

        if len(subtype_list) == 0:
            msg = ERROR_STR_PREFIX + 'subtype_list is null'
            return RET_ERROR, msg, code_list, subtype_list

        for subtype in subtype_list:
            if subtype not in SUBTYPE_MAP:
                subtype_str = ','.join([x for x in SUBTYPE_MAP])
                msg = ERROR_STR_PREFIX + 'subtype is %s , which is wrong. (%s)' % (
                    subtype, subtype_str)
                return RET_ERROR, msg, code_list, subtype_list

        for code in code_list:
            ret, msg = split_stock_str(code)
            if ret != RET_OK:
                return RET_ERROR, msg, code_list, subtype_list

        return RET_OK, "", code_list, subtype_list

    def subscribe(self, code_list, subtype_list, is_first_push=True):
        """
        订阅注册需要的实时信息，指定股票和订阅的数据类型即可

        注意：len(code_list) * 订阅的K线类型的数量 <= 100

        :param code_list: 需要订阅的股票代码列表
        :param subtype_list: 需要订阅的数据类型列表，参见SubType
        :param is_first_push: 订阅成功后是否马上推送一次数据
        :return: (ret, err_message)

                ret == RET_OK err_message为None

                ret != RET_OK err_message为错误描述字符串
        :example:

        .. code:: python

        from futuquant import *
        quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
        print(quote_ctx.subscribe(['HK.00700'], [SubType.QUOTE)])
        quote_ctx.close()
        """
        return self._subscribe_impl(code_list, subtype_list, is_first_push)

    def _subscribe_impl(self, code_list, subtype_list, is_first_push):

        ret, msg, code_list, subtype_list = self._check_subscribe_param(code_list, subtype_list)
        if ret != RET_OK:
            return ret, msg

        kline_sub_count = 0
        for sub_type in subtype_list:
            if sub_type in KLINE_SUBTYPE_LIST:
                kline_sub_count += 1

        if kline_sub_count * len(code_list) > MAX_KLINE_SUB_COUNT:
            return RET_ERROR, 'Too many subscription'

        query_processor = self._get_sync_query_processor(SubscriptionQuery.pack_subscribe_req,
                                                         SubscriptionQuery.unpack_subscribe_rsp)

        kargs = {
            'code_list': code_list,
            'subtype_list': subtype_list,
            'conn_id': self.get_sync_conn_id(),
            'is_first_push': is_first_push
        }
        ret_code, msg, _ = query_processor(**kargs)

        if ret_code != RET_OK:
            return RET_ERROR, msg

        for subtype in subtype_list:
            if subtype not in self._ctx_subscribe:
                self._ctx_subscribe[subtype] = set()
            code_set = self._ctx_subscribe[subtype]
            for code in code_list:
                code_set.add(code)

        ret_code, msg, push_req_str = SubscriptionQuery.pack_push_req(
            code_list, subtype_list, self.get_async_conn_id(), is_first_push)

        if ret_code != RET_OK:
            return RET_ERROR, msg

        ret_code, msg = self._send_async_req(push_req_str)
        if ret_code != RET_OK:
            return RET_ERROR, msg

        return RET_OK, None

    def _reconnect_subscribe(self, code_list, subtype_list):

        # 将k线定阅和其它定阅区分开来
        kline_sub_list = []
        other_sub_list = []
        for sub in subtype_list:
            if sub in KLINE_SUBTYPE_LIST:
                kline_sub_list.append(sub)
            else:
                other_sub_list.append(sub)

        # 连接断开时，可能会有大批股票需要重定阅，分次定阅，提高成功率
        kline_sub_one_size = 1
        if len(kline_sub_list) > 0:
            kline_sub_one_size = math.floor(MAX_KLINE_SUB_COUNT / len(kline_sub_list))

        sub_info_list = [
            {"sub_list": kline_sub_list, "one_size":  kline_sub_one_size},
            {"sub_list": other_sub_list, "one_size": 100},
        ]

        ret_code = RET_OK
        ret_data = None

        for info in sub_info_list:
            sub_list = info["sub_list"]
            one_size = info["one_size"]
            all_count = len(code_list)
            start_idx = 0

            while start_idx < all_count and len(sub_list):
                sub_count = one_size if start_idx + one_size <= all_count else (all_count - start_idx)
                sub_codes = code_list[start_idx: start_idx + sub_count]
                start_idx += sub_count

                ret_code, ret_data = self._subscribe_impl(sub_codes, sub_list, False)
                if ret_code != RET_OK:
                    break
            if ret_code != RET_OK:
                break

        return ret_code, ret_data

    def unsubscribe(self, code_list, subtype_list):
        """
        取消订阅
        :param code_list: 取消订阅的股票代码列表
        :param subtype_list: 取消订阅的类型，参见SubType
        :return: (ret, err_message)

                ret == RET_OK err_message为None

                ret != RET_OK err_message为错误描述字符串
        """

        ret, msg, code_list, subtype_list = self._check_subscribe_param(code_list, subtype_list)
        if ret != RET_OK:
            return ret, msg

        query_processor = self._get_sync_query_processor(SubscriptionQuery.pack_unsubscribe_req,
                                                         SubscriptionQuery.unpack_unsubscribe_rsp)

        kargs = {
            'code_list': code_list,
            'subtype_list': subtype_list,
            "conn_id": self.get_sync_conn_id()
        }

        for subtype in subtype_list:
            if subtype not in self._ctx_subscribe:
                continue
            code_set = self._ctx_subscribe[subtype]
            for code in code_list:
                if code not in code_set:
                    continue
                code_set.remove(code)

        ret_code, msg, _ = query_processor(**kargs)

        if ret_code != RET_OK:
            return RET_ERROR, msg

        ret_code, msg, unpush_req_str = SubscriptionQuery.pack_unpush_req(code_list, subtype_list, self.get_async_conn_id())
        if ret_code != RET_OK:
            return RET_ERROR, msg

        ret_code, msg = self._send_async_req(unpush_req_str)
        if ret_code != RET_OK:
            return RET_ERROR, msg

        return RET_OK, None

    def query_subscription(self, is_all_conn=True):
        """
        查询已订阅的实时信息

        :param is_all_conn: 是否返回所有连接的订阅状态,不传或者传False只返回当前连接数据
        :return: (ret, data)

                ret != RET_OK 返回错误字符串

                ret == RET_OK 返回 定阅信息的字典数据 ，格式如下:

                {
                    'total_used': 4,    # 所有连接已使用的定阅额度

                    'own_used': 0,       # 当前连接已使用的定阅额度

                    'remain': 496,       #  剩余的定阅额度

                    'sub_list':          #  每种定阅类型对应的股票列表

                    {
                        'BROKER': ['HK.00700', 'HK.02318'],

                        'RT_DATA': ['HK.00700', 'HK.02318']
                    }
                }
        """
        is_all_conn = bool(is_all_conn)
        query_processor = self._get_sync_query_processor(
            SubscriptionQuery.pack_subscription_query_req,
            SubscriptionQuery.unpack_subscription_query_rsp)
        kargs = {
            "is_all_conn": is_all_conn,
            "conn_id": self.get_sync_conn_id()
        }

        ret_code, msg, sub_table = query_processor(**kargs)
        if ret_code == RET_ERROR:
            return ret_code, msg

        ret_dict = {}
        ret_dict['total_used'] = sub_table['total_used']
        ret_dict['remain'] = sub_table['remain']
        ret_dict['own_used'] = 0
        ret_dict['sub_list'] = {}
        for conn_sub in sub_table['conn_sub_list']:

            is_own_conn = conn_sub['is_own_conn']
            if is_own_conn:
                ret_dict['own_used'] = conn_sub['used']
            if not is_all_conn and not is_own_conn:
                continue

            for sub_info in conn_sub['sub_list']:
                subtype = sub_info['subtype']

                if subtype not in ret_dict['sub_list']:
                    ret_dict['sub_list'][subtype] = []
                code_list = ret_dict['sub_list'][subtype]

                for code in sub_info['code_list']:
                    if code not in code_list:
                        code_list.append(code)

        return RET_OK, ret_dict

    def get_stock_quote(self, code_list):
        """
        获取订阅股票报价的实时数据，有订阅要求限制。

        对于异步推送，参见StockQuoteHandlerBase

        :param code_list: 股票代码列表，必须确保code_list中的股票均订阅成功后才能够执行
        :return: (ret, data)

                ret == RET_OK 返回pd dataframe数据，数据列格式如下

                ret != RET_OK 返回错误字符串

                =====================   ===========   ==============================================================
                参数                      类型                        说明
                =====================   ===========   ==============================================================
                code                    str            股票代码
                data_date               str            日期
                data_time               str            时间
                last_price              float          最新价格
                open_price              float          今日开盘价
                high_price              float          最高价格
                low_price               float          最低价格
                prev_close_price        float          昨收盘价格
                volume                  int            成交数量
                turnover                float          成交金额
                turnover_rate           float          换手率
                amplitude               int            振幅
                suspension              bool           是否停牌(True表示停牌)
                listing_date            str            上市日期 (yyyy-MM-dd)
                price_spread            float          当前价差，亦即摆盘数据的买档或卖档的相邻档位的报价差
                =====================   ===========   ==============================================================

        """
        code_list = unique_and_normalize_list(code_list)
        if not code_list:
            error_str = ERROR_STR_PREFIX + "the type of code_list param is wrong"
            return RET_ERROR, error_str

        query_processor = self._get_sync_query_processor(
            StockQuoteQuery.pack_req,
            StockQuoteQuery.unpack_rsp,
        )
        kargs = {
            "stock_list": code_list,
            "conn_id": self.get_sync_conn_id()
        }

        ret_code, msg, quote_list = query_processor(**kargs)
        if ret_code == RET_ERROR:
            return ret_code, msg

        col_list = [
            'code', 'data_date', 'data_time', 'last_price', 'open_price',
            'high_price', 'low_price', 'prev_close_price', 'volume',
            'turnover', 'turnover_rate', 'amplitude', 'suspension',
            'listing_date', 'price_spread'
        ]

        quote_frame_table = pd.DataFrame(quote_list, columns=col_list)

        return RET_OK, quote_frame_table

    def get_rt_ticker(self, code, num=500):
        """
        获取指定股票的实时逐笔。取最近num个逐笔

        :param code: 股票代码
        :param num: 最近ticker个数(有最大个数限制，最近500个）
        :return: (ret, data)

                ret == RET_OK 返回pd dataframe数据，数据列格式如下

                ret != RET_OK 返回错误字符串

                =====================   ===========   ==============================================================
                参数                      类型                        说明
                =====================   ===========   ==============================================================
                stock_code               str            股票代码
                sequence                 int            逐笔序号
                time                     str            成交时间
                price                    float          成交价格
                volume                   int            成交数量（股数）
                turnover                 float          成交金额
                ticker_direction         str            逐笔方向
                =====================   ===========   ==============================================================
        """

        if code is None or is_str(code) is False:
            error_str = ERROR_STR_PREFIX + "the type of code param is wrong"
            return RET_ERROR, error_str

        if num is None or isinstance(num, int) is False:
            error_str = ERROR_STR_PREFIX + "the type of num param is wrong"
            return RET_ERROR, error_str

        query_processor = self._get_sync_query_processor(
            TickerQuery.pack_req,
            TickerQuery.unpack_rsp,
        )
        kargs = {
            "code": code,
            "num": num,
            "conn_id": self.get_sync_conn_id()
        }
        ret_code, msg, ticker_list = query_processor(**kargs)
        if ret_code == RET_ERROR:
            return ret_code, msg

        col_list = [
            'code', 'time', 'price', 'volume', 'turnover', "ticker_direction",
            'sequence'
        ]
        ticker_frame_table = pd.DataFrame(ticker_list, columns=col_list)

        return RET_OK, ticker_frame_table

    def get_cur_kline(self, code, num, ktype=SubType.K_DAY, autype=AuType.QFQ):
        """
        实时获取指定股票最近num个K线数据，最多1000根

        :param code: 股票代码
        :param num:  k线数据个数
        :param ktype: k线类型，参见KLType
        :param autype: 复权类型，参见AuType
        :return: (ret, data)

                ret == RET_OK 返回pd dataframe数据，数据列格式如下

                ret != RET_OK 返回错误字符串

                =====================   ===========   ==============================================================
                参数                      类型                        说明
                =====================   ===========   ==============================================================
                code                     str            股票代码
                time_key                 str            时间
                open                     float          开盘价
                close                    float          收盘价
                high                     float          最高价
                low                      float          最低价
                volume                   int            成交量
                turnover                 float          成交额
                pe_ratio                 float          市盈率
                turnover_rate            float          换手率
                last_close               float          昨收价
                =====================   ===========   ==============================================================
        """
        param_table = {'code': code, 'ktype': ktype}
        for x in param_table:
            param = param_table[x]
            if param is None or is_str(param) is False:
                error_str = ERROR_STR_PREFIX + "the type of %s param is wrong" % x
                return RET_ERROR, error_str

        if num is None or isinstance(num, int) is False:
            error_str = ERROR_STR_PREFIX + "the type of num param is wrong"
            return RET_ERROR, error_str

        if autype is not None and is_str(autype) is False:
            error_str = ERROR_STR_PREFIX + "the type of autype param is wrong"
            return RET_ERROR, error_str

        query_processor = self._get_sync_query_processor(
            CurKlineQuery.pack_req,
            CurKlineQuery.unpack_rsp,
        )

        kargs = {
            "code": code,
            "num": num,
            "ktype": ktype,
            "autype": autype,
            "conn_id": self.get_sync_conn_id()
        }
        ret_code, msg, kline_list = query_processor(**kargs)
        if ret_code == RET_ERROR:
            return ret_code, msg

        col_list = [
            'code', 'time_key', 'open', 'close', 'high', 'low', 'volume',
            'turnover', 'pe_ratio', 'turnover_rate', 'last_close'
        ]
        kline_frame_table = pd.DataFrame(kline_list, columns=col_list)

        return RET_OK, kline_frame_table

    def get_order_book(self, code):
        """
        获取实时摆盘数据

        :param code: 股票代码
        :return: (ret, data)

                ret == RET_OK 返回字典，数据格式如下

                ret != RET_OK 返回错误字符串

                {‘code’: 股票代码
                ‘Ask’:[ (ask_price1, ask_volume1，order_num), (ask_price2, ask_volume2, order_num),…]
                ‘Bid’: [ (bid_price1, bid_volume1, order_num), (bid_price2, bid_volume2, order_num),…]
                }

                'Ask'：卖盘， 'Bid'买盘。每个元组的含义是(委托价格，委托数量，委托订单数)
        """
        if code is None or is_str(code) is False:
            error_str = ERROR_STR_PREFIX + "the type of code param is wrong"
            return RET_ERROR, error_str

        query_processor = self._get_sync_query_processor(
            OrderBookQuery.pack_req,
            OrderBookQuery.unpack_rsp,
        )

        kargs = {
            "code": code,
            "conn_id": self.get_sync_conn_id()
        }
        ret_code, msg, orderbook = query_processor(**kargs)
        if ret_code == RET_ERROR:
            return ret_code, msg

        return RET_OK, orderbook

    def get_multi_points_history_kline(self,
                                       code_list,
                                       dates,
                                       fields,
                                       ktype=KLType.K_DAY,
                                       autype=AuType.QFQ,
                                       no_data_mode=KLNoDataMode.FORWARD):
        '''
        获取多支股票多个时间点的指定数据列

        :param code_list: 单个或多个股票 'HK.00700'  or  ['HK.00700', 'HK.00001']
        :param dates: 单个或多个日期 '2017-01-01' or ['2017-01-01', '2017-01-02']
        :param fields: 单个或多个数据列 KL_FIELD.ALL or [KL_FIELD.DATE_TIME, KL_FIELD.OPEN]
        :param ktype: K线类型
        :param autype: 复权类型
        :param no_data_mode: 指定时间为非交易日时，对应的k线数据取值模式，参见KLNoDataMode
        :return: (ret, data)

                ret == RET_OK 返回pd dataframe数据，固定表头包括'code'(代码) 'time_point'(指定的日期) 'data_status' (KLDataStatus)。数据列格式如下

                ret != RET_OK 返回错误字符串

            =================   ===========   ==============================================================================
            参数                  类型                        说明
            =================   ===========   ==============================================================================
            code                str            股票代码
            time_point          str            请求的时间
            data_status         str            数据点是否有效，参见KLDataStatus
            time_key            str            k线时间
            open                float          开盘价
            close               float          收盘价
            high                float          最高价
            low                 float          最低价
            pe_ratio            float          市盈率
            turnover_rate       float          换手率
            volume              int            成交量
            turnover            float          成交额
            change_rate         float          涨跌幅
            last_close          float          昨收价
            =================   ===========   ==============================================================================
        '''
        req_codes = unique_and_normalize_list(code_list)
        if not code_list:
            error_str = ERROR_STR_PREFIX + "the type of code param is wrong"
            return RET_ERROR, error_str

        req_dates = unique_and_normalize_list(dates)
        if not dates:
            error_str = ERROR_STR_PREFIX + "the type of dates param is wrong"
            return RET_ERROR, error_str

        req_fields = unique_and_normalize_list(fields)
        if not fields:
            req_fields = copy(KL_FIELD.ALL_REAL)
        req_fields = KL_FIELD.normalize_field_list(req_fields)
        if not req_fields:
            error_str = ERROR_STR_PREFIX + "the type of fields param is wrong"
            return RET_ERROR, error_str

        query_processor = self._get_sync_query_processor(
            MultiPointsHisKLine.pack_req, MultiPointsHisKLine.unpack_rsp)

        # 一次性最多取100支股票的数据
        max_req_code_num = 50

        data_finish = False
        list_ret = []
        # 循环请求数据，避免一次性取太多超时
        while not data_finish:
            logger.debug('get_multi_points_history_kline - wait ... %s' % datetime.now())
            kargs = {
                "code_list": req_codes,
                "dates": req_dates,
                "fields": copy(req_fields),
                "ktype": ktype,
                "autype": autype,
                "max_req": max_req_code_num,
                "no_data_mode": int(no_data_mode),
                "conn_id": self.get_sync_conn_id()
            }
            ret_code, msg, content = query_processor(**kargs)
            if ret_code == RET_ERROR:
                return ret_code, msg

            list_kline, has_next = content
            data_finish = (not has_next)

            for dict_item in list_kline:
                item_code = dict_item['code']
                list_ret.append(dict_item)
                if item_code in req_codes:
                    req_codes.remove(item_code)

            if 0 == len(req_codes):
                data_finish = True

        # 表头列
        col_list = ['code', 'time_point', 'data_status']
        for field in req_fields:
            str_field = KL_FIELD.DICT_KL_FIELD_STR[field]
            if str_field not in col_list:
                col_list.append(str_field)

        pd_frame = pd.DataFrame(list_ret, columns=col_list)

        return RET_OK, pd_frame



