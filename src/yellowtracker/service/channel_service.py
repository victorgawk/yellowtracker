import logging
import time
import discord
import collections
from datetime import datetime, timedelta
from yellowtracker.domain.bot import Bot
from yellowtracker.domain.track_type import TrackType
from yellowtracker.util.date_util import DateUtil
from yellowtracker.util.coroutine_util import CoroutineUtil
from yellowtracker.util.track_util import TrackUtil
from yellowtracker.service.entry_service import EntryService

log = logging.getLogger(__name__)

class ChannelService:

    @staticmethod
    def get_guild_from_bot(bot: Bot, id_guild: int) -> discord.Guild:
        return next((x for x in bot.guilds if x.id == id_guild), None)

    @staticmethod
    def get_channel_from_guild(guild: discord.Guild, id_channel: int) -> discord.TextChannel:
        return next((x for x in guild.text_channels if x.id == id_channel), None)

    @staticmethod
    def get_channel_from_bot(bot: Bot, id_guild: int, id_channel: int) -> discord.TextChannel:
        guild = ChannelService.get_guild_from_bot(bot, id_guild)
        if guild is None:
            return None
        return ChannelService.get_channel_from_guild(guild, id_channel)

    @staticmethod
    async def track_entry(bot: Bot, channel_state: dict, channel: discord.TextChannel, user: discord.User, mvp: str, user_time: str):
        mins_ago = 0
        if user_time is not None:
            if user_time.isnumeric():
                mins_ago = int(user_time)
            elif len(user_time) == 5 and user_time[2] == ':':
                hrs_mins = user_time.split(':')
                if len(hrs_mins) == 2 and hrs_mins[0].isnumeric() and hrs_mins[1].isnumeric():
                    hh = int(hrs_mins[0])
                    mm = int(hrs_mins[1])
                    track_time = DateUtil.get_dt_now(bot.TIMEZONE)
                    if hh > track_time.hour or (hh == track_time.hour and mm > track_time.minute):
                        track_time -= timedelta(days=1)
                    track_time = track_time.replace(hour=hh, minute=mm)
                    td = DateUtil.get_dt_now(bot.TIMEZONE) - track_time
                    mins_ago = int(td / timedelta(minutes=1))
        if mins_ago < 0:
            mins_ago = 0

        type = channel_state['type']
        results = EntryService.find_entry(bot, mvp, type)

        if len(results) == 0:
            await CoroutineUtil.run(channel.send(
                type.desc + ' "' + mvp + '" not found.'
            ))
        elif len(results) == 1:
            bot_reply_msg = await ChannelService.update_track_time(bot, channel_state, results[0], mins_ago, user_time, user.id)
            await CoroutineUtil.run(channel.send(
                bot_reply_msg
            ))
        else:
            bot_reply_msg = 'More than one ' + type.desc
            bot_reply_msg += ' starting with "' + mvp + '" has been found.\n'
            bot_reply_msg += '\n'
            bot_reply_msg += 'Select the ' + type.desc
            bot_reply_msg += ' that you want to track'
            if user_time is not None:
                bot_reply_msg += ' with time ' + user_time
            bot_reply_msg += ':'
            await CoroutineUtil.run(channel.send(
                bot_reply_msg,
                view=TrackView(bot = bot, opts = results, mins_ago = mins_ago, user_time = user_time, track_type = type)
            ))

    @staticmethod
    async def update_track_time(bot: Bot, channel_state: dict, entry, mins_ago: int, user_time: str, id_user: int):
        conn = await bot.pool_acquire()
        type = channel_state['type']
        date = datetime.now()
        track_time = date - timedelta(minutes=mins_ago)
        try:
            read_sql = f"SELECT * FROM {type.sql_desc}_guild WHERE id_{type.sql_desc}=$1 AND id_guild=$2"
            entry_guild_db = await conn.fetch(read_sql, entry['id'], channel_state['id_guild'])
            write_sql = f"INSERT INTO {type.sql_desc}_guild(id_{type.sql_desc},id_guild,track_time)VALUES($1,$2,$3)"
            if len(entry_guild_db) > 0:
                write_sql = f"UPDATE {type.sql_desc}_guild SET track_time=$3 WHERE id_{type.sql_desc}=$1 AND id_guild=$2"
            await conn.execute(write_sql, entry['id'], channel_state['id_guild'], track_time)

            read_sql = f"SELECT * FROM {type.sql_desc}_guild_log WHERE id_{type.sql_desc}=$1 AND id_guild=$2"
            entry_guild_log_db = await conn.fetch(read_sql, entry['id'], channel_state['id_guild'])
            write_sql = f"INSERT INTO {type.sql_desc}_guild_log(id_{type.sql_desc},id_guild,date,id_user)VALUES($1,$2,$3,$4)"
            if len(entry_guild_log_db) > 0:
                write_sql = f"UPDATE {type.sql_desc}_guild_log SET date=$3,id_user=$4 WHERE id_{type.sql_desc}=$1 AND id_guild=$2"
            await conn.execute(write_sql, entry['id'], channel_state['id_guild'], date, id_user)

            entry_log = None
            for x in channel_state['entry_log_list']:
                if x['entry'] == entry:
                    entry_log = x
                    break
            if entry_log is not None:
                channel_state['entry_log_list'].remove(entry_log)
            channel_state['entry_log_list'].appendleft({
                'entry': entry,
                'date': date,
                'id_user': id_user
            })
            while len(channel_state['entry_log_list']) > 3:
                entry_log_to_remove = channel_state['entry_log_list'].pop()
                del_sql = f"DELETE FROM {type.sql_desc}_guild_log WHERE id_{type.sql_desc}=$1 AND id_guild=$2"
                await conn.execute(del_sql, entry_log_to_remove['entry']['id'], channel_state['id_guild'])
        finally:
            await bot.pool_release(conn)
        entry_state = await TrackUtil.track_entry(bot, channel_state, entry, track_time)
        await ChannelService.update_channel_message(bot, channel_state)
        msg = entry_state['entry']['name']
        if type == TrackType.MVP:
            msg += ' (' 
            msg += entry_state['entry']['map']
            msg += ')'
        msg += ' in '
        msg += TrackUtil.fmt_r1_r2(int(entry_state['r1']))
        if type == TrackType.MVP:
            msg += ' to '
            msg += TrackUtil.fmt_r1_r2(int(entry_state['r2']))
        msg += ' minutes'
        if user_time is not None:
            msg += ' (time: ' + user_time + ')'
        msg += '.'
        return msg

    @staticmethod
    async def init_channel(bot: Bot, channel_state: dict):
        channel = ChannelService.get_channel_from_bot(bot, channel_state['id_guild'], channel_state['id_channel'])
        if channel is None:
            return
        if ChannelService.validate_channel(bot, channel) is not None:
            return
        channel_state['id_message'] = None
        async for msg in channel.history():
            if msg.type == discord.MessageType.default and msg.author == bot.user and channel_state['id_message'] is None:
                channel_state['id_message'] = msg.id
                await ChannelService.update_channel_message(bot, channel_state)
                break
        await ChannelService.delete_msgs(bot, channel_state, channel)

    @staticmethod
    async def delete_msgs(bot, channel_state, channel):
        msgs_to_delete = []
        async for msg in channel.history():
            if ChannelService.is_msg_can_be_deleted(bot, channel_state, msg):
                msgs_to_delete.append(msg)
        if len(msgs_to_delete) > 0:
            await CoroutineUtil.run(channel.delete_messages(msgs_to_delete))

    @staticmethod
    def is_msg_can_be_deleted(bot, channel_state, msg):
        if channel_state['id_message'] is not None and channel_state['id_message'] == msg.id:
            return False
        if datetime.utcnow() - msg.created_at.replace(tzinfo=None) >= timedelta(days=14):
            return False
        msg_date = msg.created_at if msg.edited_at is None else msg.edited_at
        if datetime.utcnow() - msg_date.replace(tzinfo=None) <= timedelta(seconds=bot.DEL_MSG_AFTER_SECS):
            return False
        return True

    @staticmethod
    async def get_channel_history(channel: discord.TextChannel):
        return [message async for message in channel.history()]

    @staticmethod
    async def set_channel(bot: Bot, channel, type: TrackType):
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
        await ChannelService.update_channel_message(bot, channel_state)
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
            await CoroutineUtil.run(interaction.response.send_message(validate_msg))
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
            await CoroutineUtil.run(interaction.response.send_message('There is no ' + trackType.desc + ' channel set.'))
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
        await CoroutineUtil.run(interaction.response.send_message(trackType.desc + ' channel unset.'))

    @staticmethod
    async def update_channel_message(bot: Bot, channel_state: dict):
        local_tz = DateUtil.get_local_tzinfo()
        mobile = bot.guild_state_map[channel_state['id_guild']]['mobile']
        track_type = channel_state['type']
        embed = discord.Embed()
        embed.colour = discord.Colour.gold()
        embed.title = (':crown: ' if track_type == TrackType.MVP else ':pick: ') + track_type.desc + 'S'
        names = []
        maps = []
        remaining_times = []
        id_mob_first_entry = None
        cmp = 'r2' if track_type == TrackType.MVP else 'r1'

        active_entry_states = []
        inactive_entry_state_ids = []
        for entry_state in channel_state['entry_state_list']:
            if entry_state[cmp] > -bot.TABLE_ENTRY_EXPIRATION_MINS:
                remaining_time = TrackUtil.fmt_r1_r2(int(entry_state['r1']))
                if track_type == TrackType.MVP:
                    if id_mob_first_entry is None:
                        id_mob_first_entry = entry_state['entry']['id_mob']
                    remaining_time += ' to ' + TrackUtil.fmt_r1_r2(int(entry_state['r2']))
                remaining_time += ' mins'
                if mobile:
                    name = entry_state['entry']['name']
                    if track_type == TrackType.MVP:
                        name += ' (' + entry_state['entry']['map'] + ')'
                    name += ' | ' + remaining_time
                    names.append(name)
                else:
                    names.append(entry_state['entry']['name'])
                    if track_type == TrackType.MVP:
                        maps.append(entry_state['entry']['map'])
                    remaining_times.append(remaining_time)
                active_entry_states.append(entry_state)
            else:
                inactive_entry_state_ids.append((entry_state['entry']['id'], channel_state['id_guild']))

        channel_state['entry_state_list'] = active_entry_states

        conn = await bot.pool_acquire()
        try:
            del_entry_state_sql = f"DELETE FROM {track_type.sql_desc}_guild WHERE id_{track_type.sql_desc}=$1 AND id_guild=$2"
            await conn.executemany(del_entry_state_sql, inactive_entry_state_ids)
        finally:
            await bot.pool_release(conn)

        if len(names) == 0:
            embed.add_field(name=':x:', value=f"{track_type.desc} list is empty", inline=False)
        else:
            max_length = 20
            if len(names) > max_length + 1:
                diff = len(names) - max_length
                for i in range(0, diff):
                    names.pop()
                    if track_type == TrackType.MVP:
                        maps.pop()
                    remaining_times.pop()
                names.append('and ' + str(diff) + ' more...')
            if track_type == TrackType.MVP:
                embed.set_thumbnail(url="https://file5s.ratemyserver.net/mobs/" + str(id_mob_first_entry) + ".gif")
            if mobile:
                embed.add_field(name='Name', value=TrackUtil.fmt_column(names), inline=False)
            else:
                embed.add_field(name='Name', value=TrackUtil.fmt_column(names), inline=True)
                if track_type == TrackType.MVP:
                    embed.add_field(name='Map', value=TrackUtil.fmt_column(maps), inline=True)
                embed.add_field(name='Remaining Time', value=TrackUtil.fmt_column(remaining_times), inline=True)
        if len(channel_state['entry_log_list']) > 0:
            result = ''
            for entry_log in channel_state['entry_log_list']:
                if result != '':
                    result += '\n'
                result += f"[<t:{int(time.mktime(entry_log['date'].astimezone(tz=local_tz).timetuple()))}:R>]"
                result += ' ' + entry_log['entry']['name']
                if track_type == TrackType.MVP:
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
            try:
                message = await channel.fetch_message(channel_state['id_message'])
            except discord.errors.NotFound:
                pass
            except:
                log.error(f"Unexpected error.\n{CoroutineUtil.get_stack_str()}", exc_info=True)
                return
        if message is None:
            message = await CoroutineUtil.run(channel.send(embed=embed, view=ChannelMessageView(bot=bot, channel_state=channel_state)))
            if message is not None:
                channel_state['id_message'] = message.id
        else:
            await CoroutineUtil.run(message.edit(embed=embed, view=ChannelMessageView(bot=bot, channel_state=channel_state), content=''))
            await CoroutineUtil.run(message.clear_reactions())

    @staticmethod
    def validate_channel(bot: Bot, channel) -> str:
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
            await CoroutineUtil.run(interaction.response.send_message(validate_msg))
            return
        await CoroutineUtil.run(interaction.response.send_message(
            "This will remove all messages from this channel. Are you sure?",
            view=SetChannelView(bot = bot, trackType = trackType)
        ))

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
        await CoroutineUtil.run(interaction.response.edit_message(view=None))
        await ChannelService.set_channel(self.bot, interaction.channel, self.trackType)

