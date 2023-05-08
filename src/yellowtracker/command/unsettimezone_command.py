import discord
import pytz
from yellowtracker.domain.bot import Bot
from yellowtracker.util.coroutine_util import CoroutineUtil

class UnsetTimezoneCommand:

    @staticmethod
    async def unsettimezone_cmd(interaction: discord.Interaction, bot: Bot):
        guild_state = bot.guild_state_map[interaction.guild_id]
        if guild_state.get('timezone'):
            guild_state.pop('timezone')
        conn = await bot.pool_acquire()
        try:
            write_sql = 'UPDATE guild SET timezone=NULL WHERE id=$1'
            await conn.execute(write_sql, interaction.guild_id)
        finally:
            await bot.pool_release(conn)
        await CoroutineUtil.run(interaction.response.send_message('Custom timezone unset.'))
