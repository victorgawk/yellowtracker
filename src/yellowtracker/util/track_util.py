from datetime import datetime
from yellowtracker.domain.track_type import TrackType

class TrackUtil:

    @staticmethod
    async def track_entry(bot, channel_state, entry, track_time):
        type = channel_state['type']
        entry_state = next((x for x in channel_state['entry_state_list'] if x['entry'] == entry), None)   
        if entry_state is None:
            entry_state = {}
            entry_state['entry'] = entry
            entry_state['r1'] = -999
            if type == TrackType.MVP:
                entry_state['r2'] = -999
            channel_state['entry_state_list'].append(entry_state)
        entry_state['t1'] = entry['t1']
        if type == TrackType.MVP:
            entry_state['t2'] = entry['t2']
            if bot.guild_state_map[channel_state['id_guild']]['custom'] and entry['t1custom'] is not None:
                entry_state['t1'] = entry['t1custom']
                entry_state['t2'] = entry['t2custom']
        entry_state['track_time'] = track_time
        TrackUtil.calc_remaining_time(entry_state, track_time, type)
        channel_state['entry_state_list'].sort(key=lambda e : e['r1'])
        return entry_state

    @staticmethod
    def calc_remaining_time(entry_state, track_time, type):
        mins_ago = round((datetime.now() - track_time).total_seconds() / 60)
        entry_state['r1'] = entry_state['t1'] - mins_ago
        if type == TrackType.MVP:
            entry_state['r2'] = entry_state['t2'] - mins_ago

    @staticmethod
    def fmt_r1_r2(val: int):
        return str(val) if val > 0 else '**' + str(val) + '**'

    @staticmethod
    def fmt_column(values):
        result = ''
        for value in values:
            if result != '':
                result += '\n'
            result += value
        return result
