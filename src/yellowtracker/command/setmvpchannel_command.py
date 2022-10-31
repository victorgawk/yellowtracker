import discord
from yellowtracker.domain.bot import Bot
from yellowtracker.domain.track_type import TrackType
from yellowtracker.service.channel_service import ChannelService

class SetMvpChannelCommand:

    @staticmethod
    async def setmvpchannel(interaction: discord.Interaction, bot: Bot):
        await ChannelService.confirm_set_channel(interaction, bot, TrackType.MVP)
