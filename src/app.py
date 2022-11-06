import os
import discord
import asyncio
import logging
import tornado.web
from yellowtracker.command.clean_command import CleanCommand
from yellowtracker.command.custom_command import CustomCommand
from yellowtracker.command.mobile_command import MobileCommand
from yellowtracker.command.setminingchannel_command import SetMiningChannelCommand
from yellowtracker.command.setmvpchannel_command import SetMvpChannelCommand
from yellowtracker.command.settings_command import SettingsCommand
from yellowtracker.command.track_command import TrackCommand
from yellowtracker.command.unsetminingchannel_command import UnsetMiningChannelCommand
from yellowtracker.command.unsetmvpchannel_command import UnsetMvpChannelCommand
from yellowtracker.command.woe_command import WoeCommand
from yellowtracker.command.hh_command import HhCommand
from yellowtracker.command.gmc_command import GmcCommand
from yellowtracker.domain.bot import Bot
from yellowtracker.event.on_guild_join_event import OnGuildJoinEvent
from yellowtracker.event.on_guild_remove_event import OnGuildRemoveEvent
from yellowtracker.event.on_message_event import OnMessageEvent
from yellowtracker.event.on_ready_event import OnReadyEvent
from yellowtracker.timer.event_timer import EventTimer
from yellowtracker.timer.track_timer import TrackTimer

discord.utils.setup_logging()
log = logging.getLogger(__name__)
bot = Bot(intents=discord.Intents.default())
tree = discord.app_commands.CommandTree(bot)
guild = None if bot.GUILD_ID is None else discord.Object(id=int(bot.GUILD_ID))

@tree.command(description = "Remove all tracked MVPs from the list", guild = guild)
async def clean(interaction: discord.Interaction):
    await CleanCommand.clean(interaction = interaction, bot = bot)

@tree.command(description = "Enable/disable custom MVP respawn times", guild = guild)
async def custom(interaction: discord.Interaction):
    await CustomCommand.custom(interaction = interaction, bot = bot)

@tree.command(description = "Enable/disable MVP list mobile layout", guild = guild)
async def mobile(interaction: discord.Interaction):
    await MobileCommand.mobile(interaction = interaction, bot = bot)

@tree.command(description = "Define a channel to track mining locations", guild = guild)
async def setminingchannel(interaction: discord.Interaction):
    await SetMiningChannelCommand.setminingchannel(interaction = interaction, bot = bot)

@tree.command(description = "Define a channel to track MVPs", guild = guild)
async def setmvpchannel(interaction: discord.Interaction):
    await SetMvpChannelCommand.setmvpchannel(interaction = interaction, bot = bot)

@tree.command(description = "Show bot settings", guild = guild)
async def settings(interaction: discord.Interaction):
    await SettingsCommand.settings(interaction = interaction, bot = bot)

@tree.command(description = "Track a MVP that has been defeated", guild = guild)
async def track(interaction: discord.Interaction, mvp: str, time: str | None = None):
    await TrackCommand.track(interaction = interaction, bot = bot, mvp = mvp, entryTime = time)

@tree.command(description = "Undo MVP track channel definition", guild = guild)
async def unsetminingchannel(interaction: discord.Interaction):
    await UnsetMiningChannelCommand.unsetminingchannel(interaction = interaction, bot = bot)

@tree.command(description = "Undo MVP track channel definition", guild = guild)
async def unsetmvpchannel(interaction: discord.Interaction):
    await UnsetMvpChannelCommand.unsetmvpchannel(interaction = interaction, bot = bot)

@tree.command(description = "Show War of Emperium times", guild = guild)
async def woe(interaction: discord.Interaction):
    await WoeCommand.woe(interaction = interaction, bot = bot)

@tree.command(description = "Show GM Challenge times", guild = guild)
async def gmc(interaction: discord.Interaction):
    await GmcCommand.gmc(interaction = interaction, bot = bot)

@tree.command(description = "Show BG Happy Hour times", guild = guild)
async def hh(interaction: discord.Interaction):
    await HhCommand.hh(interaction = interaction, bot = bot)

@bot.event
async def on_ready():
    await OnReadyEvent.on_ready(bot = bot, tree = tree, guild = guild)

@bot.event
async def on_message(message):
    await OnMessageEvent.on_message(message = message, bot = bot)

@bot.event
async def on_guild_join(guild):
    await OnGuildJoinEvent.on_guild_join(guild = guild, bot = bot)

@bot.event
async def on_guild_remove(guild):
    await OnGuildRemoveEvent.on_guild_remove(guild = guild, bot = bot)

async def run_bot(bot: Bot) -> None:
    log.info("Starting bot.")
    if bot.BOT_USER_TOKEN is None:
        raise Exception("Bot token is missing")
    await bot.start(bot.BOT_USER_TOKEN)

async def health_check_http_server() -> None:
    port = 8080
    log.info(f"Starting health check HTTP server on port {port}.")
    class MainHandler(tornado.web.RequestHandler):
        def get(self):
            self.write("It works")
    app = tornado.web.Application([(r"/", MainHandler)])
    app.listen(port)
    await asyncio.Event().wait()

async def main():
    return await asyncio.gather(run_bot(bot), health_check_http_server(), TrackTimer.timer(bot), EventTimer.timer(bot))

loop = asyncio.new_event_loop()
loop.create_task(main())

try:
    loop.run_forever()
except KeyboardInterrupt:
    os._exit(42)
