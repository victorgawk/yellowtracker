import discord
import asyncio
from discord.ext import commands
from discord.ext.commands import has_permissions
from datetime import datetime, timedelta
import terminaltables
from base.cog import Cog
from util.date import DateUtil
from collections import deque
from util.coroutine import CoroutineUtil

emojis = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣']

class TrackType:
    MVP = 1
    MINING = 2

class Track(Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.wait_load_stuff()
        conn = await self.bot.pool.acquire()
        try:
            for guild in self.bot.guilds:
                guild_state = self.bot.guild_state_map.get(guild.id)
                if guild_state is None:
                    continue
                if guild_state['id_mvp_channel'] is not None:
                    channel_state = {}
                    channel_state['id_channel'] = guild_state['id_mvp_channel']
                    channel_state['id_guild'] = guild.id
                    channel_state['type'] = TrackType.MVP
                    channel_state['id_message'] = None
                    channel_state['entry_state_list'] = []
                    channel_state['entry_log_list'] = deque()
                    guild_state['channel_state_map'][guild_state['id_mvp_channel']] = channel_state
                if guild_state['id_mining_channel'] is not None:
                    channel_state = {}
                    channel_state['id_channel'] = guild_state['id_mining_channel']
                    channel_state['id_guild'] = guild.id
                    channel_state['type'] = TrackType.MINING
                    channel_state['id_message'] = None
                    channel_state['entry_state_list'] = []
                    channel_state['entry_log_list'] = deque()
                    guild_state['channel_state_map'][guild_state['id_mining_channel']] = channel_state
            self.bot.mvp_list = []
            db_mvp_list = await conn.fetch('SELECT * FROM mvp')
            for db_mvp in db_mvp_list:
                mvp_dict = dict(db_mvp)
                mvp_dict['alias'] = []
                self.bot.mvp_list.append(mvp_dict)
            db_mvp_alias_list = await conn.fetch('SELECT * FROM mvp_alias')
            for db_mvp_alias in db_mvp_alias_list:
                mvp = next(x for x in self.bot.mvp_list if x['id'] == db_mvp_alias['id_mvp'])
                mvp['alias'].append(db_mvp_alias['alias'])
            self.bot.mining_list = []
            db_mining_list = await conn.fetch('SELECT * FROM mining')
            for db_mining in db_mining_list:
                mining_dict = dict(db_mining)
                mining_dict['t1'] = 30
                mining_dict['alias'] = []
                self.bot.mining_list.append(mining_dict)
            await load_db_entries(self.bot, conn, TrackType.MVP)
            await load_db_entries(self.bot, conn, TrackType.MINING)
            for id_guild in self.bot.guild_state_map:
                guild_state = self.bot.guild_state_map[id_guild]
                guild = next((x for x in self.bot.guilds if x.id == id_guild), None)
                if guild is None:
                    continue
                for id_channel in guild_state['channel_state_map']:
                    await init_channel(self.bot, guild_state['channel_state_map'][id_channel])
        finally:
            await self.bot.pool.release(conn)

    @commands.Cog.listener()
    async def on_message(self, message):
        user = message.author
        channel = message.channel
        if not isinstance(channel, discord.TextChannel):
            return
        guild_state = self.bot.guild_state_map.get(channel.guild.id)
        if guild_state is None:
            return
        channel_state = guild_state['channel_state_map'].get(channel.id)
        user_state = guild_state['user_state_map'].get(user.id)
        if user_state is not None and channel_state is not None:
            if not message.content.isnumeric():
                return
            index = int(message.content) - 1
            if index < 0 or index >= len(user_state['results']):
                return
            guild_state['user_state_map'][user.id] = None
            entry = user_state['results'][index]
            bot_reply_msg = await update_track_time(self.bot, channel_state, entry, user_state['mins_ago'], user)
            await CoroutineUtil.run(user_state['bot_msg'].edit(content=fmt_msg(bot_reply_msg)))
            await CoroutineUtil.run(user_state['bot_msg'].clear_reactions())

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user == self.bot.user:
            return
        channel = reaction.message.channel
        guild_state = self.bot.guild_state_map.get(channel.guild.id)
        if guild_state is None:
            return
        channel_state = guild_state['channel_state_map'].get(channel.id)
        user_state = guild_state['user_state_map'].get(user.id)
        if user_state is not None and channel_state is not None:
            index = -1
            try:
                index = emojis.index(reaction.emoji)
            except ValueError:
                return
            guild_state['user_state_map'][user.id] = None
            entry = user_state['results'][index]
            bot_reply_msg = await update_track_time(self.bot, channel_state, entry, user_state['mins_ago'], user)
            await CoroutineUtil.run(user_state['bot_msg'].edit(content=fmt_msg(bot_reply_msg)))
            await CoroutineUtil.run(user_state['bot_msg'].clear_reactions())

    @commands.command(help='Enable/disable custom TalonRO MVP respawn times')
    @commands.guild_only()
    @has_permissions(administrator=True)
    @commands.bot_has_permissions(send_messages=True)
    async def talonro(self, ctx):
        guild_state = self.bot.guild_state_map[ctx.guild.id]
        talonro = not guild_state['talonro']
        guild_state['talonro'] = talonro
        conn = await self.bot.pool.acquire()
        try:
            write_sql = 'UPDATE guild SET talonro=$2 WHERE id=$1'
            await conn.execute(write_sql, ctx.guild.id, talonro)
        finally:
            await self.bot.pool.release(conn)
        msg = 'TalonRO custom MVP respawn times '
        msg += 'enabled.' if talonro else 'disabled.'
        await CoroutineUtil.run(ctx.send(fmt_msg(msg)))

    @commands.command(help='Set the MVP channel')
    @commands.guild_only()
    @has_permissions(administrator=True)
    @commands.bot_has_permissions(send_messages=True)
    async def setmvpchannel(self, ctx, channel: discord.TextChannel = None):
        await set_channel(self.bot, ctx, channel, TrackType.MVP)

    @commands.command(help='Set the mining channel')
    @commands.guild_only()
    @has_permissions(administrator=True)
    @commands.bot_has_permissions(send_messages=True)
    async def setminingchannel(self, ctx, channel: discord.TextChannel = None):
        await set_channel(self.bot, ctx, channel, TrackType.MINING)

    @commands.command(help='Unset the MVP channel')
    @commands.guild_only()
    @has_permissions(administrator=True)
    @commands.bot_has_permissions(send_messages=True)
    async def unsetmvpchannel(self, ctx):
        await unset_channel(self.bot, ctx, TrackType.MVP)

    @commands.command(help='Unset the mining channel')
    @commands.guild_only()
    @has_permissions(administrator=True)
    @commands.bot_has_permissions(send_messages=True)
    async def unsetminingchannel(self, ctx):
        await unset_channel(self.bot, ctx, TrackType.MINING)

    @commands.command(aliases=['t'], help='Track a MVP that has been defeated')
    @commands.guild_only()
    @commands.bot_has_permissions(send_messages=True)
    async def track(self, ctx, *args):
        validate_msg = validate_channel(self.bot, ctx.message.channel)
        if validate_msg is not None:
            await CoroutineUtil.run(ctx.send(fmt_msg(validate_msg)))
            return
        guild_state = self.bot.guild_state_map[ctx.guild.id]
        channel_state = guild_state['channel_state_map'].get(ctx.message.channel.id)
        if channel_state is None:
            await CoroutineUtil.run(ctx.send(fmt_msg('This command can only be used in a track channel.')))
            return
        mins_ago = 0
        if len(args) == 0:
            return
        query_last_idx = len(args) - 1
        if args[query_last_idx].isnumeric():
            mins_ago = int(args[query_last_idx])
            query_last_idx -= 1
        elif len(args[query_last_idx]) == 5 and args[query_last_idx][2] == ':':
            hrs_mins = args[query_last_idx].split(':')
            if len(hrs_mins) == 2 and hrs_mins[0].isnumeric() and hrs_mins[1].isnumeric():
                hh = int(hrs_mins[0])
                mm = int(hrs_mins[1])
                track_time = DateUtil.get_dt_now(self.bot.tz_str)
                if hh > track_time.hour or (hh == track_time.hour and mm > track_time.minute):
                    track_time -= timedelta(days=1)
                track_time = track_time.replace(hour=hh, minute=mm)
                td = DateUtil.get_dt_now(self.bot.tz_str) - track_time
                mins_ago = td / timedelta(minutes=1)
                query_last_idx -= 1
        if mins_ago < 0:
            mins_ago = 0
        query = args[0]
        for i in range(1, query_last_idx + 1):
            query += ' ' + args[i]
        type = channel_state['type']
        results = find_entry(self.bot, query, type)
        if len(results) == 0:
            await CoroutineUtil.run(ctx.send(fmt_msg(entry_desc(type) + ' "' + query + '" not found.')))
        elif len(results) == 1:
            bot_reply_msg = await update_track_time(self.bot, channel_state, results[0], mins_ago, ctx.message.author)
            await CoroutineUtil.run(ctx.send(fmt_msg(bot_reply_msg)))
        else:
            bot_reply_msg = 'More than one ' + entry_desc(type)
            bot_reply_msg += ' starting with "' + query + '" has been found.\n'
            bot_reply_msg += '\n'
            bot_reply_msg += 'Type or react with the number of the ' + entry_desc(type)
            bot_reply_msg += ' that you want to track:\n'
            bot_reply_msg += '\n'
            for i in range(0, min(len(results),5)):
                bot_reply_msg += str(i + 1) + '. ' + results[i]['name'] 
                if type == TrackType.MVP:
                    bot_reply_msg += ' (' + results[i]['map'] + ')'
                bot_reply_msg += '\n'
            bot_msg = await CoroutineUtil.run(ctx.send(fmt_msg(bot_reply_msg)))
            user_entry_state = guild_state['user_state_map'].get(ctx.message.author.id)
            if user_entry_state is not None and user_entry_state['bot_msg'] is not None:
                await CoroutineUtil.run(user_entry_state['bot_msg'].delete())
            guild_state['user_state_map'][ctx.message.author.id] = {
                'bot_msg': bot_msg,
                'results': results,
                'mins_ago': mins_ago
            }
            for i in range(0, min(len(results),5)):
                await CoroutineUtil.run(bot_msg.add_reaction(emojis[i]))

    async def timer(self):
        for guild in self.bot.guilds:
            guild_state = self.bot.guild_state_map.get(guild.id)
            if guild_state is None:
                continue
            for id_channel in guild_state['channel_state_map'].copy():
                channel_state = guild_state['channel_state_map'].get(id_channel)
                if channel_state is None:
                    continue
                for entry_state in channel_state['entry_state_list']:
                    calc_remaining_time(entry_state, entry_state['track_time'], channel_state['type'])
                await update_channel_message(self.bot, channel_state)
                channel = next((x for x in guild.channels if x.id == channel_state['id_channel']), None)
                if validate_channel(self.bot, channel) is not None:
                    continue
                msgs = await CoroutineUtil.run(channel.history(limit=100).flatten())
                if msgs is None:
                    continue
                for msg in msgs:
                    if msg.id == channel_state['id_message']:
                        continue
                    msg_date = msg.created_at if msg.edited_at is None else msg.edited_at
                    if datetime.utcnow() - msg_date > timedelta(seconds=self.bot.config['del_msg_after_secs']):
                        await CoroutineUtil.run(msg.delete())

async def set_channel(bot, ctx, channel, type):
    if channel is None:
        channel = ctx.message.channel
    validate_msg = validate_channel(bot, channel)
    if validate_msg is not None:
        await CoroutineUtil.run(ctx.send(fmt_msg(validate_msg)))
        return
    guild_state = bot.guild_state_map[ctx.guild.id]
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
        'id_guild': ctx.guild.id,
        'type': type,
        'id_message': None,
        'entry_state_list': entry_state_list,
        'entry_log_list': deque()
    }
    channel_state_map[channel.id] = channel_state
    await init_channel(bot, channel_state)
    conn = await bot.pool.acquire()
    try:
        sql  = 'UPDATE guild '
        sql += 'SET id_' + entry_desc_sql(type) + '_channel=$1 '
        sql += 'WHERE id=$2'
        await conn.execute(sql, channel.id, ctx.guild.id)
    finally:
        await bot.pool.release(conn)
    await CoroutineUtil.run(ctx.send(fmt_msg('New ' + entry_desc(type) + ' channel set to "' + channel.name + '".')))

