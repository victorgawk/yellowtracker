import discord
from yellowtracker.domain.bot import Bot
from yellowtracker.domain.track_type import TrackType
from yellowtracker.service.channel_service import ChannelService

class UnsetMvpChannelCommand:

    @staticmethod
    async def unsetmvpchannel(interaction: discord.Interaction, bot: Bot):
        await ChannelService.unset_channel(interaction, bot, TrackType.MVP)
