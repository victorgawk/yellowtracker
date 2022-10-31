from datetime import timezone
import discord
from yellowtracker.domain.bot import Bot
from yellowtracker.service.event_service import EventService
from yellowtracker.util.date_util import DateUtil
from yellowtracker.util.coroutine_util import CoroutineUtil

class WoeCommand:

    @staticmethod
    async def woe(interaction: discord.Interaction, bot: Bot):
        woe_map = EventService.get_woe_map(bot)
        embed = discord.Embed()
        embed.title = ':european_castle: WoE'
        embed.colour = discord.Colour.gold()
        if woe_map['ongoing'] != '':
            embed.add_field(name='Ongoing :boom:', value=woe_map['ongoing'], inline=False)
        embed.add_field(name='Next :arrow_right:', value=woe_map['next'], inline=False)
        embed.add_field(name='Saturday', value=woe_map['saturday'], inline=False)
        embed.add_field(name='Sunday', value=woe_map['sunday'], inline=False)
        footer = 'Server Time (' + bot.TIMEZONE + '): '
        footer += DateUtil.fmt_dt(DateUtil.get_dt_now(bot.TIMEZONE))
        embed.set_footer(text=footer)
        await CoroutineUtil.run(interaction.response.send_message(embed=embed))
