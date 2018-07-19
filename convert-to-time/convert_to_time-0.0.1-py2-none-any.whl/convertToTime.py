#!/usr/bin/env python
# -*- coding: utf-8 -*-

import calendar
import datetime


dayCollection = {
    "current_day": ["hôm nay", "hôm ni"],
    "next_day": ["ngày mai", "hôm sau", "ngày hôm sau"],
    "previous_day": ["hôm qua"]
}

monthCollection = {
    "current_month": ["thánh này", "tháng ni"],
    "next_month": ["tháng sau", "tháng tới"],
    "previous_month": ["tháng trước"]
}

class ConvertToTime():
    def __init__(self):
        pass

    def generateCurrentTime(self):
        now = datetime.datetime.now()
        year = now.year
        month = now.month
        day = now.day
        return year, month, day

    # function trả về số ngày trong tháng đúng với cả năm nhuận
    # ví dụ Tháng 2 năm 2001 sẽ trả về  28 
    # Tháng 2 năm 2004 sẽ trả về 29 
    def getNumberDayInMonth(sefl, year, month):
        numDayInMonth = calendar.monthrange(year, month)[1]
        return numDayInMonth

    def convertToDay(sefl, startDate):
        year, month, day = self.generateCurrentTime()
        count = 0
        for key, value in dayCollection.iteritems():
            if startDate in value:
                if key == "next_day":
                    count += 1
                elif key == "current_day":
                    count += 0
                elif key == "previous_day":
                    count -= 1
                break
        day += count
        numDayInMonth = self.getNumberDayInMonth(year, month)
        if day > numDayInMonth:
            day = day - numDayInMonth
            month += 1
        
        desireDay = datetime.datetime(year, month, day)
        return desireDay

    def convertToMonth(self, startDate):
        year, month, day = self.generateCurrentTime()
        count = 0
        for key, value in monthCollection.iteritems():
            if startDate in value:
                if key == "next_month":
                    count += 1
                elif key == "current_month":
                    count += 0
                elif key == "previous_month":
                    count -= 1
                break
        month += count
        if month > 12:
            month = month - 12
            year += 1
        desireDay = datetime.datetime(year, month, day)
        return desireDay