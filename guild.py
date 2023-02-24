import discord
from discord import app_commands
from discord.ext import commands
import pymongo
import json
import os
import random
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
class GuildData(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("준비됨")
        

async def setup(bot):
    await bot.add_cog(GuildData(bot))
    