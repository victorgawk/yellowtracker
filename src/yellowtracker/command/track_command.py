import discord
from yellowtracker.domain.bot import Bot
from yellowtracker.util.coroutine_util import CoroutineUtil
from yellowtracker.service.channel_service import ChannelService

class TrackCommand:

    @staticmethod
    async def track(interaction: discord.Interaction, bot: Bot, mvp: str, user_time: str):
        validate_msg = ChannelService.validate_channel(bot, interaction.channel)
        if validate_msg is not None:
            await CoroutineUtil.run(interaction.response.send_message(validate_msg))
            return
        guild_state = bot.guild_state_map[interaction.guild_id]
        channel_state = guild_state['channel_state_map'].get(interaction.channel_id)
        if channel_state is None:
            await CoroutineUtil.run(interaction.response.send_message('This command can only be used in a track channel.'))
            return
        await CoroutineUtil.run(interaction.response.defer(thinking = False))
        await ChannelService.track_entry(bot, channel_state, interaction.channel, interaction.user, mvp, user_time)
