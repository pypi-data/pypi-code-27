# -*- coding: utf8 -*-
import httplib
import threading
import time

HOST = "apollo-configservice-apollo.apps.intra.yongqianbao.com"  # 主机地址 例如192.168.1.101
PORT = 80  # 端口

HOST = '10.130.11.238'
PORT = 8080

URI = "/notifications/v2?cluster=cluster_bj&notifications=%5B%7B%22notificationId%22%3A2%2C+%22namespaceName%22%3A+%22application%22%7D%5D&appId=1001"  # 相对地址,加参数防止缓存，否则可能会返回304

TOTAL = 0  # 总数
SUCCESS = 0  # 响应成功数
FAIL = 0  # 响应失败数
EXCEPT = 0  # 响应异常数


def probe_cost():
    start = time.time()
    conn = httplib.HTTPConnection(HOST, PORT, False, timeout=90)
    conn.request('GET', '/configfiles/json/1001/cluster_bj/application?ip=192.168.1.220"')
    res = conn.getresponse()
    if res.status == 200 or res.status == 304:
        return time.time() - start

    print("error")


class RequestThread(threading.Thread):

    # 构造函数
    def __init__(self, thread_name):
        threading.Thread.__init__(self, name=thread_name)

    def run(self):
        global TOTAL
        global SUCCESS
        global FAIL
        global EXCEPT

        TOTAL += 1
        try:
            conn = httplib.HTTPConnection(HOST, PORT, False, timeout=90)
            conn.request('GET', URI)
            res = conn.getresponse()

            if res.status == 200 or res.status == 304:
                SUCCESS += 1
            else:
                print "FAIL: ", res.status, res.read()
                FAIL += 1
            conn.close()
        except Exception as e:
            print "EXCEPT: ", e
            EXCEPT += 1


print '===========task start==========='

max = 5000

i = 0
while True:
    if i >= max:
        break

    rate = 0.0 if TOTAL == 0 else FAIL * 1.0 / TOTAL
    if rate > 0.2:
        print "STATISTIC: %d, rate: %f, total: %d,success: %d,fail: %d,except: %d" % (i, rate, TOTAL, SUCCESS, FAIL, EXCEPT)
        break

    try:
        RequestThread("thread" + str(i)).start()
        time.sleep(0.002)
    except Exception as e:
        print("THREAD START FAILED: ", e.message)
        pass
    i += 1

    if i % 500 == 0:
        print "STATISTIC: %d, rate: %f, total: %d,success: %d,fail: %d,except: %d" % (i, rate, TOTAL, SUCCESS, FAIL, EXCEPT)

print("total:", i)

t = 1
while (SUCCESS + FAIL + EXCEPT) < i:
    rate = 0.0 if TOTAL == 0 else FAIL * 1.0 / TOTAL
    print "STATISTIC: %d, rate: %f, total: %d,success: %d,fail: %d,except: %d" % (t, rate, TOTAL, SUCCESS, FAIL, EXCEPT)
    print "cost: {}".format(probe_cost())
    t += 1
    time.sleep(1)

print "STATISTIC: %d, rate: %f, total: %d,success: %d,fail: %d,except: %d" % (t, rate, TOTAL, SUCCESS, FAIL, EXCEPT)
