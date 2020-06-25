import os
import discord
from discord.ext import commands

class Bot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pool = None
        self.config = {
            'bot_user_token': str(os.environ.get('BOT_USER_TOKEN')),
            'database_url': str(os.environ.get('DATABASE_URL')),
            'del_msg_after_secs': int(os.environ.get('DEL_MSG_AFTER_SECS')),
            'table_entry_expiration_mins': int(os.environ.get('TABLE_ENTRY_EXPIRATION_MINS')),
            'table_refresh_rate_secs': int(os.environ.get('TABLE_REFRESH_RATE_SECS')),
        }
        self.guild_state_map = {}
        self.stuff_loaded = False
        self.tz_str = 'Europe/Berlin'
        self.mvp_list = []
        self.mining_list = []