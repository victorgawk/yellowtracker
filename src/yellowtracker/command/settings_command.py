import discord
from yellowtracker.domain.bot import Bot
from yellowtracker.domain.emoji import Emoji
from yellowtracker.domain.track_type import TrackType
from yellowtracker.service.channel_service import ChannelService
from yellowtracker.util.coroutine_util import CoroutineUtil

class SettingsCommand:

    @staticmethod
    async def settings(interaction: discord.Interaction, bot: Bot):
        guild = interaction.guild
        if guild is None:
            await interaction.response.defer()
            return
        guild_state = bot.guild_state_map[guild.id]
        mvp_channel = None
        mining_channel = None
        for channel_id in guild_state['channel_state_map']:
            if guild_state['channel_state_map'][channel_id]['type'] == TrackType.MVP:
                mvp_channel = ChannelService.get_channel_from_guild(guild, channel_id)
            else:
                mining_channel = ChannelService.get_channel_from_guild(guild, channel_id)
        msg = f"Custom MVP Times: {Emoji.YES.value if guild_state['custom'] else Emoji.NO.value}\n"
        msg += f"Mobile Layout: {Emoji.YES.value if guild_state['mobile'] else Emoji.NO.value}\n"
        msg += f"MVP Channel: {'' if mvp_channel is None else mvp_channel.mention}\n"
        msg += f"Mining Channel: {'' if mining_channel is None else mining_channel.mention}"
        await CoroutineUtil.run(interaction.response.send_message(msg))
