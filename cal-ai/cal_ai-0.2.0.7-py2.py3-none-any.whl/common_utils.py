#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import logging
import pytz
from datetime import datetime, date


class CommonUtils(object):
    @staticmethod
    def get_current_pst_timestamp():
        utc_date = datetime.now(tz=pytz.utc)
        pst_date = utc_date.astimezone(pytz.timezone('US/Pacific'))
        return int(time.mktime(pst_date.timetuple()))

    @staticmethod
    def date_str_to_timestamp(date_str, format="%Y-%m-%d %H:%M:%S"):
        return int(time.mktime(datetime.strptime(date_str, format).timetuple()))

    @staticmethod
    def timestamp_to_data_str(ts, format="%Y-%m-%d %H:%M:%S"):
        current_date = datetime.fromtimestamp(ts)
        return current_date.strftime(format)

    @staticmethod
    def get_column_name_from_host_name(host_name):
        dcg_list = ["dcg01", "dcg02", "dcg11", "dcg12", "dcg13"]
        for dcg in dcg_list:
            if host_name.startswith(dcg):
                return dcg
        if host_name.startswith("slc"):
            if host_name.endswith("a"):
                return "slca"
            elif host_name.endswith("b"):
                return "slcb"
        logging.warn("host %s can not be identified, class it into phx" % host_name)
        return "phx"

    @staticmethod
    def get_current_month_each_day_start_end_time():
        start_end_time_dict = {}
        today = datetime.today()
        last_timestamp = int(time.time())
        for day in range(today.day, 0, -1):
            xth_day = date(today.year, today.month, day)
            xth_day_start = int(time.mktime(xth_day.timetuple()))
            start_end_time_dict[xth_day] = (xth_day_start, last_timestamp)
            last_timestamp = xth_day_start - 1
        return start_end_time_dict

    @staticmethod
    def remove_serial_duplicate(duplicate_list):
        if len(duplicate_list) <= 1:
            return duplicate_list
        else:
            uniq_list = [duplicate_list[0]]
            for i in range(1, len(duplicate_list)):
                if duplicate_list[i][0] != uniq_list[-1][0]:
                    uniq_list.append(duplicate_list[i])
        return uniq_list


if __name__ == '__main__':
    print("Current time: %s" % CommonUtils.timestamp_to_data_str(int(time.time())))
    print("Current PST time: %s" % CommonUtils.timestamp_to_data_str(CommonUtils.get_current_pst_timestamp()))
    __host_name = "dcg13risktxncomputeserv6056"
    print("Pool name for %s is %s" % (__host_name, CommonUtils.get_column_name_from_host_name(__host_name)))


