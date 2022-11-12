from datetime import datetime, timedelta
from yellowtracker.domain.bot import Bot
from yellowtracker.domain.track_type import TrackType
from yellowtracker.service.channel_service import ChannelService
from yellowtracker.util.track_util import TrackUtil

class TrackService:

    @staticmethod
    async def update_track_time(bot: Bot, channel_state: dict, entry, mins_ago: int, user_time: str | None, id_user: int):
        conn = await bot.pool_acquire()
        type = channel_state['type']
        date = datetime.now()
        track_time = date - timedelta(minutes=mins_ago)
        try:
            read_sql = f"SELECT * FROM {type.sql_desc}_guild WHERE id_{type.sql_desc}=$1 AND id_guild=$2"
            entry_guild_db = await conn.fetch(read_sql, entry['id'], channel_state['id_guild'])
            write_sql = f"INSERT INTO {type.sql_desc}_guild(id_{type.sql_desc},id_guild,track_time)VALUES($1,$2,$3)"
            if len(entry_guild_db) > 0:
                write_sql = f"UPDATE {type.sql_desc}_guild SET track_time=$3 WHERE id_{type.sql_desc}=$1 AND id_guild=$2"
            await conn.execute(write_sql, entry['id'], channel_state['id_guild'], track_time)

            read_sql = f"SELECT * FROM {type.sql_desc}_guild_log WHERE id_{type.sql_desc}=$1 AND id_guild=$2"
            entry_guild_log_db = await conn.fetch(read_sql, entry['id'], channel_state['id_guild'])
            write_sql = f"INSERT INTO {type.sql_desc}_guild_log(id_{type.sql_desc},id_guild,date,id_user)VALUES($1,$2,$3,$4)"
            if len(entry_guild_log_db) > 0:
                write_sql = f"UPDATE {type.sql_desc}_guild_log SET date=$3,id_user=$4 WHERE id_{type.sql_desc}=$1 AND id_guild=$2"
            await conn.execute(write_sql, entry['id'], channel_state['id_guild'], date, id_user)

            entry_log = None
            for x in channel_state['entry_log_list']:
                if x['entry'] == entry:
                    entry_log = x
                    break
            if entry_log is not None:
                channel_state['entry_log_list'].remove(entry_log)
            channel_state['entry_log_list'].appendleft({
                'entry': entry,
                'date': date,
                'id_user': id_user
            })
            while len(channel_state['entry_log_list']) > 3:
                entry_log_to_remove = channel_state['entry_log_list'].pop()
                del_sql = f"DELETE FROM {type.sql_desc}_guild_log WHERE id_{type.sql_desc}=$1 AND id_guild=$2"
                await conn.execute(del_sql, entry_log_to_remove['entry']['id'], channel_state['id_guild'])
        finally:
            await bot.pool_release(conn)
        entry_state = await TrackUtil.track_entry(bot, channel_state, entry, track_time)
        await ChannelService.update_channel_message(bot, channel_state)
        msg = entry_state['entry']['name']
        if type == TrackType.MVP:
            msg += ' (' 
            msg += entry_state['entry']['map']
            msg += ')'
        msg += ' in '
        msg += TrackUtil.fmt_r1_r2(int(entry_state['r1']))
        if type == TrackType.MVP:
            msg += ' to '
            msg += TrackUtil.fmt_r1_r2(int(entry_state['r2']))
        msg += ' minutes'
        if user_time is not None:
            msg += ' (time: ' + user_time + ')'
        msg += '.'
        return msg

