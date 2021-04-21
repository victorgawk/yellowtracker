from datetime import datetime, timedelta
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from base.cog import Cog
from util.coroutine import CoroutineUtil
from cog.track import TrackType

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

    @commands.command(help='Set the member channel')
    @commands.guild_only()
    @has_permissions(administrator=True)
    @commands.bot_has_permissions(send_messages=True)
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
        await CoroutineUtil.run(ctx.send('Member channel set to {0.mention}.'.format(channel)))

    @commands.command(help='Unset the member channel')
    @commands.guild_only()
    @has_permissions(administrator=True)
    @commands.bot_has_permissions(send_messages=True)
    async def unsetmemberchannel(self, ctx):
        guild_state = self.bot.guild_state_map[ctx.guild.id]
        guild_state['id_member_channel'] = None
        conn = await self.bot.pool.acquire()
        try:
            sql = 'UPDATE guild SET id_member_channel=NULL WHERE id=$1'
            await conn.execute(sql, ctx.guild.id)
        finally:
            await self.bot.pool.release(conn)
        await CoroutineUtil.run(ctx.send('Member channel unset.'))

    @commands.command(help='Show bot settings')
    @commands.guild_only()
    @has_permissions(administrator=True)
    @commands.bot_has_permissions(send_messages=True)
    async def settings(self, ctx):
        guild_state = self.bot.guild_state_map[ctx.guild.id]
        mvp_channel = None
        mining_channel = None
        for channel_id in guild_state['channel_state_map']:
            if guild_state['channel_state_map'][channel_id]['type'] == TrackType.MVP:
                mvp_channel = next((x for x in ctx.guild.channels if x.id == channel_id), None)
            else:
                mining_channel = next((x for x in ctx.guild.channels if x.id == channel_id), None)
        member_channel = next((x for x in ctx.guild.channels if x.id == guild_state['id_member_channel']), None)
        msg = 'TalonRO MVP Times: :' + ('white_check_mark' if guild_state['talonro'] else 'x') + ':'
        msg += '\nMVP Channel: ' + ('' if mvp_channel is None else mvp_channel.mention)
        msg += '\nMining Channel: ' + ('' if mining_channel is None else mining_channel.mention)
        msg += '\nMember Channel: ' + ('' if member_channel is None else member_channel.mention)
        await CoroutineUtil.run(ctx.send(msg))

    @commands.command(help='List all guilds that have this bot')
    @commands.dm_only()
    @commands.is_owner()
    @commands.bot_has_permissions(send_messages=True)
    async def guilds(self, ctx):
        str = ''
        count = 0
        for guild in self.bot.guilds:
            str += '{0.name} ({0.id})\n'.format(guild)
            count += 1
            if count == 20:
                await CoroutineUtil.run(ctx.send(str))
                str = ''
                count = 0
        str += 'Total guilds: **{0}**'.format(len(self.bot.guilds))
        await CoroutineUtil.run(ctx.send(str))

    @commands.command(help='Send a direct message to each user who own a server that have this bot')
    @commands.dm_only()
    @commands.is_owner()
    @commands.bot_has_permissions(send_messages=True)
    async def notify(self, ctx, user_msg):
        users_id = set()
        for guild in self.bot.guilds:
            users_id.add(guild.owner_id)
        for user_id in users_id:
            user = await CoroutineUtil.run(self.bot.fetch_user(user_id))
            if user is not None:
                msg = 'You are receiving this message because you own a discord server that have this bot.'
                msg += '\n\n' + user_msg
                await CoroutineUtil.run(user.send(msg))

async def send_member_message(bot, guild, user, title, description):
    guild_state = bot.guild_state_map[guild.id]
    id_channel = guild_state['id_member_channel']
    if id_channel is None:
        return
    channel = next((x for x in guild.channels if x.id == id_channel), None)
    if channel is None:
        return
    embed = discord.Embed()
    embed.title = title
    embed.description = description
    embed.set_thumbnail(url=user.avatar_url)
    embed.set_author(icon_url=user.avatar_url, name='{0}'.format(user))
    embed.colour = discord.Colour.gold()
    embed.set_footer(text='User ID: {0.id}'.format(user))
    await CoroutineUtil.run(channel.send(embed=embed))

def setup(bot):
    bot.add_cog(Admin(bot))