class SetChannelNoButton(discord.ui.Button):
    def __init__(self):
        super().__init__(style=discord.ButtonStyle.secondary, label='No')
    async def callback(self, interaction: discord.Interaction):
        await CoroutineUtil.run(interaction.response.edit_message(view=None))

class TrackView(discord.ui.View):
    def __init__(self, *, timeout = 180, bot, opts, mins_ago, user_time, track_type):
        super().__init__(timeout = timeout)
        self.add_item(TrackSelect(bot, opts, mins_ago, user_time, track_type))

class TrackSelect(discord.ui.Select):
    def __init__(self, bot: Bot, opts, mins_ago, user_time, track_type):
        self.bot = bot
        self.opts = opts
        self.mins_ago = mins_ago
        self.user_time = user_time
        self.track_type = track_type
        options = []
        for opt in self.opts:
            if track_type == TrackType.MVP:
                options.append(discord.SelectOption(label=opt["name"], description=opt["map"], value=opt["id"]))
            else:
                options.append(discord.SelectOption(label=opt["name"], value=opt["id"]))
        super().__init__(placeholder="Select an option",options=options)
    async def callback(self, interaction: discord.Interaction):
        entry = next((x for x in self.opts if str(x["id"]) == self.values[0]), None)
        guild_state = self.bot.guild_state_map.get(interaction.guild_id)
        if guild_state is None:
            return
        channel_state = guild_state['channel_state_map'].get(interaction.channel_id)
        bot_reply_msg = await ChannelService.update_track_time(self.bot, channel_state, entry, self.mins_ago, self.user_time, interaction.user.id)
        await CoroutineUtil.run(interaction.response.edit_message(content=bot_reply_msg, view=None))

