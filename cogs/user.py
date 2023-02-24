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

    @app_commands.command(name="인벤토리", description="인벤토리를 불러옵니다")
    async def 인벤토리(self, interaction: discord.Interaction):
        with open('users.json') as f:
            data = json.load(f)

        if str(interaction.user.id) not in data:
            await interaction.response.send_message("등록되지 않은 유저입니다.")
            return
        user_data = data[str(interaction.user.id)]
        item_info = "".join([f"{key}: {value}\n" for key, value in user_data["item"].items()])
        embed = discord.Embed(title=f"{interaction.user.name}의 인벤토리", color=0x0aa40f)
        embed.set_author(name="치이", icon_url="https://i.imgur.com/7a4oeOi.jpg")
        embed.add_field(name="아이템 보유량", value=item_info)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="정보", description="유저 정보를 불러옵니다")
    async def 정보(self, interaction: discord.Interaction):
        with open('users.json') as f:
            data = json.load(f)

        if str(interaction.user.id) not in data:
            await interaction.response.send_message("등록되지 않은 유저입니다.")
            return
        user_data = data[str(interaction.user.id)]
        level_data = user_data['level']
        embed = discord.Embed(title=f"{interaction.user.name}의 프로필",description=f"Lv. {level_data['main']} \nExp: {level_data['xp']}/5000", color=0x0aa40f)
        embed.set_author(name="치이", icon_url="https://i.imgur.com/7a4oeOi.jpg")
        embed.add_field(name="호감도 레벨", value=f"랑이:{level_data['rangi']}\n 치이:{level_data['cheeyi']}\n세희:{level_data['saehee']}", inline=False)
        await interaction.response.send_message(embed=embed)



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