async def unset_channel(bot, ctx, type):
    validate_msg = validate_channel(bot, ctx.message.channel)
    if validate_msg is not None:
        await CoroutineUtil.run(ctx.send(fmt_msg(validate_msg)))
        return
    guild_state = bot.guild_state_map[ctx.guild.id]
    channel_state_map = guild_state['channel_state_map']
    channel_state = next(
        (
            channel_state_map[x]
            for x in channel_state_map
            if channel_state_map[x]['type'] == type
        ),
        None
    )
    if channel_state is None:
        await CoroutineUtil.run(ctx.send(fmt_msg('There is no ' + entry_desc(type) + ' channel set.')))
        return
    del channel_state_map[channel_state['id_channel']]
    conn = await bot.pool.acquire()
    try:
        sql  = 'UPDATE guild '
        sql += 'SET id_' + entry_desc_sql(type) + '_channel=NULL '
        sql += 'WHERE id=$1'
        await conn.execute(sql, ctx.guild.id)
    finally:
        await bot.pool.release(conn)
    await CoroutineUtil.run(ctx.send(fmt_msg(entry_desc(type) + ' channel unset.')))

async def load_db_entries(bot, conn, type):
    db_entry_guild_list = await conn.fetch('SELECT * FROM ' + entry_desc_sql(type) + '_guild')
    entry_list = bot.mvp_list if type == TrackType.MVP else bot.mining_list
    for db_entry_guild in db_entry_guild_list:
        guild_state = bot.guild_state_map[db_entry_guild['id_guild']]
        if guild_state is None:
            continue
        entry = next(
            x for x in entry_list
            if x['id'] == db_entry_guild['id_' + entry_desc_sql(type)]
        )
        channel_state_map = guild_state['channel_state_map']
        channel_state = next(
            (
                channel_state_map[x]
                for x in channel_state_map
                if channel_state_map[x]['type'] == type
            ),
            None
        )
        if channel_state is None:
            continue
        await track_entry(bot, channel_state, entry, db_entry_guild['track_time'])
    await load_db_entries_log(bot, conn, type)

