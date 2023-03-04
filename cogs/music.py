import discord
from discord import app_commands
from discord.ext import commands
import os
import random
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

class Music(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    

async def setup(bot):
    await bot.add_cog(Music(bot))
    
