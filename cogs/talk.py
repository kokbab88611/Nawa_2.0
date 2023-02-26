import discord
from discord import app_commands
from discord.ext import commands
import pymongo
import json
import os
import random
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

all_hi = ["안녕", "어서와", "히사시부리", "하이", "반가워", "오랜만이야", "나 또 왔어", "올만", "또 보네", 
        "좋은 아침", "잘 잤어", "좋은 밤", "좋은 저녁", "좋은 점심", "여기야", "반갑다", 
        "돌아왔", "나 왔어", "나 왔", "갔다 왔어", "다녀왔"]

class Talk(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    commands.command()
    async def rangi_hi(ctx):
        await ctx.send()

    @commands.Cog.listener()
    async def on_message(self, message):
        contents = message.content.split(" ")
        if message.author.bot: 
            return None

        print("인사", any(x in all_hi for x in message.content))
        print("랑이", ("랑이야" in contents))

        if any(x in all_hi for x in message.content):
            print(message.content)
            await message.channel.send("안녕하느냐!")

async def setup(bot):
    await bot.add_cog(Talk(bot))
    
