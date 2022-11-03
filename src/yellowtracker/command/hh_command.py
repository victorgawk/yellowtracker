import discord
from yellowtracker.domain.bot import Bot
from yellowtracker.domain.emoji import Emoji
from yellowtracker.service.event_service import EventService
from yellowtracker.util.date_util import DateUtil
from yellowtracker.util.coroutine_util import CoroutineUtil

class HhCommand:

    @staticmethod
    async def hh(interaction: discord.Interaction, bot: Bot):
        bghh_map = EventService.get_hh_map(bot)
        embed = discord.Embed()
        embed.title = f"{Emoji.HH.value} BG Happy Hour"
        embed.colour = discord.Colour.gold()
        if bghh_map['ongoing'] != '':
            embed.add_field(name='Ongoing :boom:', value=bghh_map['ongoing'], inline=False)
        embed.add_field(name='Next :arrow_right:', value=bghh_map['next'], inline=False)
        if bghh_map['today'] != '':
            embed.add_field(name='Today', value=bghh_map['today'], inline=False)
        if bghh_map['tomorrow'] != '':
            embed.add_field(name='Tomorrow', value=bghh_map['tomorrow'], inline=False)
        footer = 'Server Time (' + bot.TIMEZONE + '): '
        footer += DateUtil.fmt_dt(DateUtil.get_dt_now(bot.TIMEZONE))
        embed.set_footer(text=footer)
        await CoroutineUtil.run(interaction.response.send_message(embed=embed))
