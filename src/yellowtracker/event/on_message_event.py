import logging
import discord
import time
from yellowtracker.domain.bot import Bot
from yellowtracker.domain.track_type import TrackType
from yellowtracker.service.channel_service import ChannelService
from yellowtracker.util.coroutine_util import CoroutineUtil
from yellowtracker.util.track_util import TrackUtil

log = logging.getLogger(__name__)

class OnMessageEvent:

    @staticmethod
    async def on_message(bot: Bot, tree: discord.app_commands.CommandTree, message: discord.Message):
        if not OnMessageEvent.validate_message(bot, message):
            return
        args = message.content.split(" ", 1)
        if args[0] == "!guilds":
            await OnMessageEvent.guilds(bot, message.channel)
        if args[0] == "!notify":
            if (len(args)) < 2:
                return
            await OnMessageEvent.notify(bot, message.channel, args[1])
        if args[0] == "!sync":
            await OnMessageEvent.sync(bot, tree, message.channel)
        if args[0] == "!channels":
            await OnMessageEvent.channels(bot, message.channel)

    @staticmethod
    async def guilds(bot: Bot, dm_channel: discord.abc.Messageable):
        lines = []
        for guild in bot.guilds:
            owner = None
            if guild.owner_id is not None:
                owner = await CoroutineUtil.run(guild.fetch_member(guild.owner_id))
            lines.append(f"{guild.name} | {owner} | {guild.id}")
        title = "Guilds"
        header = "Name | Owner | ID"
        await OnMessageEvent.send_msg_paginated(bot, dm_channel, title, header, lines)

    @staticmethod
    async def notify(bot: Bot, dm_channel: discord.abc.Messageable, user_msg: str):
        users_id = set()
        count = 0
        for guild in bot.guilds:
            users_id.add(guild.owner_id)
        for user_id in users_id:
            user = await CoroutineUtil.run(bot.fetch_user(user_id))
            if user is not None:
                msg = "You are receiving this message because you own a discord server that have this bot."
                msg += "\n\n"
                msg += user_msg
                await CoroutineUtil.run(user.send(msg))
                count += 1
        await CoroutineUtil.run(dm_channel.send(f"Notification sent to {count} users."))

    @staticmethod
    async def sync(bot: Bot, tree: discord.app_commands.CommandTree, dm_channel: discord.abc.Messageable):
        ts = time.time()
        await CoroutineUtil.run(dm_channel.send(f"Begin sync slash commands with {len(bot.guilds)} guilds."))
        for guild in bot.guilds:
            tree.copy_global_to(guild=guild)
            await CoroutineUtil.run(tree.sync(guild=guild))
        await CoroutineUtil.run(dm_channel.send(f"Slash commands synced with {len(bot.guilds)} guilds in {int(time.time() - ts)} secs."))

    @staticmethod
    async def channels(bot: Bot, dm_channel: discord.abc.Messageable):
        lines = []
        for guild in bot.guilds:
            guild_state = bot.guild_state_map.get(guild.id)
            if guild_state is None:
                continue
            for id_channel in guild_state['channel_state_map'].copy():
                channel_state = guild_state['channel_state_map'].get(id_channel)
                if channel_state is None:
                    continue
                if len(channel_state['entry_state_list']) > 0:
                    owner = None
                    if guild.owner_id is not None:
                        owner = await CoroutineUtil.run(guild.fetch_member(guild.owner_id))
                    if owner is None:
                        continue
                    channel = ChannelService.get_channel_from_guild(guild, channel_state['id_channel'])
                    if channel is None:
                        continue
                    line = f"{channel} | "
                    line += f"{channel_state['type'].sql_desc} | "
                    line += f"{guild} | "
                    line += f"{owner} | "
                    line += f"{'Yes' if guild_state['custom'] else 'No'} | "
                    line += f"{'Yes' if guild_state['mobile'] else 'No'} | "
                    line += f"{len(channel_state['entry_state_list'])}"
                    lines.append(line)
        title = "Channels"
        header = "Channel | Type | Guild | Owner | Custom | Mobile | Entries"
        await OnMessageEvent.send_msg_paginated(bot, dm_channel, title, header, lines)

    @staticmethod
    async def send_msg_paginated(bot: Bot, dm_channel: discord.abc.Messageable, title: str, header: str, lines: list[str]):
        if lines == 0:
            embed = discord.Embed(color=discord.Colour.gold(), title=title)
            embed.add_field(name=header, value="Empty", inline=False)
            await CoroutineUtil.run(dm_channel.send(embed=embed))
            return
        page_size = 10
        msg = ""
        offset = 1
        count = 0
        for line in lines:
            msg += f"{line}\n"
            count += 1
            if count == page_size:
                embed = discord.Embed(color=discord.Colour.gold(), title=title)
                embed.add_field(name=header, value=msg, inline=False)
                embed.set_footer(text=f"{offset} to {offset + count - 1} (Total: {len(lines)})")
                await CoroutineUtil.run(dm_channel.send(embed=embed))
                msg = ""
                offset = offset + count
                count = 0
        if count > 0:
            embed = discord.Embed(color=discord.Colour.gold(), title=title)
            embed.add_field(name=header, value=msg, inline=False)
            embed.set_footer(text=f"{offset} to {offset + count - 1} (Total: {len(lines)})")
            await CoroutineUtil.run(dm_channel.send(embed=embed))

    @staticmethod
    def validate_message(bot: Bot, message: discord.Message) -> bool:
        if not message.content.startswith("!"):
            return False
        if type(message.channel) != discord.DMChannel:
            return False
        if bot.application is None:
            return False
        bot_owner = bot.application.owner
        if bot_owner is None:
            return False
        if bot_owner.id != message.author.id:
            return False
        return True
