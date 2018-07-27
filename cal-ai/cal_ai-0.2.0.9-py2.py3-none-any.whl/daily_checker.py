#!/usr/bin/python
# -*- coding: utf-8 -*-
from threading import Thread
from .common_utils import CommonUtils
from .cal_crawler import CalCrawler
from .ai_monitor import AIMonitor
from .healthy_checker import CheckStatus


THREAD_TIMEOUT = 300


class DailyChecker(object):
    @staticmethod
    def __healthy_check(host_name, start_time, end_time, check_date, check_result, pool_name="risktxncomputeserv"):
        check_result[check_date] = AIMonitor.monitor_live_box(host_name, start_time, end_time, pool_name)[0]
        print("Check %s on %s result: %s" % (host_name, check_date, check_result[check_date]))

    @staticmethod
    def check_for_host_current_month(host_name, callback_result):
        thread_list = []
        check_result = {}
        check_date_dict = CommonUtils.get_current_month_each_day_start_end_time()
        for check_date, time_tuple in check_date_dict.items():
            thread = Thread(target=DailyChecker.__healthy_check, args=[host_name, time_tuple[0], time_tuple[1],
                                                                       check_date, check_result])
            thread.daemon = True
            thread.start()
            thread_list.append(thread)
        for thread in thread_list:
            thread.join(THREAD_TIMEOUT)

        status_dict = {check_status: 0 for check_status in CheckStatus}
        for check_date, healthy_status in check_result.items():
            status_dict[healthy_status] += 1
        callback_result[host_name] = status_dict
        return callback_result

    @staticmethod
    def pool_check(pool_name="risktxncomputeserv"):
        thread_list = []
        check_result = {}
        for host_name in CalCrawler.get_all_traffic_host(pool_name):
            thread = Thread(target=DailyChecker.check_for_host_current_month, args=[host_name, check_result])
            thread.daemon = True
            thread.start()
            thread_list.append(thread)
        for thread in thread_list:
            thread.join(THREAD_TIMEOUT)
        return check_result

    @staticmethod
    def get_top_10_bad_box(pool_name="risktxncomputeserv"):
        check_result = DailyChecker.pool_check(pool_name)
        check_result_list = [(host_name, status_dict) for host_name, status_dict in check_result.items()]
        sorted_result = sorted(check_result_list, cmp=lambda x, y: cmp(x[1][CheckStatus.RED], y[1][CheckStatus.RED]),
                               reverse=True)
        return sorted_result[:10]


if __name__ == '__main__':
    # print(DailyChecker.pool_check())
    print(DailyChecker.check_for_host_current_month("ccg01risktxncomputeserv4184", {}))


