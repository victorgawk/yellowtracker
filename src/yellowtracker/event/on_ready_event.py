import discord
import collections
import asyncpg
import logging
import os
from yellowtracker.domain.bot import Bot
from yellowtracker.domain.track_type import TrackType
from yellowtracker.service.channel_service import ChannelService
from yellowtracker.service.entry_service import EntryService

log = logging.getLogger(__name__)

class OnReadyEvent:

    @staticmethod
    async def on_ready(bot: Bot, tree: discord.app_commands.CommandTree, guild: discord.Object | None):
        log.info(f"Connected as {bot.user} on {len(bot.guilds)} servers.")

        log.info(f"Syncing slash commands.")
        if guild is not None:
            tree.copy_global_to(guild=guild)
        await tree.sync(guild=guild)

        try:
            log.info(f"Creating database pool.")
            bot.pool = await asyncpg.create_pool(dsn=bot.DATABASE_URL)
        except Exception as e:
            log.error(f"Error trying to create database pool: {e}")
            os._exit(42)

        conn: asyncpg.connection.Connection = await bot.pool_acquire()
        try:
            await OnReadyEvent.load_database(bot, conn)
        finally:
            await bot.pool_release(conn)

    @staticmethod
    async def load_database(bot: Bot, conn: asyncpg.connection.Connection):
        meta_sql = 'SELECT * FROM pg_catalog.pg_tables WHERE schemaname=\'public\' and tablename=\'mvp\''
        db_table_list = await conn.fetch(meta_sql)
        if len(db_table_list) == 0:
            log.error(f"Initial database structure not found.")
            os._exit(42)

        log.info(f"Loading servers settings.")
        db_guild_list = await conn.fetch('SELECT * FROM guild')
        for db_guild in db_guild_list:
            if ChannelService.get_guild_from_bot(bot, db_guild['id']) is None:
                await conn.execute('DELETE FROM mvp_guild WHERE id_guild=$1', db_guild['id'])
                await conn.execute('DELETE FROM mining_guild WHERE id_guild=$1', db_guild['id'])
                await conn.execute('DELETE FROM guild WHERE id=$1', db_guild['id'])
        for guild in bot.guilds:
            guild_state = {
                'id_guild': guild.id,
                'custom': True,
                'mobile': False,
                'id_mvp_channel': None,
                'id_mining_channel': None,
                'id_member_channel': None,
                'user_state_map': {},
                'channel_state_map': {}
            }
            bot.guild_state_map[guild.id] = guild_state
            db_guild = next((x for x in db_guild_list if x['id'] == guild.id), None)
            if db_guild is None:
                await conn.execute('INSERT INTO guild(id)VALUES($1)', guild.id)
            else:
                guild_state['custom'] = db_guild['custom']
                guild_state['mobile'] = db_guild['mobile']
                guild_state['id_mvp_channel'] = db_guild['id_mvp_channel']
                guild_state['id_mining_channel'] = db_guild['id_mining_channel']
                guild_state['id_member_channel'] = db_guild['id_member_channel']
                if guild_state['id_mvp_channel'] is not None:
                    channel_state = {}
                    channel_state['id_channel'] = guild_state['id_mvp_channel']
                    channel_state['id_guild'] = guild.id
                    channel_state['type'] = TrackType.MVP
                    channel_state['id_message'] = None
                    channel_state['entry_state_list'] = []
                    channel_state['entry_log_list'] = collections.deque()
                    guild_state['channel_state_map'][guild_state['id_mvp_channel']] = channel_state
                if guild_state['id_mining_channel'] is not None:
                    channel_state = {}
                    channel_state['id_channel'] = guild_state['id_mining_channel']
                    channel_state['id_guild'] = guild.id
                    channel_state['type'] = TrackType.MINING
                    channel_state['id_message'] = None
                    channel_state['entry_state_list'] = []
                    channel_state['entry_log_list'] = collections.deque()
                    guild_state['channel_state_map'][guild_state['id_mining_channel']] = channel_state

        log.info("Loading MVPs.")
        bot.mvp_list = []
        db_mvp_list = await conn.fetch('SELECT * FROM mvp')
        for db_mvp in db_mvp_list:
            mvp_dict = dict(db_mvp)
            mvp_dict['alias'] = []
            bot.mvp_list.append(mvp_dict)
        db_mvp_alias_list = await conn.fetch('SELECT * FROM mvp_alias')
        for db_mvp_alias in db_mvp_alias_list:
            mvp = next(x for x in bot.mvp_list if x['id'] == db_mvp_alias['id_mvp'])
            mvp['alias'].append(db_mvp_alias['alias'])

        log.info("Loading mining locations.")
        bot.mining_list = []
        db_mining_list = await conn.fetch('SELECT * FROM mining')
        for db_mining in db_mining_list:
            mining_dict = dict(db_mining)
            mining_dict['t1'] = 30
            mining_dict['alias'] = []
            bot.mining_list.append(mining_dict)

        log.info("Loading MVP entries.")
        await EntryService.load_db_entries(bot, conn, TrackType.MVP)

        log.info("Loading mining location entries.")
        await EntryService.load_db_entries(bot, conn, TrackType.MINING)

        log.info("Initializing track channels.")
        for id_guild in bot.guild_state_map:
            guild_state = bot.guild_state_map[id_guild]
            guild = ChannelService.get_guild_from_bot(bot, id_guild)
            if guild is None:
                continue
            for id_channel in guild_state['channel_state_map']:
                await ChannelService.init_channel(bot, guild_state['channel_state_map'][id_channel])