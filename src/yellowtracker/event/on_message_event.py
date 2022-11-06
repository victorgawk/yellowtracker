import discord
from yellowtracker.domain.bot import Bot
from yellowtracker.util.coroutine_util import CoroutineUtil

class OnMessageEvent:

    @staticmethod
    async def on_message(bot: Bot, message: discord.Message):
        if not OnMessageEvent.validate(bot, message):
            return
        args = message.content.split(" ", 1)
        if args[0] == "!guilds":
            await OnMessageEvent.guilds(bot, message.channel)
        if args[0] == "!notify":
            if (len(args)) < 2:
                return
            await OnMessageEvent.notify(bot, message.channel, args[1])

    @staticmethod
    async def guilds(bot: Bot, channel: discord.abc.Messageable):
        page_size = 20
        guilds = ""
        offset = 1
        count = 0
        for guild in bot.guilds:
            owner = None
            if guild.owner_id is not None:
                owner = await CoroutineUtil.run(guild.fetch_member(guild.owner_id))
            guilds += f"{guild.name} | {owner} | {guild.id}\n"
            count += 1
            if count == page_size:
                await OnMessageEvent.send_guilds_partial_msg(bot, channel, offset, count, guilds)
                guilds = ""
                offset = offset + count
                count = 0
        if count > 0:
            await OnMessageEvent.send_guilds_partial_msg(bot, channel, offset, count, guilds)

    @staticmethod
    async def notify(bot: Bot, channel: discord.abc.Messageable, user_msg: str):
        users_id = set()
        for guild in bot.guilds:
            users_id.add(guild.owner_id)
        for user_id in users_id:
            user = await CoroutineUtil.run(bot.fetch_user(user_id))
            if user is not None:
                msg = "You are receiving this message because you own a discord server that have this bot."
                msg += "\n\n"
                msg += user_msg
                await CoroutineUtil.run(user.send(msg))

    @staticmethod
    async def send_guilds_partial_msg(bot: Bot, channel: discord.abc.Messageable, offset: int, count: int, guilds: str):
        embed = discord.Embed()
        embed.title = "Guilds"
        embed.colour = discord.Colour.gold()
        embed.add_field(name="Name | Owner | ID", value=guilds, inline=False)
        embed.set_footer(text=f"{offset} to {offset + count - 1} (Total: {len(bot.guilds)})")
        await CoroutineUtil.run(channel.send(embed=embed))

    @staticmethod
    def validate(bot: Bot, message: discord.Message) -> bool:
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
