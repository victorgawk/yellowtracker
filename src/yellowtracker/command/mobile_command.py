import discord
from yellowtracker.domain.bot import Bot
from yellowtracker.service.channel_service import ChannelService
from yellowtracker.util.coroutine_util import CoroutineUtil

class MobileCommand:

    @staticmethod
    async def mobile(interaction: discord.Interaction, bot: Bot):
        guild_state = bot.guild_state_map[interaction.guild_id]
        mobile = not guild_state['mobile']
        guild_state['mobile'] = mobile
        conn = await bot.pool_acquire()
        try:
            write_sql = 'UPDATE guild SET mobile=$2 WHERE id=$1'
            await conn.execute(write_sql, interaction.guild_id, mobile)
        finally:
            await bot.pool_release(conn)
        msg = 'MVP list mobile layout '
        msg += 'enabled.' if mobile else 'disabled.'
        channel_state = guild_state['channel_state_map'].get(interaction.channel_id)
        await CoroutineUtil.run(interaction.response.send_message(msg))
        await ChannelService.update_channel_message(bot, channel_state)
