import os
import discord
from asyncpg.pool import Pool
from dotenv import load_dotenv

load_dotenv()

class Bot(discord.Client):

    BOT_USER_TOKEN = os.getenv("BOT_USER_TOKEN")
    DATABASE_URL = os.getenv("DATABASE_URL")
    DEL_MSG_AFTER_SECS = int(os.getenv("DEL_MSG_AFTER_SECS", default=10))
    TABLE_ENTRY_EXPIRATION_MINS = int(os.getenv("TABLE_ENTRY_EXPIRATION_MINS", default=20))
    TRACK_TIMER_DELAY_SECS = int(os.getenv("TRACK_TIMER_DELAY_SECS", default=5))
    EVENT_TIMER_DELAY_SECS = int(os.getenv("EVENT_TIMER_DELAY_SECS", default=5))
    TIMEZONE = os.getenv("TIMEZONE", default="PST8PDT")
    GUILD_ID = os.getenv("GUILD_ID")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pool: Pool | None = None
        self.guild_state_map = {}
        self.mvp_list = []
        self.mining_list = []
        self.race_time = None

    async def pool_acquire(self):
        if self.pool is None:
            raise Exception("Pool is None")
        return await self.pool.acquire()

    async def pool_release(self, conn):
        if self.pool is None:
            raise Exception("Pool is None")
        return await self.pool.release(conn)
