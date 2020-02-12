from datetime import datetime, timedelta
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from cog.cog import Cog

class Admin(Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await send_member_message(
            self.bot,
            member.guild,
            member,
            ':wave: Member joined',
            '{0.mention} joined the server.'.format(member)
        )

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if self.bot.user.id == member.id:
            return
        await send_member_message(
            self.bot,
            member.guild,
            member,
            ':x: Member left',
            '**{0.name}** left the server.'.format(member)
        )

    @commands.command()
    @has_permissions(administrator=True)
    async def setmemberchannel(self, ctx, channel: discord.TextChannel = None):
        if channel is None:
            channel = ctx.message.channel
        guild_state = self.bot.guild_state_map[ctx.guild.id]
        guild_state['id_member_channel'] = channel.id
        conn = await self.bot.pool.acquire()
        try:
            sql = 'UPDATE guild SET id_member_channel=$1 WHERE id=$2'
            await conn.execute(sql, channel.id, ctx.guild.id)
        finally:
            await self.bot.pool.release(conn)
        await ctx.send('Member channel set to {0.mention}.'.format(channel))

    @commands.command()
    @has_permissions(administrator=True)
    async def unsetmemberchannel(self, ctx):
        guild_state = self.bot.guild_state_map[ctx.guild.id]
        guild_state['id_member_channel'] = None
        conn = await self.bot.pool.acquire()
        try:
            sql = 'UPDATE guild SET id_member_channel=NULL WHERE id=$1'
            await conn.execute(sql, ctx.guild.id)
        finally:
            await self.bot.pool.release(conn)
        await ctx.send('Member channel unset.')

async def send_member_message(bot, guild, user, title, description):
    guild_state = bot.guild_state_map[guild.id]
    id_channel = guild_state['id_member_channel']
    if id_channel is None:
        return
    channel = next(x for x in guild.channels if x.id == id_channel)
    if channel is None:
        return
    embed = discord.Embed()
    embed.title = title
    embed.description = description
    embed.set_thumbnail(url=user.avatar_url)
    embed.set_author(icon_url=user.avatar_url, name='{0}'.format(user))
    embed.colour = discord.Colour.gold()
    embed.set_footer(text='User ID: {0.id}'.format(user))
    await channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Admin(bot))