async def load_db_entries_log(bot, conn, type):
    sql = 'SELECT * FROM ' + entry_desc_sql(type) + '_guild_log ORDER BY log_date DESC'
    db_entry_log_list = await conn.fetch(sql)
    entry_list = bot.mvp_list if type == TrackType.MVP else bot.mining_list
    for db_entry_log in db_entry_log_list:
        guild_state = bot.guild_state_map[db_entry_log['id_guild']]
        if guild_state is None:
            continue
        entry = next(
            x for x in entry_list
            if x['id'] == db_entry_log['id_' + entry_desc_sql(type)]
        )
        channel_state_map = guild_state['channel_state_map']
        channel_state = next(
            (
                channel_state_map[x]
                for x in channel_state_map
                if channel_state_map[x]['type'] == type
            ),
            None
        )
        if channel_state is None:
            continue
        if len(channel_state['entry_log_list']) < 3:
            channel_state['entry_log_list'].append({
                'entry': entry,
                'log_date': db_entry_log['log_date'],
                'log_user': db_entry_log['log_user']
            })
            continue
        delete_sql = 'DELETE FROM ' + entry_desc_sql(type) + '_guild_log'
        delete_sql += ' WHERE id_guild=$1'
        delete_sql += ' AND id_' + entry_desc_sql(type) + '=$2'
        delete_sql += ' AND log_date=$3'
        delete_sql += ' AND log_user=$4'
        await conn.execute(
            delete_sql,
            db_entry_log['id_guild'],
            db_entry_log['id_' + entry_desc_sql(type)],
            db_entry_log['log_date'],
            db_entry_log['log_user']
        )

