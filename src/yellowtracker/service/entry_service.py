
from yellowtracker.domain.bot import Bot
from yellowtracker.domain.track_type import TrackType
from yellowtracker.util.track_util import TrackUtil

class EntryService:

    @staticmethod
    async def load_db_entries(bot: Bot, conn, type: TrackType):
        db_entry_guild_list = await conn.fetch('SELECT * FROM ' + type.sql_desc + '_guild')
        entry_list = bot.mvp_list if type == TrackType.MVP else bot.mining_list
        for db_entry_guild in db_entry_guild_list:
            guild_state = bot.guild_state_map[db_entry_guild['id_guild']]
            if guild_state is None:
                continue
            entry = next(
                x for x in entry_list
                if x['id'] == db_entry_guild['id_' + type.sql_desc]
            )
            channel_state_map = guild_state['channel_state_map']
            channel_state = next(
                (
                    channel_state_map[x]
                    for x in channel_state_map
                    if channel_state_map[x]['type'] == type
                ),
                None
            )
            if channel_state is None:
                continue
            await TrackUtil.track_entry(bot, channel_state, entry, db_entry_guild['track_time'])
        await EntryService.load_db_entries_log(bot, conn, type)

    @staticmethod
    async def load_db_entries_log(bot: Bot, conn, type):
        sql = 'SELECT * FROM ' + type.sql_desc + '_guild_log ORDER BY date DESC'
        db_entry_log_list = await conn.fetch(sql)
        entry_list = bot.mvp_list if type == TrackType.MVP else bot.mining_list
        for db_entry_log in db_entry_log_list:
            guild_state = bot.guild_state_map[db_entry_log['id_guild']]
            if guild_state is None:
                continue
            entry = next(
                x for x in entry_list
                if x['id'] == db_entry_log['id_' + type.sql_desc]
            )
            channel_state_map = guild_state['channel_state_map']
            channel_state = next(
                (
                    channel_state_map[x]
                    for x in channel_state_map
                    if channel_state_map[x]['type'] == type
                ),
                None
            )
            if channel_state is None:
                continue
            if len(channel_state['entry_log_list']) < 3:
                channel_state['entry_log_list'].append({
                    'entry': entry,
                    'date': db_entry_log['date'],
                    'id_user': db_entry_log['id_user']
                })
            else:
                entry_state = next((x for x in channel_state['entry_state_list'] if x['entry'] == entry), None)
                if entry_state is not None:
                    rtime = entry_state['r2'] if type == TrackType.MVP else entry_state['r1']
                    if rtime <= -bot.TABLE_ENTRY_EXPIRATION_MINS:
                        delete_sql = 'DELETE FROM ' + type.sql_desc + '_guild'
                        delete_sql += ' WHERE id_guild=$1'
                        delete_sql += ' AND id_' + type.sql_desc + '=$2'
                        await conn.execute(
                            delete_sql,
                            db_entry_log['id_guild'],
                            db_entry_log['id_' + type.sql_desc]
                        )

    @staticmethod
    def find_entry(bot, query, type):
        entry_list = bot.mvp_list if type == TrackType.MVP else bot.mining_list
        results = []
        for entry in entry_list:
            compare = entry['name']
            if type == TrackType.MVP:
                compare += ' ' + entry['map']
            if compare.lower() == query.lower():
                if entry not in results:
                    results.append(entry)
                return results
            if compare.lower().startswith(query.lower()):
                if entry not in results:
                    results.append(entry)
            for alias in entry['alias']:
                compare = alias
                if type == TrackType.MVP:
                    compare += ' ' + entry['map']
                if compare.lower() == query.lower():
                    if entry not in results:
                        results.append(entry)
                    return results
                if compare.lower().startswith(query.lower()):
                    if entry not in results:
                        results.append(entry)
        return results
