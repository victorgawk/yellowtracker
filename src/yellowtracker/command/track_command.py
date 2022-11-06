from datetime import timedelta
import discord
from yellowtracker.domain.bot import Bot
from yellowtracker.domain.track_type import TrackType
from yellowtracker.util.coroutine_util import CoroutineUtil
from yellowtracker.util.date_util import DateUtil
from yellowtracker.service.track_service import TrackService
from yellowtracker.service.channel_service import ChannelService
from yellowtracker.service.entry_service import EntryService

class TrackCommand:

    @staticmethod
    async def track(interaction: discord.Interaction, bot: Bot, mvp: str, entryTime: str | None):
        validate_msg = ChannelService.validate_channel(bot, interaction.channel)
        if validate_msg is not None:
            await CoroutineUtil.run(interaction.response.send_message(validate_msg))
            return
        guild_state = bot.guild_state_map[interaction.guild_id]
        channel_state = guild_state['channel_state_map'].get(interaction.channel_id)
        if channel_state is None:
            await CoroutineUtil.run(interaction.response.send_message('This command can only be used in a track channel.'))
            return

        mins_ago = 0
        if entryTime is not None:
            if entryTime.isnumeric():
                mins_ago = int(entryTime)
            elif len(entryTime) == 5 and entryTime[2] == ':':
                hrs_mins = entryTime.split(':')
                if len(hrs_mins) == 2 and hrs_mins[0].isnumeric() and hrs_mins[1].isnumeric():
                    hh = int(hrs_mins[0])
                    mm = int(hrs_mins[1])
                    track_time = DateUtil.get_dt_now(bot.TIMEZONE)
                    if hh > track_time.hour or (hh == track_time.hour and mm > track_time.minute):
                        track_time -= timedelta(days=1)
                    track_time = track_time.replace(hour=hh, minute=mm)
                    td = DateUtil.get_dt_now(bot.TIMEZONE) - track_time
                    mins_ago = int(td / timedelta(minutes=1))
        if mins_ago < 0:
            mins_ago = 0

        type = channel_state['type']
        results = EntryService.find_entry(bot, mvp, type)

        if len(results) == 0:
            await CoroutineUtil.run(interaction.response.send_message(
                type.desc + ' "' + mvp + '" not found.'
            ))
        elif len(results) == 1:
            bot_reply_msg = await TrackService.update_track_time(bot, channel_state, results[0], mins_ago, interaction.user.id)
            await CoroutineUtil.run(interaction.response.send_message(
                bot_reply_msg
            ))
        else:
            bot_reply_msg = 'More than one ' + type.desc
            bot_reply_msg += ' starting with "' + mvp + '" has been found.\n'
            bot_reply_msg += '\n'
            bot_reply_msg += 'Select the ' + type.desc
            bot_reply_msg += ' that you want to track'
            if entryTime is not None:
                bot_reply_msg += ' with time ' + entryTime
            bot_reply_msg += ':'
            await CoroutineUtil.run(interaction.response.send_message(
                bot_reply_msg,
                view=TrackView(bot = bot, opts = results, mins_ago = mins_ago, track_type = type)
            ))

class TrackView(discord.ui.View):
    def __init__(self, *, timeout = 180, bot, opts, mins_ago, track_type):
        super().__init__(timeout = timeout)
        self.add_item(TrackSelect(bot, opts, mins_ago, track_type))

class TrackSelect(discord.ui.Select):
    def __init__(self, bot: Bot, opts, mins_ago, track_type):
        self.bot = bot
        self.opts = opts
        self.mins_ago = mins_ago
        self.track_type = track_type
        options = []
        for opt in self.opts:
            if track_type == TrackType.MVP:
                options.append(discord.SelectOption(label=opt["name"], description=opt["map"], value=opt["id"]))
            else:
                options.append(discord.SelectOption(label=opt["name"], value=opt["id"]))
        super().__init__(placeholder="Select an option",options=options)
    async def callback(self, interaction: discord.Interaction):
        entry = next((x for x in self.opts if str(x["id"]) == self.values[0]), None)
        guild_state = self.bot.guild_state_map.get(interaction.guild_id)
        if guild_state is None:
            return
        channel_state = guild_state['channel_state_map'].get(interaction.channel_id)
        bot_reply_msg = await TrackService.update_track_time(self.bot, channel_state, entry, self.mins_ago, interaction.user.id)
        await CoroutineUtil.run(interaction.response.edit_message(content=bot_reply_msg, view=None))