class ChannelMessageView(discord.ui.View):
    def __init__(self, *, timeout = None, bot: Bot, channel_state: dict):
        self.bot = bot
        self.channel_state = channel_state
        super().__init__(timeout = timeout)
        self.add_item(ChannelMessageTrackButton(bot = bot, channel_state = channel_state))

class ChannelMessageTrackButton(discord.ui.Button):
    def __init__(self, bot: Bot, channel_state: dict):
        self.bot = bot
        self.channel_state = channel_state
        super().__init__(style = discord.ButtonStyle.primary, emoji = "➕", label = f"TRACK {channel_state['type'].desc}")
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(ChannelMessageTrackModal(bot = self.bot, channel_state=self.channel_state))

class ChannelMessageTrackModal(discord.ui.Modal):
    def __init__(self, bot: Bot, channel_state: dict):
        super().__init__(title = f"TRACK {channel_state['type'].desc}")
        self.bot = bot
        self.channel_state = channel_state
        self.name_input = discord.ui.TextInput(label = "Name")
        self.time_input = discord.ui.TextInput(label = "Time", required = False)
        self.add_item(self.name_input)
        self.add_item(self.time_input)
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking = False)
        name = self.name_input.value.strip()
        if len(name) > 0:
            user_time = self.time_input.value.strip()
            if len(user_time) == 0:
                user_time = None
            await ChannelService.track_entry(self.bot, self.channel_state, interaction.channel, interaction.user, name, user_time)

