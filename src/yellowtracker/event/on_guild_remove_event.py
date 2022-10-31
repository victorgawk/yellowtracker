import logging
from yellowtracker.domain.bot import Bot

log = logging.getLogger(__name__)

class OnGuildRemoveEvent:

    @staticmethod
    async def on_guild_remove(guild, bot: Bot):
        log.info(f"Withdrawn from {guild.name}.")
        bot.guild_state_map[guild.id] = None
        conn = await bot.pool_acquire()
        try:
            await conn.execute('DELETE FROM mvp_guild WHERE id_guild=$1', guild.id)
            await conn.execute('DELETE FROM mining_guild WHERE id_guild=$1', guild.id)
            await conn.execute('DELETE FROM guild WHERE id=$1', guild.id)
        finally:
            await bot.pool_release(conn)