async def init_channel(bot, channel_state):
    guild = next(x for x in bot.guilds if x.id == channel_state['id_guild'])
    channel = next((x for x in guild.channels if x.id == channel_state['id_channel']), None)
    if validate_channel(bot, channel) is not None:
        return
    channel_state['id_message'] = None
    msgs = await CoroutineUtil.run(channel.history(oldest_first=True).flatten())
    if msgs is None:
        return
    msgs_to_delete = []
    for msg in msgs:
        if msg.type == discord.MessageType.default and msg.author == bot.user and channel_state['id_message'] is None:
            channel_state['id_message'] = msg.id
            await update_channel_message(bot, channel_state)
            continue
        msgs_to_delete.append(msg)
    await CoroutineUtil.run(channel.delete_messages(msgs_to_delete))

async def update_track_time(bot, channel_state, entry, mins_ago, log_user):
    conn = await bot.pool.acquire()
    type = channel_state['type']
    track_time = datetime.now() - timedelta(minutes=mins_ago)
    try:
        read_sql = 'SELECT * FROM ' + entry_desc_sql(type) + '_guild '
        read_sql += 'WHERE id_' + entry_desc_sql(type) + '=$1 AND id_guild=$2'
        entry_guild_db = await conn.fetch(
            read_sql,
            entry['id'],
            channel_state['id_guild']
        )
        write_sql = 'INSERT INTO ' + entry_desc_sql(type) + '_guild(id_' + entry_desc_sql(type)
        write_sql += ',id_guild,track_time)VALUES($1,$2,$3)'
        if len(entry_guild_db) > 0:
            write_sql = 'UPDATE ' + entry_desc_sql(type) + '_guild SET track_time=$3 '
            write_sql += 'WHERE id_' + entry_desc_sql(type) + '=$1 AND id_guild=$2'
        await conn.execute(write_sql, entry['id'], channel_state['id_guild'], track_time)
        log_sql = 'INSERT INTO ' + entry_desc_sql(type) + '_guild_log(id_' + entry_desc_sql(type)
        log_sql += ',id_guild,log_date,log_user)VALUES($1,$2,$3,$4)'
        log_date = datetime.now()
        log_user_str = str(log_user)
        await conn.execute(log_sql, entry['id'], channel_state['id_guild'], log_date, log_user_str)
        channel_state['entry_log_list'].appendleft({
            'entry': entry,
            'log_date': log_date,
            'log_user': log_user_str
        })
        if len(channel_state['entry_log_list']) > 3:
            channel_state['entry_log_list'].pop()
    finally:
        await bot.pool.release(conn)
    entry_state = await track_entry(bot, channel_state, entry, track_time)
    await update_channel_message(bot, channel_state)
    msg = entry_state['entry']['name']
    if type == TrackType.MVP:
        msg += ' (' 
        msg += entry_state['entry']['map']
        msg += ')'
    msg += ' in '
    msg += str(int(entry_state['r1']))
    if type == TrackType.MVP:
        msg += ' to '
        msg += str(int(entry_state['r2']))
    msg += ' minutes.'
    return msg

