import discord
from yellowtracker.domain.bot import Bot
from yellowtracker.domain.emoji import Emoji
from yellowtracker.service.event_service import EventService
from yellowtracker.util.date_util import DateUtil
from yellowtracker.util.coroutine_util import CoroutineUtil

class GmcCommand:

    @staticmethod
    async def gmc(interaction: discord.Interaction, bot: Bot):
        gmc_map = EventService.get_gmc_map(bot)
        embed = discord.Embed()
        embed.title = f"{Emoji.GMC.value} GMC"
        embed.colour = discord.Colour.gold()
        if gmc_map['ongoing'] != '':
            embed.add_field(name='Ongoing :boom:', value=gmc_map['ongoing'], inline=False)
        embed.add_field(name='Next :arrow_right:', value=gmc_map['next'], inline=False)
        if gmc_map['today'] != '':
            embed.add_field(name='Today', value=gmc_map['today'], inline=False)
        if gmc_map['tomorrow'] != '':
            embed.add_field(name='Tomorrow', value=gmc_map['tomorrow'], inline=False)
        footer = 'Server Time (' + bot.TIMEZONE + '): ' 
        footer += DateUtil.fmt_dt(DateUtil.get_dt_now(bot.TIMEZONE))
        embed.set_footer(text=footer)
        await CoroutineUtil.run(interaction.response.send_message(embed=embed))
