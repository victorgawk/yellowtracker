import discord
from yellowtracker.domain.bot import Bot
from yellowtracker.domain.emoji import Emoji
from yellowtracker.service.event_service import EventService
from yellowtracker.util.date_util import DateUtil
from yellowtracker.util.coroutine_util import CoroutineUtil
from yellowtracker.command import gmctokens

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
        await CoroutineUtil.run(interaction.response.send_message(embed=embed, view = GmcView(bot)))

class GmcView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout = None)
        self.bot = bot
        self.add_item(GmcTokensButton(bot = bot))

class GmcTokensButton(discord.ui.Button):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(style = discord.ButtonStyle.primary, emoji = "🗒️", label = "Manage GMC Tokens")
    async def callback(self, interaction: discord.Interaction):
        gmcTokenUser = gmctokens.GmcTokenUser(self.bot, interaction.user)
        await gmcTokenUser.initAccs()
        await interaction.user.send(embed = gmcTokenUser.embed(), view = gmctokens.GmcTokensView(gmcTokenUser = gmcTokenUser))
        await interaction.response.defer(thinking = False)
