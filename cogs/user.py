import discord
from discord import app_commands
from discord.ext import commands
import pymongo
import urllib.parse
import json
import os
import asyncio
import random


class User(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        with open(os.path.join(os.getcwd(), 'users.json')) as f:
            self.userData = json.load(f)

    @commands.Cog.listener()
    async def on_ready(self):
        print("준비됨")

    @commands.command(name="핑")
    async def ping(self, ctx):
        await ctx.send("퐁이니라!")

    @commands.command(name="아", pass_context=True)
    async def 아(self, ctx):
        await self.saveUser(ctx)

    @commands.command(name="인벤", pass_context=True)
    async def 인벤(self, ctx):
        with open('users.json') as f:
            data = json.load(f)
            if str(ctx.author.id) not in data:
                await ctx.send("등록되지 않은 유저입니다")
                return
            user_data=data[str(ctx.author.id)]
            await ctx.send(f"{user_data}")
    """
    @app_commands.command(name="인벤토리", description="인벤토리를 불러옵니다")
    async def 인벤토리(self,interaction:discord.Interaction):
        with open('users.json') as f:
            data = json.load(f)

        embed = discord.Embed(title="인벤토리", color=0x0aa40f)
        embed.set_author(name="치이", icon_url="https://i.imgur.com/7a4oeOi.jpg")
        embed.add_field(name="호감도 레벨", value="테스트3,테스트4", inline=False)
        embed.add_field(name="기타", value="테스트1, 테스트2", inline=False)
        embed.set_footer(text="연관 검색어 결과는 위와 같습니다.")
        """



    async def saveUser(self, ctx):
        await ctx.invoke(self.bot.get_command('핑'))

        with open(os.path.join(os.getcwd(), 'users.json'),'r+') as f:
            data = json.load(f)
            if str(ctx.author.id) not in data:
                data[ctx.author.id] = \
                    {
                        "level": {
                            "main": 1,
                            "xp": 0,
                            "rangi": 0,
                            "cheeyi": 0,
                            "saehee": 0
                        },
                        "money": 0,
                        "item": {
                            "a": 1,
                            "b": 0,
                            "c": 99
                        },
                        "attendence": False
                    }


            else:
                #random_xp = random.randint(1, 2)
                #self.userData[ctx.author.id]["level"]["xp"] += random_xp
                print("벌써 존재하는 유저입니다")
                #if self.level_up(ctx.author.id):
                    #await ctx.send("레벨업{}".format(self.userData[ctx.author.id]["level"]["xp"]))
        with open(os.path.join(os.getcwd(), 'users.json'),'w+') as f:
            json.dump(data, f, indent=4)


async def setup(bot):
    await bot.add_cog(User(bot))