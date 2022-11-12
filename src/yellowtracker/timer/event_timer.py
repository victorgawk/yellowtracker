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

    evt_types = ['hh', 'woe', 'gmc']
    idx = 0

    @staticmethod
    async def timer(bot: Bot):
        if not bot.tracker_ready:
            return
        if bot.ws is not None:
            dt_now = DateUtil.get_dt_now(bot.TIMEZONE)
            evt, ongoing = EventService.get_next_evt(bot, EventTimer.evt_types[EventTimer.idx])
            if evt is None:
                return
            str = EventTimer.get_msg_prefix(evt)
            if ongoing:
                str += ' ends '
                str += DateUtil.fmt_time_short((evt['dt_end'] - dt_now) / timedelta(milliseconds=1))
            else:
                str += ' '
                str += DateUtil.fmt_time_short((evt['dt_begin'] - dt_now) / timedelta(milliseconds=1))
            game = discord.Game(name=str)
            await CoroutineUtil.run(bot.change_presence(activity=game))
            EventTimer.idx = (EventTimer.idx + 1) % len(EventTimer.evt_types)

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
