import discord
from pytz import timezone
from datetime import timedelta
from yellowtracker.domain.bot import Bot
from yellowtracker.service.event_service import EventService
from yellowtracker.util.coroutine_util import CoroutineUtil
from yellowtracker.util.date_util import DateUtil

class EventTimer:

    @staticmethod
    async def timer(bot: Bot):
        if bot.ws is not None:
            dt_now = DateUtil.get_dt_now(bot.TIMEZONE)
            # if bot.race_time is not None:
            #     race_begin = bot.race_time
            #     race_end = bot.race_time + timedelta(hours=1)
            #     if dt_now > race_end:
            #         await update_race_time(bot, None)
            #     else:
            #         str = 'Summer Race'
            #         if race_begin <= dt_now <= race_end:
            #             str += ' ends '
            #             str += DateUtil.fmt_time_short((race_end - dt_now) / timedelta(milliseconds=1))
            #         else:
            #             str += ' '
            #             str += DateUtil.fmt_time_short((race_begin - dt_now) / timedelta(milliseconds=1))
            #         game = discord.Game(name=str)
            #         await CoroutineUtil.run(self.bot.change_presence(activity=game))
            #         return
            evt = EventService.get_next_evt(bot)
            if evt is None:
                return
            str = ('WoE ' if evt['type'] == 'woe' else '') + evt['name']
            if evt['dt_begin'] <= dt_now <= evt['dt_end']:
                str += ' ends '
                str += DateUtil.fmt_time_short((evt['dt_end'] - dt_now) / timedelta(milliseconds=1))
            else:
                str += ' '
                str += DateUtil.fmt_time_short((evt['dt_begin'] - dt_now) / timedelta(milliseconds=1))
            game = discord.Game(name=str)
            await CoroutineUtil.run(bot.change_presence(activity=game))
