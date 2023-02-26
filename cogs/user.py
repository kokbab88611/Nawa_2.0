import discord
from discord import app_commands
from discord.ext import commands, tasks
import pymongo
import json
import os
import random
list_dev_id = ["339767912841871360", "474389454262370314", "393932860597338123", "185181025104560128"]
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
class UserData(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.data = self.get_json()
        print(self.data)
        self.repeat_save_user.start()

    @commands.Cog.listener()
    async def on_ready(self):
        print("준비됨")

    def set_json(self):
        try:
            with open(os.path.join(__location__ + '\\json\\users.json'), "w") as file:
                print(self.data)
                file.write(json.dump(self.data, file, indent=4))
        except TypeError:
            pass

    def get_json(self):
        with open(os.path.join(f"{__location__}\\json\\users.json"),'r',encoding='utf-8') as file:
            print("저장됨")
            return json.load(file)

    def check_user(self, user_id: str):
        if str(user_id) not in self.data:
            self.data[user_id] = {
                    "level": {
                        "main": 1,
                        "xp": 0,
                        "rangi": 0,
                        "cheeyi": 0,
                        "saehee": 0
                    },
                    "money": 30000,
                    "item": {
                        "a": 1,
                        "b": 0,
                        "c": 99
                    },
                    "attendence": False
                }
            print("유저 없었어")
        else:
            pass

    def level_up(self, user_id: str):
            current_xp = self.data[user_id]["level"]["xp"]
            current_lvl = self.data[user_id]["level"]["main"]

            if current_xp >= round(0.04 * (current_lvl ** 3) + 0.8 * (current_lvl ** 2) + 2 * current_lvl):
                return True

            return False
    
    async def give_money(self, money: int, user: discord.Member = "다"):
        if user == None:
            pass

    async def give_xp(self, ctx):
        #await ctx.invoke(self.bot.get_command('핑'))
        self.check_user(str(ctx.author.id))
        random_xp = random.randint(1, 2)
        self.data[str(ctx.author.id)]["level"]["xp"] += random_xp
        if self.level_up(str(ctx.author.id)):
            self.data[str(ctx.author.id)]["level"]["main"] += 1
            await ctx.send(f"레벨업{self.data[str(ctx.author.id)]['level']['main']}")   

    @commands.command(name=";지급", pass_context=True)
    async def give_money(self, ctx, user, money: int):
        if str(ctx.author.id) in list_dev_id:
            if user == "전체":
                for x in self.data.items():
                    self.data[x[0]]["money"] += money
            else:  
                self.check_user(str(ctx.author.id))
                self.data[str(user)]["money"] += money
        else:
            pass
    @commands.command(name=";징수", pass_context=True)
    async def take_money(self, ctx, user, money: int):
        if str(ctx.author.id) in list_dev_id:
            if user == "전체":
                for x in self.data.items():
                    self.data[x[0]]["money"] -= money
            else:  
                self.check_user(str(ctx.author.id))
                self.data[str(user)]["money"] -= money
        else:
            pass

    @commands.command(name="핑")
    async def ping(self, ctx):
        await ctx.send("퐁이니라!")

    @commands.command(name="아", pass_context=True)
    async def test(self, ctx):
        await self.give_xp(ctx)

    @commands.command(name="인벤", pass_context=True)
    async def inven(self, ctx):
        self.check_user()
        user_data=self.data[str(ctx.author.id)]
        await ctx.send(f"{user_data}")

    @app_commands.command(name="인벤토리", description="인벤토리를 불러옵니다")
    async def inventory(self, interaction: discord.Interaction):
        self.check_user(str(interaction.user.id))
        user_data = self.data[str(interaction.user.id)]
        item_info = "".join([f"{key}: {value}\n" for key, value in user_data["item"].items()])
        embed = discord.Embed(title=f"{interaction.user.name}의 인벤토리", color=0x0aa40f)
        embed.set_author(name="치이", icon_url="https://i.imgur.com/7a4oeOi.jpg")
        embed.add_field(name="아이템 보유량", value=item_info)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="정보", description="유저 정보를 불러옵니다")
    async def user_information(self, interaction: discord.Interaction):
        self.check_user(str(interaction.user.id))
        with open('users.json') as f:
            data = json.load(f)

        if str(interaction.user.id) not in self.data:
            await interaction.response.send_message("등록되지 않은 유저입니다.")
            return
        user_data = self.data[str(interaction.user.id)]
        level_data = user_data['level']
        embed = discord.Embed(title=f"{interaction.user.name}의 프로필",description=f"Lv. {level_data['main']} \nExp: {level_data['xp']}/5000", color=0x0aa40f)
        embed.set_author(name="치이", icon_url="https://i.imgur.com/7a4oeOi.jpg")
        embed.add_field(name="호감도 레벨", value=f"랑이:{level_data['rangi']}\n 치이:{level_data['cheeyi']}\n세희:{level_data['saehee']}", inline=False)
        await interaction.response.send_message(embed=embed)



    @commands.Cog.listener()
    async def on_disconnect(self):
        self.set_json()

    @tasks.loop(seconds=30)
    async def repeat_save_user(self):
        self.set_json()
        self.get_json()
        print("저장됨")

async def setup(bot):
    await bot.add_cog(UserData(bot))
    
