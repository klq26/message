# -*- coding: utf-8 -*-

import time
from datetime import datetime

class datetimeManager:

    def __init__(self):
        super().__init__()

    def getTimeStamp(self):
        return time.time()

    def getTimeStampFromString(self, dateString):
        """
        从时间字符串中解析出 datetime 对象
        """
        timeFormat = '%Y/%m/%d %H:%M:%S'
        return datetime.strptime(dateString, timeFormat).timestamp()

    def getDateString(self, sep=''):
        """
        获取日期字符串，分隔符自定义。例如： 2020/01/01 或 2020-01-01
        """
        today = time.strftime('%Y' + sep + '%m' + sep + '%d', time.localtime())
        return today

    def getDateTimeString(self):
        """
        获取时间字符串。例如： 2020/01/01 10:30:00
        """
        ts = self.getTimeStamp()
        timeFormat = '%Y/%m/%d %H:%M:%S'
        timeString = time.strftime(timeFormat, time.localtime(ts))
        return timeString
    
    def getDuration(self, start_ts, end_ts):
        """
        获取两个 ts 之间的时间间隔（秒）
        """
        duration = round(end_ts - start_ts, 4)
        return duration
