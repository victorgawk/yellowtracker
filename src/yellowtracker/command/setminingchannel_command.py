import discord
from yellowtracker.domain.bot import Bot
from yellowtracker.domain.track_type import TrackType
from yellowtracker.service.channel_service import ChannelService

class SetMiningChannelCommand:

    @staticmethod
    async def setminingchannel(interaction: discord.Interaction, bot: Bot):
        await ChannelService.confirm_set_channel(interaction, bot, TrackType.MINING)
