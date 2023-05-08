import os
import discord
import asyncio
import logging
from yellowtracker.command.clean_command import CleanCommand
from yellowtracker.command.custom_command import CustomCommand
from yellowtracker.command.mobile_command import MobileCommand
from yellowtracker.command.setminingchannel_command import SetMiningChannelCommand
from yellowtracker.command.setmvpchannel_command import SetMvpChannelCommand
from yellowtracker.command.settings_command import SettingsCommand
from yellowtracker.command.track_command import TrackCommand
from yellowtracker.command.timezone_command import TimezoneCommand
from yellowtracker.command.unsetminingchannel_command import UnsetMiningChannelCommand
from yellowtracker.command.unsetmvpchannel_command import UnsetMvpChannelCommand
from yellowtracker.command.unsettimezone_command import UnsetTimezoneCommand
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
from yellowtracker.util.coroutine_util import CoroutineUtil

bot = Bot(intents=discord.Intents.default())
tree = discord.app_commands.CommandTree(bot)
discord.utils.setup_logging()
log = logging.getLogger(__name__)

@tree.command(description = "Remove all tracked MVPs from the list")
async def clean(interaction: discord.Interaction):
    await CleanCommand.clean(interaction = interaction, bot = bot)

@tree.command(description = "Enable/disable custom MVP respawn times")
async def custom(interaction: discord.Interaction):
    await CustomCommand.custom_cmd(interaction = interaction, bot = bot)

@tree.command(description = "Define a custom timezone for MVP tracking")
async def timezone(interaction: discord.Interaction, timezone: str):
    await TimezoneCommand.timezone_cmd(interaction = interaction, bot = bot, timezone = timezone)

@tree.command(description = "Undo custom timezone definition")
async def unsettimezone(interaction: discord.Interaction):
    await UnsetTimezoneCommand.unsettimezone_cmd(interaction = interaction, bot = bot)

@tree.command(description = "Enable/disable MVP list mobile layout")
async def mobile(interaction: discord.Interaction):
    await MobileCommand.mobile(interaction = interaction, bot = bot)

@tree.command(description = "Define a channel to track mining locations")
async def setminingchannel(interaction: discord.Interaction):
    await SetMiningChannelCommand.setminingchannel(interaction = interaction, bot = bot)

@tree.command(description = "Define a channel to track MVPs")
async def setmvpchannel(interaction: discord.Interaction):
    await SetMvpChannelCommand.setmvpchannel(interaction = interaction, bot = bot)

@tree.command(description = "Show bot settings")
async def settings(interaction: discord.Interaction):
    await SettingsCommand.settings(interaction = interaction, bot = bot)

@tree.command(description = "Track a MVP that has been defeated")
async def track(interaction: discord.Interaction, mvp: str, time: str = None):
    await TrackCommand.track(interaction = interaction, bot = bot, mvp = mvp, user_time = time)

@tree.command(description = "Undo MVP track channel definition")
async def unsetminingchannel(interaction: discord.Interaction):
    await UnsetMiningChannelCommand.unsetminingchannel(interaction = interaction, bot = bot)

@tree.command(description = "Undo MVP track channel definition")
async def unsetmvpchannel(interaction: discord.Interaction):
    await UnsetMvpChannelCommand.unsetmvpchannel(interaction = interaction, bot = bot)

@tree.command(description = "Show War of Emperium times")
async def woe(interaction: discord.Interaction):
    await WoeCommand.woe(interaction = interaction, bot = bot)

@tree.command(description = "Show GM Challenge times")
async def gmc(interaction: discord.Interaction):
    await GmcCommand.gmc(interaction = interaction, bot = bot)

@tree.command(description = "Show BG Happy Hour times")
async def hh(interaction: discord.Interaction):
    await HhCommand.hh(interaction = interaction, bot = bot)

@bot.event
async def on_ready():
    await OnReadyEvent.on_ready(bot = bot, tree = tree)

@bot.event
async def on_message(message):
    await OnMessageEvent.on_message(message = message, tree = tree, bot = bot)

@bot.event
async def on_guild_join(guild):
    await OnGuildJoinEvent.on_guild_join(guild = guild, tree = tree, bot = bot)

@bot.event
async def on_guild_remove(guild):
    await OnGuildRemoveEvent.on_guild_remove(guild = guild, bot = bot)

async def run_bot(bot: Bot) -> None:
    log.info("Start bot client.")
    if bot.BOT_USER_TOKEN is None:
        raise Exception("Bot token is missing")
    await bot.start(bot.BOT_USER_TOKEN)

async def run_timer(bot: Bot) -> None:
    log.info("Start timer.")
    while True:
        await CoroutineUtil.run(EventTimer.timer(bot))
        await CoroutineUtil.run(TrackTimer.timer(bot))
        await CoroutineUtil.run(asyncio.sleep(bot.TIMER_DELAY_SECS))

async def main():
    return await asyncio.gather(run_bot(bot), run_timer(bot))

loop = asyncio.new_event_loop()
loop.create_task(main())

try:
    loop.run_forever()
except KeyboardInterrupt:
    os._exit(42)
