#coding:utf-8
import os
import sys
import urllib2
import urllib,urllib2

def log2(message):
    print(message)
def wechat_send(pre_log_str,title,message):
    pre_log_str+=sys._getframe().f_code.co_name+':'
    log2(pre_log_str+'[start]')

    '''
     select count(*),status from activity_teacher_yearbook group by status ;

    '''
    url='http://192.168.199.1:8000/mainsugar/loginGET/'
    url='https://pushbear.ftqq.com/sub'
    textmod ={'user':'admin','password':'admin'}
    textmod={
      "sendkey": "1945-9555a8df744033c5baeeeba062fc1791",
      "text": "%s"%(title),
      "desp": "%s"%(message)
    }
    textmod = urllib.urlencode(textmod)
    log2(pre_log_str+' '+textmod)
    #输出内容:password=admin&user=admin
    req = urllib2.Request(url = '%s%s%s' % (url,'?',textmod))
    res = urllib2.urlopen(req)
    res = res.read()
    log2(pre_log_str+' '+res)
    #输出内容:登录成功
    log2(pre_log_str+'[  end]')

if __name__=="__main__":
    sys.argv[1]
    sys.argv[2]
    wechat_send("main",sys.argv[1],sys.argv[2])
    #wechat_send("main","message_test")