async def track_entry(bot, channel_state, entry, track_time):
    type = channel_state['type']
    entry_state = next((x for x in channel_state['entry_state_list'] if x['entry'] == entry), None)   
    if entry_state is None:
        entry_state = {}
        entry_state['entry'] = entry
        entry_state['r1'] = -999
        if type == TrackType.MVP:
            entry_state['r2'] = -999
        channel_state['entry_state_list'].append(entry_state)
    entry_state['t1'] = entry['t1']
    if type == TrackType.MVP:
        entry_state['t2'] = entry['t2']
        if bot.guild_state_map[channel_state['id_guild']]['talonro'] and entry['t1talonro'] is not None:
            entry_state['t1'] = entry['t1talonro']
            entry_state['t2'] = entry['t2talonro']
    entry_state['track_time'] = track_time
    calc_remaining_time(entry_state, track_time, type)
    channel_state['entry_state_list'].sort(key=lambda e : e['r1'])
    return entry_state

def calc_remaining_time(entry_state, track_time, type):
    mins_ago = round((datetime.now() - track_time).total_seconds() / 60)
    entry_state['r1'] = entry_state['t1'] - mins_ago
    if type == TrackType.MVP:
        entry_state['r2'] = entry_state['t2'] - mins_ago

async def update_channel_message(bot, channel_state):
    type = channel_state['type']
    table = []
    table_labels = []
    table_labels.append('Name')
    if type == TrackType.MVP:
        table_labels.append('Map')
    table_labels.append('Remaining Time')
    table.append(table_labels)
    cmp = 'r2' if type == TrackType.MVP else 'r1'
    for entry_state in channel_state['entry_state_list']:
        if entry_state[cmp] <= -bot.config['table_entry_expiration_mins']:
            entry_state['r1'] = -999
            if type == TrackType.MVP:
                entry_state['r2'] = -999
            conn = await bot.pool.acquire()
            try:
                sql  = 'DELETE FROM ' + entry_desc_sql(type) + '_guild '
                sql += 'WHERE id_guild=$1 AND id_' + entry_desc_sql(type) + '=$2'
                await conn.execute(sql, channel_state['id_guild'], entry_state['entry']['id'])
            finally:
                await bot.pool.release(conn)
        if entry_state[cmp] > -bot.config['table_entry_expiration_mins']:
            remaining_time = str(int(entry_state['r1']))
            if type == TrackType.MVP:
                remaining_time += ' to ' + str(int(entry_state['r2']))
            remaining_time += ' mins'
            table_row = []
            table_row.append(entry_state['entry']['name'])
            if type == TrackType.MVP:
                table_row.append(entry_state['entry']['map'])
            table_row.append(remaining_time)
            table.append(table_row)
    result = 'No ' + entry_desc(type) + ' has been tracked.'
    if len(table) > 1:
        max_length = 20
        if len(table) > max_length + 1:
            diff = len(table) - max_length
            for i in range(0, diff):
                table.pop()
            table_row = []
            table_row.append('and ' + str(diff) + ' more...')
            if type == TrackType.MVP:
                table_row.append('')
            table_row.append('')
            table.append(table_row)
        result = entry_desc(type) + 'S\n'
        result += terminaltables.AsciiTable(table).table
    if len(channel_state['entry_log_list']) > 0:
        result += '\n\nTRACK LOG:\n'
        for entry_log in channel_state['entry_log_list']:
            milliseconds = (entry_log['log_date'] - datetime.now()) / timedelta(milliseconds=1)
            result += '[' + DateUtil.fmt_time_short(milliseconds) + ']'
            result += ' ' + entry_log['entry']['name']
            if type == TrackType.MVP:
                result += ' (' + entry_log['entry']['map'] + ')'
            result += ' by ' + entry_log['log_user']
            result += '\n'
    guild = next((x for x in bot.guilds if x.id == channel_state['id_guild']), None)
    if guild is None:
        return
    channel = next((x for x in guild.channels if x.id == channel_state['id_channel']), None)
    if validate_channel(bot, channel) is not None:
        return
    message = None
    if channel_state['id_message'] is not None:
        message = await CoroutineUtil.run_with_retries(channel.fetch_message(channel_state['id_message']))
    if message is None:
        message = await CoroutineUtil.run(channel.send(content=fmt_msg(result)))
        if message is not None:
            channel_state['id_message'] = message.id
    else:
        await CoroutineUtil.run(message.edit(content=fmt_msg(result)))
        await CoroutineUtil.run(message.clear_reactions())

def validate_channel(bot, channel):
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

def find_entry(bot, query, type):
    entry_list = bot.mvp_list if type == TrackType.MVP else bot.mining_list
    results = []
    for entry in entry_list:
        compare = entry['name']
        if type == TrackType.MVP:
            compare += ' ' + entry['map']
        if compare.lower() == query.lower():
            if entry not in results:
                results.append(entry)
            return results
        if compare.lower().startswith(query.lower()):
            if entry not in results:
                results.append(entry)
        for alias in entry['alias']:
            compare = alias
            if type == TrackType.MVP:
                compare += ' ' + entry['map']
            if compare.lower() == query.lower():
                if entry not in results:
                    results.append(entry)
                return results
            if compare.lower().startswith(query.lower()):
                if entry not in results:
                    results.append(entry)
    return results

def entry_desc_sql(type):
    return entry_desc(type, sql=True)

def entry_desc(type, sql=False):
    if sql:
        return 'mvp' if type == TrackType.MVP else 'mining'
    return 'MVP' if type == TrackType.MVP else 'MINING ZONE'

def fmt_msg(msg):
    return '```\n' + msg + '```'

def setup(bot):
    bot.add_cog(Track(bot))
