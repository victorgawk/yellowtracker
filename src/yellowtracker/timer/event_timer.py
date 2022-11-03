import asyncio
import logging
import discord
from datetime import timedelta
from yellowtracker.domain.bot import Bot
from yellowtracker.domain.emoji import Emoji
from yellowtracker.service.event_service import EventService
from yellowtracker.util.coroutine_util import CoroutineUtil
from yellowtracker.util.date_util import DateUtil

log = logging.getLogger(__name__)

class EventTimer:

    @staticmethod
    async def timer(bot: Bot):
        log.info("Starting event timer.")
        while True:
            if bot.ws is not None:
                dt_now = DateUtil.get_dt_now(bot.TIMEZONE)
                ongoing, not_ongoing = EventService.get_next_evts(bot)
                if len(ongoing) > 0:
                    for evt in ongoing:
                        str = EventTimer.get_msg_prefix(evt)
                        str += ' ends '
                        str += DateUtil.fmt_time_short((evt['dt_end'] - dt_now) / timedelta(milliseconds=1))
                        game = discord.Game(name=str)
                        await CoroutineUtil.run(bot.change_presence(activity=game))
                        await asyncio.sleep(bot.EVENT_TIMER_DELAY_SECS)
                else:
                    for evt in not_ongoing:
                        str = EventTimer.get_msg_prefix(evt)
                        str += ' '
                        str += DateUtil.fmt_time_short((evt['dt_begin'] - dt_now) / timedelta(milliseconds=1))
                        game = discord.Game(name=str)
                        await CoroutineUtil.run(bot.change_presence(activity=game))
                        await asyncio.sleep(bot.EVENT_TIMER_DELAY_SECS)
            else:
                await asyncio.sleep(bot.EVENT_TIMER_DELAY_SECS)

    @staticmethod
    def get_msg_prefix(evt: dict) -> str:
        str = ''
        if evt['type'] == 'hh':
            str += Emoji.HH.value
        elif evt['type'] == 'woe':
            str += Emoji.WOE.value
        elif evt['type'] == 'gmc':
            str += Emoji.GMC.value
        str += evt['name']
        return str
