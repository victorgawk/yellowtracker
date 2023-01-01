import time
from pytz import timezone
from datetime import timedelta
from yellowtracker.domain.bot import Bot
from yellowtracker.domain.weekly_event import WeeklyEvent
from yellowtracker.util.date_util import DateUtil

class EventService:

    @staticmethod
    def get_gmc_map(bot: Bot) -> dict:
        dt_now = DateUtil.get_dt_now(bot.TIMEZONE)
        weekday_today = dt_now.isoweekday()
        weekday_tomorrow = 1 if weekday_today == 7 else (weekday_today + 1)
        evts = EventService.get_evts(bot, type='gmc')
        gmc_map = {}
        gmc_map['ongoing'] = ''
        gmc_map['next'] = ''
        gmc_map['today'] = ''
        gmc_map['tomorrow'] = ''
        next_evt = evts[0]
        for evt in evts:
            str_gmc = '' + EventService.format_evt(bot, evt) + '\n'
            if int(evt['weekday']) == weekday_today:
                gmc_map['today'] += str_gmc
            elif int(evt['weekday']) == weekday_tomorrow:
                gmc_map['tomorrow'] += str_gmc
            if evt['dt_begin'] <= dt_now <= evt['dt_end']:
                gmc_map['ongoing'] = EventService.format_evt(bot, evt)
            if evt['dt_begin'] <= dt_now:
                continue
            if next_evt['dt_begin'] < dt_now or evt['dt_begin'] < next_evt['dt_begin']:
                next_evt = evt
        if next_evt != None:
            gmc_map['next'] = EventService.format_evt(bot, next_evt)
        return gmc_map

    @staticmethod
    def get_woe_map(bot: Bot) -> dict:
        dt_now = DateUtil.get_dt_now(bot.TIMEZONE)
        evts = EventService.get_evts(bot, type='woe')
        woe_map = {}
        woe_map['ongoing'] = ''
        woe_map['next'] = ''
        woe_map['saturday'] = ''
        woe_map['sunday'] = ''
        next_evt = evts[0]
        for evt in evts:
            str_woe = '' + EventService.format_evt(bot, evt) + '\n'
            if int(evt['weekday']) == 7:
                woe_map['sunday'] += str_woe
            else:
                woe_map['saturday'] += str_woe
            if evt['dt_begin'] <= dt_now <= evt['dt_end']:
                woe_map['ongoing'] = EventService.format_evt(bot, evt)
            if evt['dt_begin'] <= dt_now:
                continue
            if next_evt['dt_begin'] < dt_now or evt['dt_begin'] < next_evt['dt_begin']:
                next_evt = evt
        if next_evt != None:
            woe_map['next'] = EventService.format_evt(bot, next_evt)
        return woe_map

    @staticmethod
    def get_hh_map(bot: Bot) -> dict:
        dt_now = DateUtil.get_dt_now(bot.TIMEZONE)
        weekday_today = dt_now.isoweekday()
        weekday_tomorrow = 1 if weekday_today == 7 else (weekday_today + 1)
        evts = EventService.get_evts(bot, type='hh')
        hh_map = {}
        hh_map['ongoing'] = ''
        hh_map['next'] = ''
        hh_map['today'] = ''
        hh_map['tomorrow'] = ''
        next_evt = evts[0]
        for evt in evts:
            str_hh = '' + EventService.format_evt(bot, evt) + '\n'
            if int(evt['weekday']) == weekday_today:
                hh_map['today'] += str_hh
            elif int(evt['weekday']) == weekday_tomorrow:
                hh_map['tomorrow'] += str_hh
            if evt['dt_begin'] <= dt_now <= evt['dt_end']:
                hh_map['ongoing'] = EventService.format_evt(bot, evt)
            if evt['dt_begin'] <= dt_now:
                continue
            if next_evt['dt_begin'] < dt_now or evt['dt_begin'] < next_evt['dt_begin']:
                next_evt = evt
        if next_evt != None:
            hh_map['next'] = EventService.format_evt(bot, next_evt)
        return hh_map

    @staticmethod
    def get_next_evt(bot: Bot, type: str = None) -> tuple[dict, bool]:
        dt_now = DateUtil.get_dt_now(bot.TIMEZONE)
        evts = EventService.get_evts(bot, type)
        next_evt = None
        ongoing = False
        for evt in evts:
            if evt['dt_end'] < dt_now:
                continue
            if next_evt is None:
                next_evt = evt
            if evt['dt_begin'] <= dt_now <= evt['dt_end']: #ongoing
                ongoing = True
                break
            if evt['dt_begin'] < next_evt['dt_begin']: #next
                next_evt = evt
        return next_evt, ongoing

    @staticmethod
    def is_ongoing(bot: Bot, evt: dict):
        dt_now = DateUtil.get_dt_now(bot.TIMEZONE)
        return evt['dt_begin'] <= dt_now <= evt['dt_end']

    @staticmethod
    def format_evt(bot: Bot, evt: dict) -> str:
        local_tz = DateUtil.get_local_tzinfo()
        dt_now = DateUtil.get_dt_now(bot.TIMEZONE)
        result = '**'
        result += evt['name']
        result += '** '
        result += f"<t:{int(time.mktime(evt['dt_begin'].astimezone(tz=local_tz).timetuple()))}:f>"
        if evt['dt_begin'] <= dt_now <= evt['dt_end']:
            result += ' (ends '
            result += f"<t:{int(time.mktime(evt['dt_end'].astimezone(tz=local_tz).timetuple()))}:R>"
        else:
            result += ' ('
            result += f"<t:{int(time.mktime(evt['dt_begin'].astimezone(tz=local_tz).timetuple()))}:R>"
        result += ')'
        return result

    @staticmethod
    def get_evts(bot: Bot, type: str = None) -> list[dict]:
        tzinfo = timezone(bot.TIMEZONE)
        result = []
        for evt in WeeklyEvent.DATA:
            if type is not None and evt['type'] != type:
                continue
            evt_begin = evt['begin'].split(':')
            dt_evt_begin = DateUtil.get_dt_now(bot.TIMEZONE).replace(
                hour=int(evt_begin[0]),
                minute=int(evt_begin[1]),
                second=0,
                microsecond=0
            )
            while dt_evt_begin.isoweekday() != int(evt['weekday']):
                dt_evt_begin += timedelta(days=1)
            dt_evt_begin = dt_evt_begin.replace(tzinfo=None)
            dt_evt_begin = tzinfo.localize(dt_evt_begin, is_dst=False)
            evt_end = evt['end'].split(':')
            dt_evt_end = DateUtil.get_dt_now(bot.TIMEZONE).replace(
                hour=int(evt_end[0]),
                minute=int(evt_end[1]),
                second=0,
                microsecond=0
            )
            while dt_evt_end.isoweekday() != int(evt['weekday']):
                dt_evt_end += timedelta(days=1)
            dt_evt_end = dt_evt_end.replace(tzinfo=None)
            dt_evt_end = tzinfo.localize(dt_evt_end, is_dst=False)
            if dt_evt_end < dt_evt_begin:
                dt_evt_end += timedelta(days=1)
            evtcp = EventService.copy_evt(evt)
            evtcp['dt_begin'] = dt_evt_begin
            evtcp['dt_end'] = dt_evt_end
            result.append(evtcp)
        result.sort(key=lambda x: x['dt_begin'])
        return result

    @staticmethod
    def copy_evt(evt: dict[str, str]) -> dict:
        copy = {}
        copy['name'] = evt['name']
        copy['type'] = evt['type']
        copy['weekday'] = evt['weekday']
        copy['begin'] = evt['begin']
        copy['end'] = evt['end']
        copy['dt_begin'] = None
        copy['dt_end'] = None
        return copy
