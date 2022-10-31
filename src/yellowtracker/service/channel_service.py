import discord
import collections
from datetime import datetime, timedelta
from yellowtracker.domain.bot import Bot
from yellowtracker.domain.track_type import TrackType
from yellowtracker.util.date_util import DateUtil
from yellowtracker.util.coroutine_util import CoroutineUtil
from yellowtracker.util.track_util import TrackUtil

class ChannelService:

    @staticmethod
    def get_guild_from_bot(bot: Bot, id_guild: int) -> discord.Guild | None:
        return next((x for x in bot.guilds if x.id == id_guild), None)

    @staticmethod
    def get_channel_from_guild(guild: discord.Guild, id_channel: int) -> discord.TextChannel | None:
        return next((x for x in guild.text_channels if x.id == id_channel), None)

    @staticmethod
    def get_channel_from_bot(bot: Bot, id_guild: int, id_channel: int) -> discord.TextChannel | None:
        guild = ChannelService.get_guild_from_bot(bot, id_guild)
        if guild is None:
            return None
        return ChannelService.get_channel_from_guild(guild, id_channel)

    @staticmethod
    async def init_channel(bot: Bot, channel_state: dict):
        channel = ChannelService.get_channel_from_bot(bot, channel_state['id_guild'], channel_state['id_channel'])
        if channel is None:
            return
        if ChannelService.validate_channel(bot, channel) is not None:
            return
        channel_state['id_message'] = None
        msgs = [message async for message in channel.history(oldest_first=True)]
        if msgs is None:
            return
        msgs_to_delete = []
        for msg in msgs:
            if msg.type == discord.MessageType.default and msg.author == bot.user and channel_state['id_message'] is None:
                channel_state['id_message'] = msg.id
                await ChannelService.update_channel_message(bot, channel_state)
                continue
            msgs_to_delete.append(msg)
        await CoroutineUtil.run(channel.delete_messages(msgs_to_delete))

    @staticmethod
    async def set_channel(bot, channel, type: TrackType):
        guild_state = bot.guild_state_map[channel.guild.id]
        channel_state_map = guild_state['channel_state_map']
        channel_state = next(
            (
                channel_state_map[x]
                for x in channel_state_map
                if channel_state_map[x]['type'] == type
            ),
            None
        )
        entry_state_list = []
        if channel_state is not None:
            entry_state_list = channel_state['entry_state_list']
            del channel_state_map[channel_state['id_channel']]
        channel_state = {
            'id_channel': channel.id,
            'id_guild': channel.guild.id,
            'type': type,
            'id_message': None,
            'entry_state_list': entry_state_list,
            'entry_log_list': collections.deque()
        }
        channel_state_map[channel.id] = channel_state
        await ChannelService.init_channel(bot, channel_state)
        conn = await bot.pool_acquire()
        try:
            sql  = 'UPDATE guild '
            sql += 'SET id_' + type.sql_desc + '_channel=$1 '
            sql += 'WHERE id=$2'
            await conn.execute(sql, channel.id, channel.guild.id)
        finally:
            await bot.pool_release(conn)

    @staticmethod
    async def unset_channel(interaction: discord.Interaction, bot: Bot, trackType: TrackType):
        validate_msg = ChannelService.validate_channel(bot, interaction.channel)
        if validate_msg is not None:
            await interaction.response.send_message(validate_msg)
            return
        guild_state = bot.guild_state_map[interaction.guild_id]
        channel_state_map = guild_state['channel_state_map']
        channel_state = next(
            (
                channel_state_map[x]
                for x in channel_state_map
                if channel_state_map[x]['type'] == trackType
            ),
            None
        )
        if channel_state is None:
            await interaction.response.send_message('There is no ' + trackType.desc + ' channel set.')
            return
        del channel_state_map[channel_state['id_channel']]
        conn = await bot.pool_acquire()
        try:
            sql  = 'UPDATE guild '
            sql += 'SET id_' + trackType.sql_desc + '_channel=NULL '
            sql += 'WHERE id=$1'
            await conn.execute(sql, interaction.guild_id)
        finally:
            await bot.pool_release(conn)
        await interaction.response.send_message(trackType.desc + ' channel unset.')

    @staticmethod
    async def update_channel_message(bot: Bot, channel_state: dict):
        mobile = bot.guild_state_map[channel_state['id_guild']]['mobile']
        type = channel_state['type']
        embed = discord.Embed()
        embed.colour = discord.Colour.gold()
        embed.title = (':crown: ' if type == TrackType.MVP else ':pick: ') + type.desc + 'S'
        names = []
        maps = []
        remaining_times = []
        id_mob_first_entry = None
        cmp = 'r2' if type == TrackType.MVP else 'r1'
        for entry_state in channel_state['entry_state_list']:
            if entry_state[cmp] > -bot.TABLE_ENTRY_EXPIRATION_MINS:
                remaining_time = TrackUtil.fmt_r1_r2(int(entry_state['r1']))
                if type == TrackType.MVP:
                    if id_mob_first_entry is None:
                        id_mob_first_entry = entry_state['entry']['id_mob']
                    remaining_time += ' to ' + TrackUtil.fmt_r1_r2(int(entry_state['r2']))
                remaining_time += ' mins'
                if mobile:
                    name = entry_state['entry']['name']
                    if type == TrackType.MVP:
                        name += ' (' + entry_state['entry']['map'] + ')'
                    name += ' | ' + remaining_time
                    names.append(name)
                else:
                    names.append(entry_state['entry']['name'])
                    if type == TrackType.MVP:
                        maps.append(entry_state['entry']['map'])
                    remaining_times.append(remaining_time)
        if len(names) == 0:
            embed.add_field(name=':x:', value='No ' + type.desc + ' has been tracked.', inline=False)
        else:
            max_length = 20
            if len(names) > max_length + 1:
                diff = len(names) - max_length
                for i in range(0, diff):
                    names.pop()
                    if type == TrackType.MVP:
                        maps.pop()
                    remaining_times.pop()
                names.append('and ' + str(diff) + ' more...')
            if type == TrackType.MVP:
                embed.set_thumbnail(url="https://file5s.ratemyserver.net/mobs/" + str(id_mob_first_entry) + ".gif")
            if mobile:
                embed.add_field(name='Name', value=TrackUtil.fmt_column(names), inline=False)
            else:
                embed.add_field(name='Name', value=TrackUtil.fmt_column(names), inline=True)
                if type == TrackType.MVP:
                    embed.add_field(name='Map', value=TrackUtil.fmt_column(maps), inline=True)
                embed.add_field(name='Remaining Time', value=TrackUtil.fmt_column(remaining_times), inline=True)
        if len(channel_state['entry_log_list']) > 0:
            result = ''
            for entry_log in channel_state['entry_log_list']:
                if result != '':
                    result += '\n'
                milliseconds = (entry_log['entry_time'] - datetime.now()) / timedelta(milliseconds=1)
                result += '**[' + DateUtil.fmt_time_short(milliseconds) + ']**'
                result += ' ' + entry_log['entry']['name']
                if type == TrackType.MVP:
                    result += ' (' + entry_log['entry']['map'] + ')'
                result += ' by <@' + str(entry_log['id_user']) + '>'
            embed.add_field(name='Track Log', value=result, inline=False)
        guild = ChannelService.get_guild_from_bot(bot, channel_state['id_guild'])
        if guild is None:
            return
        channel = ChannelService.get_channel_from_bot(bot, channel_state['id_guild'], channel_state['id_channel'])
        if channel is None:
            return
        if ChannelService.validate_channel(bot, channel) is not None:
            return
        message = None
        if channel_state['id_message'] is not None:
            message = await CoroutineUtil.run_with_retries(channel.fetch_message(channel_state['id_message']))
        if message is None:
            message = await CoroutineUtil.run(channel.send(embed=embed))
            if message is not None:
                channel_state['id_message'] = message.id
        else:
            await CoroutineUtil.run(message.edit(embed=embed, content=''))
            await CoroutineUtil.run(message.clear_reactions())

    @staticmethod
    def validate_channel(bot: Bot, channel) -> str | None:
        if channel is None:
            return 'Invalid channel.'
        member = next((x for x in channel.members if x == bot.user), None)
        if member is None:
            return 'Bot need to be a member of this channel.'
        permissions = channel.permissions_for(member)
        missing_permissions = []
        if not permissions.read_messages:
            missing_permissions.append('Read Messages')
        if not permissions.send_messages:
            missing_permissions.append('Send Messages')
        if not permissions.manage_messages:
            missing_permissions.append('Manage Messages')
        if not permissions.read_message_history:
            missing_permissions.append('Read Message History')
        if not permissions.add_reactions:
            missing_permissions.append('Add Reactions')
        if len(missing_permissions) > 0:
            msg = 'Bot is missing the following permissions:\n\n'
            for idx in range(len(missing_permissions)):
                msg += str(idx+1) + '. ' + missing_permissions[idx] + '\n'
            return msg
        return None

    @staticmethod
    async def confirm_set_channel(interaction: discord.Interaction, bot: Bot, trackType: TrackType):
        validate_msg = ChannelService.validate_channel(bot, interaction.channel)
        if validate_msg is not None:
            await interaction.response.send_message(validate_msg)
            return
        await interaction.response.send_message(
            "This will remove all messages from this channel. Are you sure?",
            view=SetChannelView(bot = bot, trackType = trackType)
        )

class SetChannelView(discord.ui.View):
    def __init__(self, *, timeout = 180, bot, trackType):
        super().__init__(timeout=timeout)
        self.add_item(SetChannelYesButton(bot = bot, trackType = trackType))
        self.add_item(SetChannelNoButton())

class SetChannelYesButton(discord.ui.Button):
    def __init__(self, bot, trackType):
        self.bot = bot
        self.trackType = trackType
        super().__init__(style=discord.ButtonStyle.primary, label='Yes')
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.edit_message(view=None)
        await ChannelService.set_channel(self.bot, interaction.channel, self.trackType)

class SetChannelNoButton(discord.ui.Button):
    def __init__(self):
        super().__init__(style=discord.ButtonStyle.secondary, label='No')
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.edit_message(view=None)
