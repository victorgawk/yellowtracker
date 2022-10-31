from datetime import datetime, timedelta
from yellowtracker.domain.bot import Bot
from yellowtracker.util.coroutine_util import CoroutineUtil
from yellowtracker.service.channel_service import ChannelService
from yellowtracker.util.track_util import TrackUtil

class TrackTimer:

    @staticmethod
    async def timer(bot: Bot):
        for guild in bot.guilds:
            guild_state = bot.guild_state_map.get(guild.id)
            if guild_state is None:
                continue
            for id_channel in guild_state['channel_state_map'].copy():
                channel_state = guild_state['channel_state_map'].get(id_channel)
                if channel_state is None:
                    continue
                for entry_state in channel_state['entry_state_list']:
                    TrackUtil.calc_remaining_time(entry_state, entry_state['track_time'], channel_state['type'])
                await ChannelService.update_channel_message(bot, channel_state)
                channel = ChannelService.get_channel_from_guild(guild, channel_state['id_channel'])
                if channel is None:
                    return
                if ChannelService.validate_channel(bot, channel) is not None:
                    continue
                msgs = [message async for message in channel.history(limit=100)]
                if msgs is None:
                    continue
                for msg in msgs:
                    if msg.id == channel_state['id_message']:
                        continue
                    msg_date = msg.created_at if msg.edited_at is None else msg.edited_at
                    if datetime.utcnow() - msg_date.replace(tzinfo=None) > timedelta(seconds=bot.DEL_MSG_AFTER_SECS):
                        await CoroutineUtil.run(msg.delete())
