from datetime import datetime
from pytz import timezone
import math

class DateUtil(object):
    @staticmethod
    def fmt_time(milliseconds):
        minutes = math.floor(math.floor(math.fabs(milliseconds) / 1000) / 60)
        hours = math.floor(minutes / 60)
        days = math.floor(hours / 24)
        minutes = minutes % 60
        hours = hours % 24
        if minutes == 0 and hours == 0 and days == 0:
            return 'now'
        result = ''
        if days > 0:
            result += str(days) + (' day ' if days == 1 else ' days ')
        if hours > 0:
            result += str(hours) + (' hour ' if hours == 1 else ' hours ')
        if days == 0 and minutes > 0:
            result += str(minutes) + (' minute ' if minutes == 1 else ' minutes ')
        if milliseconds < 0:
            result += 'ago'
        elif milliseconds > 0:
            result = 'in ' + result
        return result.strip()

    @staticmethod
    def fmt_time_short(milliseconds):
        minutes = math.floor(math.floor(math.fabs(milliseconds) / 1000) / 60)
        hours = math.floor(minutes / 60)
        days = math.floor(hours / 24)
        minutes = minutes % 60
        hours = hours % 24
        if minutes == 0 and hours == 0 and days == 0:
            return 'now'
        result = ''
        if days > 0:
            result += str(days) + 'd '
        if hours > 0:
            result += str(hours) + 'h '
        if days == 0 and minutes > 0:
            result += str(minutes) + 'm '
        if milliseconds < 0:
            result += 'ago'
        elif milliseconds > 0:
            result = 'in ' + result
        return result.strip()

    @staticmethod
    def fmt_dt(dt):
        return dt.strftime('%A %H:%M')
        #return dt.strftime('%Y-%m-%d %H:%M:%S %Z%z')

    @staticmethod
    def get_dt_now(tz_str):
        dt_now = datetime.now()
        #dt_now = datetime(2020, 2, 16, 1, 0, 1)
        return dt_now.astimezone(timezone(tz_str))