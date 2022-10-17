from pytz import timezone
from datetime import datetime, timedelta
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import asyncpg
import asyncio
import math
from base.bot import Bot

intents = discord.Intents.default()
intents.message_content = True
bot = Bot(command_prefix='!', intents=intents)

extensions = (
    'Event',
    'Track',
    'Admin'
)

@bot.event
async def on_ready():
    bot.stuff_loaded = False
    for guild in bot.guilds:
        guild_state = {
            'id_guild': guild.id,
            'talonro': True,
            'mobile': False,
            'id_mvp_channel': None,
            'id_mining_channel': None,
            'id_member_channel': None,
            'user_state_map': {},
            'channel_state_map': {}
        }
        bot.guild_state_map[guild.id] = guild_state
    bot.pool = await asyncpg.create_pool(dsn=bot.config['database_url'])
    conn = await bot.pool.acquire()
    try:
        meta_sql = 'SELECT * FROM pg_catalog.pg_tables '
        meta_sql += 'WHERE schemaname=\'public\' and tablename=\'mvp\''
        db_table_list = await conn.fetch(meta_sql)
        if len(db_table_list) == 0:
            sql_file = open('sql/yellowtracker.sql', 'r')
            await conn.execute(sql_file.read())
        db_guild_list = await conn.fetch('SELECT * FROM guild')
        for guild in bot.guilds:
            db_guild = next((x for x in db_guild_list if x['id'] == guild.id), None)
            if db_guild is None:
                await conn.execute('INSERT INTO guild(id)VALUES($1)', guild.id)
                continue
            guild_state = bot.guild_state_map[guild.id]
            guild_state['talonro'] = db_guild['talonro']
            guild_state['mobile'] = db_guild['mobile']
            guild_state['id_mvp_channel'] = db_guild['id_mvp_channel']
            guild_state['id_mining_channel'] = db_guild['id_mining_channel']
            guild_state['id_member_channel'] = db_guild['id_member_channel']
        for db_guild in db_guild_list:
            if next((x for x in bot.guilds if x.id == db_guild['id']), None) is None:
                await conn.execute('DELETE FROM mvp_guild WHERE id_guild=$1', db_guild['id'])
                await conn.execute('DELETE FROM mining_guild WHERE id_guild=$1', db_guild['id'])
                await conn.execute('DELETE FROM guild WHERE id=$1', db_guild['id'])
    finally:
        await bot.pool.release(conn)
    bot.stuff_loaded = True

@bot.event
async def on_guild_join(guild):
    print('Joined to {0.name}!'.format(guild))
    guild_state = {
        'id_guild': guild.id,
        'talonro': True,
        'mobile': False,
        'id_mvp_channel': None,
        'id_mining_channel': None,
        'id_member_channel': None,
        'user_state_map': {},
        'channel_state_map': {}
    }
    bot.guild_state_map[guild.id] = guild_state
    conn = await bot.pool.acquire()
    try:
        read_sql = 'SELECT * FROM guild WHERE id=$1'
        guild_db = await conn.fetch(read_sql, guild.id)
        if len(guild_db) == 0:
            write_sql = 'INSERT INTO guild(id)VALUES($1)'
            await conn.execute(write_sql, guild.id)
    finally:
        await bot.pool.release(conn)

@bot.event
async def on_guild_remove(guild):
    print('Withdrawn from {0.name}.'.format(guild))
    bot.guild_state_map[guild.id] = None
    conn = await bot.pool.acquire()
    try:
        await conn.execute('DELETE FROM mvp_guild WHERE id_guild=$1', guild.id)
        await conn.execute('DELETE FROM mining_guild WHERE id_guild=$1', guild.id)
        await conn.execute('DELETE FROM guild WHERE id=$1', guild.id)
    finally:
        await bot.pool.release(conn)

@bot.event
async def on_command_error(ctx, error):
    return

async def timer_thread(bot):
    for extension in extensions:
        await bot.load_extension('cog.' + extension.lower())
    while True:
        for extension in extensions:
            cog = bot.get_cog(extension)
            if cog is not None and hasattr(cog, 'timer'):
                await cog.timer()
        await asyncio.sleep(bot.config['table_refresh_rate_secs'])


print('Bot started!'.format(bot))

tasks = [
    timer_thread(bot),
    bot.start(bot.config['bot_user_token'])
]

async def run_tasks_async():
    return await asyncio.gather(*(tasks))

def run_tasks():
  asyncio.run(run_tasks_async())

run_tasks()