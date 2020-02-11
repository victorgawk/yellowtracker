from pytz import timezone
from datetime import datetime, timedelta
import discord
from discord.ext import commands
import math
from cog.cog import Cog
from util.date import DateUtil

weekly_events = [
{'name':'Vanilla NT','type':'woe','weekday':'6','begin':'15:00','end':'16:00'},
{'name':'Vanilla FE','type':'woe','weekday':'6','begin':'16:15','end':'17:15'},
{'name':'Unres FE','type':'woe','weekday':'6','begin':'17:30','end':'18:30'},
{'name':'Vanilla NT','type':'woe','weekday':'7','begin':'02:45','end':'03:45'},
{'name':'Vanilla SE','type':'woe','weekday':'7','begin':'04:00','end':'05:00'},
{'name':'Unres SE','type':'woe','weekday':'7','begin':'05:15','end':'06:15'},
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

    @commands.command()
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
        await ctx.send(embed=embed)

def get_woe_map(bot, timezone):
    dt_now = DateUtil.get_dt_now(bot.tz_str)
    evts = get_evts_by_type(bot, timezone, 'woe')
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
        if evt['dt_begin'] < next_evt['dt_begin']:
            next_evt = evt
    if next_evt != None:
        woe_map['next'] = format_evt(bot, next_evt, timezone)
    return woe_map

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

def get_evts_by_type(bot, timezone, type):
    result = []
    for evt in weekly_events:
        if evt['type'] != type:
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
        dt_evt_begin = dt_evt_begin.astimezone(timezone)
        evt_end = evt['end'].split(':')
        dt_evt_end = DateUtil.get_dt_now(bot.tz_str).replace(
            hour=int(evt_end[0]),
            minute=int(evt_end[1]),
            second=0,
            microsecond=0
        )
        while dt_evt_end.isoweekday() != int(evt['weekday']):
            dt_evt_end += timedelta(days=1)
        dt_evt_end = dt_evt_end.astimezone(timezone)
        evt['dt_begin'] = dt_evt_begin
        evt['dt_end'] = dt_evt_end
        result.append(evt)
    result.sort(key=lambda x: x['dt_begin'])
    return result

def setup(bot):
    bot.add_cog(Event(bot))