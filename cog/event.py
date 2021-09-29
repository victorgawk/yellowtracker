from pytz import timezone
from datetime import datetime, timedelta
import discord
from discord.ext import commands
import math
from base.cog import Cog
from util.date import DateUtil
from util.coroutine import CoroutineUtil

weekly_events = [
{'name':'Vanilla NT','type':'woe','weekday':'6','begin':'15:00','end':'16:00'},
{'name':'Vanilla FE','type':'woe','weekday':'6','begin':'16:15','end':'17:15'},
{'name':'Unres FE','type':'woe','weekday':'6','begin':'17:30','end':'18:30'},
{'name':'Vanilla NT','type':'woe','weekday':'7','begin':'02:45','end':'03:45'},
{'name':'Vanilla SE','type':'woe','weekday':'7','begin':'04:00','end':'05:00'},
{'name':'Unres SE','type':'woe','weekday':'7','begin':'05:15','end':'06:15'},
{'name':'BG Happy Hour','type':'bghh','weekday':'2','begin':'04:00','end':'05:00'},
{'name':'BG Happy Hour','type':'bghh','weekday':'2','begin':'10:00','end':'11:00'},
{'name':'BG Happy Hour','type':'bghh','weekday':'2','begin':'16:00','end':'17:00'},
{'name':'BG Happy Hour','type':'bghh','weekday':'4','begin':'04:00','end':'05:00'},
{'name':'BG Happy Hour','type':'bghh','weekday':'4','begin':'10:00','end':'11:00'},
{'name':'BG Happy Hour','type':'bghh','weekday':'4','begin':'16:00','end':'17:00'},
{'name':'BG Happy Hour','type':'bghh','weekday':'5','begin':'04:00','end':'06:00'},
{'name':'BG Happy Hour','type':'bghh','weekday':'6','begin':'04:00','end':'06:00'},
{'name':'BG Happy Hour','type':'bghh','weekday':'6','begin':'10:00','end':'12:00'},
{'name':'BG Happy Hour','type':'bghh','weekday':'6','begin':'18:30','end':'20:30'},
{'name':'BG Happy Hour','type':'bghh','weekday':'7','begin':'06:15','end':'08:15'},
{'name':'BG Happy Hour','type':'bghh','weekday':'7','begin':'10:00','end':'12:00'},
{'name':'BG Happy Hour','type':'bghh','weekday':'7','begin':'15:00','end':'17:00'},
{'name':'GMC','type':'gmc','weekday':'1','begin':'02:00','end':'04:00'},
{'name':'GMC','type':'gmc','weekday':'1','begin':'12:00','end':'14:00'},
{'name':'GMC','type':'gmc','weekday':'1','begin':'16:00','end':'18:00'},
{'name':'GMC','type':'gmc','weekday':'2','begin':'04:00','end':'06:00'},
{'name':'GMC','type':'gmc','weekday':'2','begin':'14:00','end':'16:00'},
{'name':'GMC','type':'gmc','weekday':'2','begin':'18:00','end':'20:00'},
{'name':'GMC','type':'gmc','weekday':'3','begin':'06:00','end':'08:00'},
{'name':'GMC','type':'gmc','weekday':'3','begin':'14:00','end':'16:00'},
{'name':'GMC','type':'gmc','weekday':'3','begin':'20:00','end':'22:00'},
{'name':'GMC','type':'gmc','weekday':'4','begin':'08:00','end':'10:00'},
{'name':'GMC','type':'gmc','weekday':'4','begin':'18:00','end':'20:00'},
{'name':'GMC','type':'gmc','weekday':'5','begin':'00:00','end':'02:00'},
{'name':'GMC','type':'gmc','weekday':'5','begin':'11:00','end':'13:00'},
{'name':'GMC','type':'gmc','weekday':'5','begin':'15:00','end':'17:00'},
{'name':'GMC','type':'gmc','weekday':'5','begin':'20:00','end':'22:00'},
{'name':'GMC','type':'gmc','weekday':'6','begin':'02:00','end':'04:00'},
{'name':'GMC','type':'gmc','weekday':'6','begin':'12:00','end':'14:00'},
{'name':'GMC','type':'gmc','weekday':'6','begin':'18:00','end':'20:00'},
{'name':'GMC','type':'gmc','weekday':'7','begin':'00:00','end':'02:00'},
{'name':'GMC','type':'gmc','weekday':'7','begin':'11:00','end':'13:00'},
{'name':'GMC','type':'gmc','weekday':'7','begin':'15:00','end':'17:00'}
]

