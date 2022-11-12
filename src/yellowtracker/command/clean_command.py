from datetime import datetime, timedelta
import discord
from yellowtracker.domain.bot import Bot
from yellowtracker.domain.track_type import TrackType
from yellowtracker.util.coroutine_util import CoroutineUtil
from yellowtracker.service.channel_service import ChannelService

class CleanCommand:

    @staticmethod
    async def clean(interaction: discord.Interaction, bot: Bot):
        validate_msg = ChannelService.validate_channel(bot, interaction.channel)
        if validate_msg is not None:
            await CoroutineUtil.run(interaction.response.send_message(validate_msg))
            return
        guild_state = bot.guild_state_map[interaction.guild_id]
        channel_state = guild_state['channel_state_map'].get(interaction.channel_id)
        if channel_state is None:
            await CoroutineUtil.run(interaction.response.send_message('This command can only be used in a track channel.'))
            return

        await CoroutineUtil.run(interaction.response.send_message(
            "This will clean the list. Are you sure?",
            view=CleanView(bot = bot, trackType = channel_state['type'])
        ))

class CleanView(discord.ui.View):
    def __init__(self, *, timeout = 180, bot, trackType):
        super().__init__(timeout=timeout)
        self.add_item(CleanYesButton(bot = bot, trackType = trackType))
        self.add_item(CleanNoButton())

class CleanYesButton(discord.ui.Button):
    def __init__(self, bot: Bot, trackType: TrackType):
        self.bot = bot
        self.trackType = trackType
        super().__init__(style=discord.ButtonStyle.primary, label='Yes')
    async def callback(self, interaction: discord.Interaction):
        bot = self.bot
        guild_state = bot.guild_state_map.get(interaction.guild_id)
        if guild_state is None:
            await CoroutineUtil.run(interaction.response.defer())
            return
        channel_state = guild_state['channel_state_map'].get(interaction.channel_id)
        for entry_state in channel_state['entry_state_list']:
            mins_ago = entry_state['t2' if self.trackType == TrackType.MVP else 't1']
            mins_ago += bot.TABLE_ENTRY_EXPIRATION_MINS
            entry_state['r1'] = -mins_ago
            if self.trackType == TrackType.MVP:
                entry_state['r2'] = -mins_ago
        await ChannelService.update_channel_message(bot, channel_state)
        await CoroutineUtil.run(interaction.response.edit_message(content='Track list cleared.', view=None))

class CleanNoButton(discord.ui.Button):
    def __init__(self):
        super().__init__(style=discord.ButtonStyle.secondary, label='No')
    async def callback(self, interaction: discord.Interaction):
        await CoroutineUtil.run(interaction.response.edit_message(view=None))
