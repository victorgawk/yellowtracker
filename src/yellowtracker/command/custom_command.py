import discord
from yellowtracker.domain.bot import Bot
from yellowtracker.util.coroutine_util import CoroutineUtil

class CustomCommand:

    @staticmethod
    async def custom_cmd(interaction: discord.Interaction, bot: Bot):
        guild_state = bot.guild_state_map[interaction.guild_id]
        custom = not guild_state['custom']
        guild_state['custom'] = custom
        conn = await bot.pool_acquire()
        try:
            write_sql = 'UPDATE guild SET custom=$2 WHERE id=$1'
            await conn.execute(write_sql, interaction.guild_id, custom)
        finally:
            await bot.pool_release(conn)
        msg = 'Custom MVP respawn times '
        msg += 'enabled.' if custom else 'disabled.'
        await CoroutineUtil.run(interaction.response.send_message(msg))