class Event(Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.wait_load_stuff()
        conn = await self.bot.pool.acquire()
        try:
            global_parameter = await conn.fetchrow('SELECT * FROM global_parameter WHERE id=$1', 1)
            race_time = global_parameter['race_time']
            if race_time is not None:
                self.bot.race_time = race_time.astimezone(timezone(self.bot.tz_str))
        finally:
            await self.bot.pool.release(conn)

    @commands.command(help='Show TalonRO War of Emperium times')
    @commands.bot_has_permissions(send_messages=True)
    async def woe(self, ctx):
        woe_map = get_woe_map(self.bot, timezone(self.bot.tz_str))
        embed = discord.Embed()
        embed.title = ':european_castle: WoE'
        embed.colour = discord.Colour.gold()
        if woe_map['ongoing'] != '':
            embed.add_field(name='Ongoing :boom:', value=woe_map['ongoing'], inline=False)
        embed.add_field(name='Next :arrow_right:', value=woe_map['next'], inline=False)
        embed.add_field(name='Saturday', value=woe_map['saturday'], inline=False)
        embed.add_field(name='Sunday', value=woe_map['sunday'], inline=False)
        footer = 'Server Time (' + self.bot.tz_str + '): '
        footer += DateUtil.fmt_dt(DateUtil.get_dt_now(self.bot.tz_str))
        embed.set_footer(text=footer)
        await CoroutineUtil.run(ctx.send(embed=embed))

    @commands.command(help='Show TalonRO GM Challenge times')
    @commands.bot_has_permissions(send_messages=True)
    async def gmc(self, ctx):
        gmc_map = get_gmc_map(self.bot, timezone(self.bot.tz_str))
        embed = discord.Embed()
        embed.title = ':dragon_face: GMC'
        embed.colour = discord.Colour.gold()
        if gmc_map['ongoing'] != '':
            embed.add_field(name='Ongoing :boom:', value=gmc_map['ongoing'], inline=False)
        embed.add_field(name='Next :arrow_right:', value=gmc_map['next'], inline=False)
        if gmc_map['today'] != '':
            embed.add_field(name='Today', value=gmc_map['today'], inline=False)
        if gmc_map['tomorrow'] != '':
            embed.add_field(name='Tomorrow', value=gmc_map['tomorrow'], inline=False)
        footer = 'Server Time (' + self.bot.tz_str + '): ' 
        footer += DateUtil.fmt_dt(DateUtil.get_dt_now(self.bot.tz_str))
        embed.set_footer(text=footer)
        await CoroutineUtil.run(ctx.send(embed=embed))

    @commands.command(help='Show TalonRO BG Happy Hour times')
    @commands.bot_has_permissions(send_messages=True)
    async def bghh(self, ctx):
        bghh_map = get_bghh_map(self.bot, timezone(self.bot.tz_str))
        embed = discord.Embed()
        embed.title = ':crossed_swords: BG Happy Hour'
        embed.colour = discord.Colour.gold()
        if bghh_map['ongoing'] != '':
            embed.add_field(name='Ongoing :boom:', value=bghh_map['ongoing'], inline=False)
        embed.add_field(name='Next :arrow_right:', value=bghh_map['next'], inline=False)
        if bghh_map['today'] != '':
            embed.add_field(name='Today', value=bghh_map['today'], inline=False)
        if bghh_map['tomorrow'] != '':
            embed.add_field(name='Tomorrow', value=bghh_map['tomorrow'], inline=False)
        footer = 'Server Time (' + self.bot.tz_str + '): '
        footer += DateUtil.fmt_dt(DateUtil.get_dt_now(self.bot.tz_str))
        embed.set_footer(text=footer)
        await CoroutineUtil.run(ctx.send(embed=embed))

    @commands.command(help='Set the next Summer Race time')
    @commands.bot_has_permissions(send_messages=True)
    async def setrace(self, ctx, time_str):
        mins_ago = 0
        if len(time_str) != 5 or time_str[2] != ':':
            return
        hrs_mins = time_str.split(':')
        if len(hrs_mins) != 2 or not hrs_mins[0].isnumeric() or not hrs_mins[1].isnumeric():
            return
        hh = int(hrs_mins[0])
        mm = int(hrs_mins[1])
        time = datetime.now() + timedelta(hours=hh, minutes=mm)
        await update_race_time(self.bot, time)
        await CoroutineUtil.run(ctx.send('Summer Race set to begin in {0} hours and {1} minutes.'.format(hh, mm)))

    async def timer(self):
        if self.bot.ws is not None:
            dt_now = DateUtil.get_dt_now(self.bot.tz_str)
            if self.bot.race_time is not None:
                race_begin = self.bot.race_time
                race_end = self.bot.race_time + timedelta(hours=1)
                if dt_now > race_end:
                    await update_race_time(self.bot, None)
                else:
                    str = 'Summer Race'
                    if race_begin <= dt_now <= race_end:
                        str += ' ends '
                        str += DateUtil.fmt_time_short((race_end - dt_now) / timedelta(milliseconds=1))
                    else:
                        str += ' '
                        str += DateUtil.fmt_time_short((race_begin - dt_now) / timedelta(milliseconds=1))
                    str += ' (TalonRO)'
                    game = discord.Game(name=str)
                    await CoroutineUtil.run(self.bot.change_presence(activity=game))
                    return
            evt = get_next_evt(self.bot, timezone(self.bot.tz_str))
            str = ('WoE ' if evt['type'] == 'woe' else '') + evt['name']
            if evt['dt_begin'] <= dt_now <= evt['dt_end']:
                str += ' ends '
                str += DateUtil.fmt_time_short((evt['dt_end'] - dt_now) / timedelta(milliseconds=1))
            else:
                str += ' '
                str += DateUtil.fmt_time_short((evt['dt_begin'] - dt_now) / timedelta(milliseconds=1))
            str += ' (TalonRO)'
            game = discord.Game(name=str)
            await CoroutineUtil.run(self.bot.change_presence(activity=game))

async def update_race_time(bot, race_time):
    conn = await bot.pool.acquire()
    try:
        sql = 'UPDATE global_parameter SET race_time=$1 WHERE id=$2'
        await conn.execute(sql, race_time, 1)
    finally:
        await bot.pool.release(conn)
    bot.race_time = None
    if race_time is not None:
        bot.race_time = race_time.astimezone(timezone(bot.tz_str))

def get_gmc_map(bot, timezone):
    dt_now = DateUtil.get_dt_now(bot.tz_str)
    weekday_today = dt_now.isoweekday()
    weekday_tomorrow = 1 if weekday_today == 7 else (weekday_today + 1)
    evts = get_evts(bot, timezone, type='gmc')
    gmc_map = {}
    gmc_map['ongoing'] = ''
    gmc_map['next'] = ''
    gmc_map['today'] = ''
    gmc_map['tomorrow'] = ''
    next_evt = evts[0]
    for evt in evts:
        str_gmc = '' + format_evt(bot, evt, timezone) + '\n'
        if int(evt['weekday']) == weekday_today:
            gmc_map['today'] += str_gmc
        elif int(evt['weekday']) == weekday_tomorrow:
            gmc_map['tomorrow'] += str_gmc
        if evt['dt_begin'] <= dt_now <= evt['dt_end']:
            gmc_map['ongoing'] = format_evt(bot, evt, timezone)
        if evt['dt_begin'] <= dt_now:
            continue
        if next_evt['dt_begin'] < dt_now or evt['dt_begin'] < next_evt['dt_begin']:
            next_evt = evt
    if next_evt != None:
        gmc_map['next'] = format_evt(bot, next_evt, timezone)
    return gmc_map

def get_woe_map(bot, timezone):
    dt_now = DateUtil.get_dt_now(bot.tz_str)
    evts = get_evts(bot, timezone, type='woe')
    woe_map = {}
    woe_map['ongoing'] = ''
    woe_map['next'] = ''
    woe_map['saturday'] = ''
    woe_map['sunday'] = ''
    next_evt = evts[0]
    for evt in evts:
        str_woe = '' + format_evt(bot, evt, timezone) + '\n'
        if int(evt['weekday']) == 7:
            woe_map['sunday'] += str_woe
        else:
            woe_map['saturday'] += str_woe
        if evt['dt_begin'] <= dt_now <= evt['dt_end']:
            woe_map['ongoing'] = format_evt(bot, evt, timezone)
        if evt['dt_begin'] <= dt_now:
            continue
        if next_evt['dt_begin'] < dt_now or evt['dt_begin'] < next_evt['dt_begin']:
            next_evt = evt
    if next_evt != None:
        woe_map['next'] = format_evt(bot, next_evt, timezone)
    return woe_map

def get_bghh_map(bot, timezone):
    dt_now = DateUtil.get_dt_now(bot.tz_str)
    weekday_today = dt_now.isoweekday()
    weekday_tomorrow = 1 if weekday_today == 7 else (weekday_today + 1)
    evts = get_evts(bot, timezone, type='bghh')
    bghh_map = {}
    bghh_map['ongoing'] = ''
    bghh_map['next'] = ''
    bghh_map['today'] = ''
    bghh_map['tomorrow'] = ''
    next_evt = evts[0]
    for evt in evts:
        str_bghh = '' + format_evt(bot, evt, timezone) + '\n'
        if int(evt['weekday']) == weekday_today:
            bghh_map['today'] += str_bghh
        elif int(evt['weekday']) == weekday_tomorrow:
            bghh_map['tomorrow'] += str_bghh
        if evt['dt_begin'] <= dt_now <= evt['dt_end']:
            bghh_map['ongoing'] = format_evt(bot, evt, timezone)
        if evt['dt_begin'] <= dt_now:
            continue
        if next_evt['dt_begin'] < dt_now or evt['dt_begin'] < next_evt['dt_begin']:
            next_evt = evt
    if next_evt != None:
        bghh_map['next'] = format_evt(bot, next_evt, timezone)
    return bghh_map

def get_next_evt(bot, timezone):
    dt_now = DateUtil.get_dt_now(bot.tz_str)
    evts = get_evts(bot, timezone)
    next_evt = None
    for evt in evts:
        if evt['dt_end'] < dt_now:
            continue
        if next_evt is None:
            next_evt = evt
        if evt['dt_begin'] <= dt_now <= evt['dt_end']: #ongoing
            return next_evt
            break
        if evt['dt_begin'] < next_evt['dt_begin']: #next
            next_evt = evt
    return next_evt

def format_evt(bot, evt, timezone):
    dt_now = DateUtil.get_dt_now(bot.tz_str)
    result = '**'
    result += evt['name']
    result += '** '
    result += evt['dt_begin'].strftime('%H:%M')
    if evt['dt_begin'] <= dt_now <= evt['dt_end']:
        result += ' (ends '
        result += DateUtil.fmt_time((evt['dt_end'] - dt_now) / timedelta(milliseconds=1))
    else:
        result += ' ('
        result += DateUtil.fmt_time((evt['dt_begin'] - dt_now) / timedelta(milliseconds=1))
    result += ')'
    return result

def get_evts(bot, timezone, type=None):
    result = []
    for evt in weekly_events:
        if type is not None and evt['type'] != type:
            continue
        evt_begin = evt['begin'].split(':')
        dt_evt_begin = DateUtil.get_dt_now(bot.tz_str).replace(
            hour=int(evt_begin[0]),
            minute=int(evt_begin[1]),
            second=0,
            microsecond=0
        )
        while dt_evt_begin.isoweekday() != int(evt['weekday']):
            dt_evt_begin += timedelta(days=1)
        dt_evt_begin = dt_evt_begin.replace(tzinfo=None)
        dt_evt_begin = timezone.localize(dt_evt_begin, is_dst=False)
        evt_end = evt['end'].split(':')
        dt_evt_end = DateUtil.get_dt_now(bot.tz_str).replace(
            hour=int(evt_end[0]),
            minute=int(evt_end[1]),
            second=0,
            microsecond=0
        )
        while dt_evt_end.isoweekday() != int(evt['weekday']):
            dt_evt_end += timedelta(days=1)
        dt_evt_end = dt_evt_end.replace(tzinfo=None)
        dt_evt_end = timezone.localize(dt_evt_end, is_dst=False)
        evt['dt_begin'] = dt_evt_begin
        evt['dt_end'] = dt_evt_end
        result.append(evt)
    result.sort(key=lambda x: x['dt_begin'])
    return result

def setup(bot):
    bot.add_cog(Event(bot))