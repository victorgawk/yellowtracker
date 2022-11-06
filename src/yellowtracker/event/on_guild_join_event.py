import discord
import logging
from yellowtracker.domain.bot import Bot
from yellowtracker.util.coroutine_util import CoroutineUtil

log = logging.getLogger(__name__)

class OnGuildJoinEvent:

    @staticmethod
    async def on_guild_join(guild, tree: discord.app_commands.CommandTree, bot: Bot):
        tree.copy_global_to(guild=guild)
        await CoroutineUtil.run(tree.sync(guild=guild))
        log.info(f"Joined to {guild.name}.")
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
        conn = await bot.pool_acquire()
        try:
            read_sql = 'SELECT * FROM guild WHERE id=$1'
            guild_db = await conn.fetch(read_sql, guild.id)
            if len(guild_db) == 0:
                write_sql = 'INSERT INTO guild(id)VALUES($1)'
                await conn.execute(write_sql, guild.id)
        finally:
            await bot.pool_release(conn)