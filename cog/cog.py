import discord
import asyncio
from discord.ext import commands

class Cog(commands.Cog):
    async def wait_load_stuff(self):
        while not self.bot.stuff_loaded:
            await asyncio.sleep(1)