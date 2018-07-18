import time
from datetime import date, timedelta
import datetime
import calendar

# logger = setup_custom_logger()

def get_timestamp():
    return int(time.time())

def get_current_time_str():
    temp = time.localtime(time.time())
    szTime = time.strftime("%Y-%m-%d %H:%M:%S", temp)
    return szTime

def timestamp2str(tt):
    t1 = time.localtime(float(tt))
    t2 = time.strftime("%Y-%m-%d %H:%M:%S", t1)
    return t2

def hour():
    temp = time.localtime(time.time())
    szTime = time.strftime("%H", temp)
    return int(szTime)

def today():
    today = date.today()
    return today.strftime('%Y-%m-%d')

def yesterday():
    yesterday = date.today() + timedelta(-1)
    return yesterday.strftime('%Y-%m-%d')

def diff_day(nDiff):
    day = date.today() + timedelta(nDiff)
    return day.strftime('%Y-%m-%d')

def addmonths(date,months = 0):
    targetmonth=months+date.month
    try:
        if 0 == targetmonth%12:
            return date.replace(year=date.year+int(targetmonth/12) - 1,month=12)
        else:
            return date.replace(year=date.year + int(targetmonth / 12), month=(targetmonth % 12))
    except Exception,e:
        # There is an exception if the day of the month we're in does not exist in the target month
        # Go to the FIRST of the month AFTER, then go back one day.
        print e
        date.replace(year=date.year+int((targetmonth+1)/12),month=((targetmonth+1)%12),day=1)
        date+=datetime.timedelta(days=-1)
        return date

def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)  # this will never fail
    return next_month - datetime.timedelta(days=next_month.day)

def first_day_of_month(nDiffMon = 0):
    today = date.today()
    date1 = addmonths(today.replace(day=1), nDiffMon)
    return date1.replace(day=1)

def last_day_of_month(nDiffMon = 0):
    def end_day(any_day):
        next_month = any_day.replace(day=28) + datetime.timedelta(days=4)  # this will never fail
        return next_month - datetime.timedelta(days=next_month.day)

    return end_day(first_day_of_month(nDiffMon))