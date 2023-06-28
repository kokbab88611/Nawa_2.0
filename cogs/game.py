import discord,random,string,array,time
import asyncio
from discord import app_commands,Interaction,Reaction,InteractionResponse
from discord.ui import Button, View
from discord.ext import commands, tasks
import random
import os
import PIL
from PIL import Image, ImageFont, ImageDraw
import datetime

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

ZodiacDict = {
    "호랑이":"",
    "토끼":"",
    "용":"",
    "뱀":"",
    "말":"",
    "양":"",
    "원숭이":"",
    "닭":"",
    "개":"",
    "돼지":"",
    "쥐":"",
    "소":"",
}

MemoryGameDict = {1:"<:aya:1122868308144828438>",
2:"<:baduk:1122868299663941783>",
3:"<:chie:1122868288616157214>",
4:"<:gahi:1122868284077903932>",
5:"<:nyangi:1122868279225090149>",
6:"<:rangi:1122868296832782396>",
7:"<:seongi:1122868304210558996>",
8:"<:yeorin:1122868292625895606>"}

class MemoryGameVars():
    def __init__(self):
        self.tries = 0
        self.cards = [f"{MemoryGameDict[1]}", 
        f"{MemoryGameDict[1]}", 
        f"{MemoryGameDict[2]}", 
        f"{MemoryGameDict[2]}", 
        f"{MemoryGameDict[3]}", 
        f"{MemoryGameDict[3]}", 
        f"{MemoryGameDict[4]}", 
        f"{MemoryGameDict[4]}", 
        f"{MemoryGameDict[5]}", 
        f"{MemoryGameDict[5]}", 
        f"{MemoryGameDict[6]}", 
        f"{MemoryGameDict[6]}", 
        f"{MemoryGameDict[7]}", 
        f"{MemoryGameDict[7]}", 
        f"{MemoryGameDict[8]}", 
        f"{MemoryGameDict[8]}"]
        self.cards = random.sample(self.cards, len(self.cards))
        self.cards_dis = ["⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜"]

class MemoryGameDropDown(discord.ui.Select):
    def __init__(self, variables, command_userid):
        self.variables = variables
        self.command_userid = command_userid
        options = [
            discord.SelectOption(
                label="A1", value=0),
            discord.SelectOption(
                label="A2", value=1),
            discord.SelectOption(
                label="A3", value=2),
            discord.SelectOption(
                label="A4", value=3),
            discord.SelectOption(
                label="B1", value=4),
            discord.SelectOption(
                label="B2", value=5),
            discord.SelectOption(
                label="B3", value=6),
            discord.SelectOption(
                label="B4", value=7),
            discord.SelectOption(
                label="C1", value=8),
            discord.SelectOption(
                label="C2", value=9),
            discord.SelectOption(
                label="C3", value=10),
            discord.SelectOption(
                label="C4", value=11),
            discord.SelectOption(
                label="D1", value=12),
            discord.SelectOption(
                label="D2", value=13),
            discord.SelectOption(
                label="D3", value=14),
            discord.SelectOption(
                label="D4", value=15),
        ]

        super().__init__(placeholder="원하시는 카드를 선택하십시오", options=options, min_values=2, max_values=2)

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id == self.command_userid:
            lst = []
            for i in range(len(self.variables.cards_dis)):
                if self.variables.cards_dis[i] != "⬜":
                    if self.variables.cards_dis[i] in lst:
                        lst.remove(self.variables.cards_dis[i])
                    else:
                        lst.append(self.variables.cards_dis[i])
            for i in lst:
                self.variables.cards_dis[self.variables.cards_dis.index(i)] = "⬜"

            if self.variables.cards_dis[int(self.values[0])] == "⬜" and self.variables.cards_dis[int(self.values[1])] == "⬜":
                self.variables.tries += 1
                self.variables.cards_dis[int(self.values[0])], self.variables.cards_dis[int(self.values[1])] = self.variables.cards[int(self.values[0])], self.variables.cards[int(self.values[1])]

                if "⬜" in self.variables.cards_dis:
                    base=Game.MemoryGameGrid(self.variables.cards_dis)
                    embed = discord.Embed(
                            title="카드 짝 맞추기",
                            description=base)
                    view = MemoryGameView(self.variables, self.command_userid)
                    await interaction.response.edit_message(content="", view=view, embed=embed)
                else:
                    base = f"소요 횟수: {self.variables.tries}"
                    embed = discord.Embed(
                            title="카드 짝 맞추기",
                            description=base)
                    await interaction.response.edit_message(content="", embed=embed, view=None)
            else:
                base=Game.MemoryGameGrid(self.variables.cards_dis)
                embed = discord.Embed(
                        title="카드 짝 맞추기",
                        description=base)
                view = MemoryGameView(self.variables, self.command_userid)
                await interaction.response.edit_message(content="이미 뒤집힌 카드는 선택할 수 없습니다", view=view, embed=embed)
        else:
            await interaction.response.send_message(content="타인의 게임에 관여할 수 없습니다", ephemeral=True)

class MemoryGameView(discord.ui.View):
    def __init__(self, variables, command_userid):
        super().__init__()
        self.add_item(MemoryGameDropDown(variables, command_userid))

class Game(commands.Cog):
    channel_id:string
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("준비됨")

    @app_commands.command(name="추첨", description="추첨기를 생성합니다")
    async def raname(self, interaction: discord.Interaction, people: str, join: int = 1):
        if people:
            arr = people.split(",")
            if len(arr) < join:
                await interaction.response.send_message("참가자가 충분하지 않습니다!")
                return
            arry: str = ""
            for i in range(join):
                result = random.randint(0, len(arr) - 1)
                arry += f"{i + 1}: {arr[result]}\n"
                del arr[result]

            embed = discord.Embed(title="추첨 완료", color=0xb0a7d3)
            embed.set_author(name="페이", icon_url="https://i.imgur.com/7a4oeOi.jpg")
            embed.add_field(name="당첨자", value=arry, inline=True)
            await interaction.response.send_message(embed=embed)

    def MemoryGameGrid(cards_dis):
        base= f"""⬛1️⃣2️⃣3️⃣4️⃣
        🇦{cards_dis[0]}{cards_dis[1]}{cards_dis[2]}{cards_dis[3]}
        🇧{cards_dis[4]}{cards_dis[5]}{cards_dis[6]}{cards_dis[7]}
        🇨{cards_dis[8]}{cards_dis[9]}{cards_dis[10]}{cards_dis[11]}
        🇩{cards_dis[12]}{cards_dis[13]}{cards_dis[14]}{cards_dis[15]}"""
        return base

    @app_commands.command(name="카드짝", description="카드 짝 맞추기 게임을 플레이합니다")
    async def MemoryGame(self, interaction: discord.Interaction):
        command_userid = interaction.user.id
        variables = MemoryGameVars()
        print(variables.cards)
        base=Game.MemoryGameGrid(variables.cards_dis)
        embed = discord.Embed(
                title="카드 짝 맞추기",
                description=base)
        view = MemoryGameView(variables, command_userid)
        await interaction.response.send_message(embed=embed, view=view)

    @app_commands.command(name="운세", description="오늘의 운세입니다")
    async def DailyLuck(self, interaction: discord.Interaction, zodiac: str):
        """
        _summary_
        오늘의 띠별 운세
        Args:
            interaction (discord.interaction, 필수): 커맨드 쓴 사람 & interaction
            zodiac (int, 옵션): 자신의 띠
        """

        date_text = datetime.datetime.now().strftime("%m")+"월"+" "+datetime.datetime.now().strftime("%d")+"일"
        image = Image.open(os.path.join(f"{__location__}\\DailyLuck\\DailyLuckImg.jpg"))
        fonts_dir = os.path.join(f"{__location__}\\DailyLuck")
        draw = ImageDraw.Draw(image)
        draw.text((410,40),date_text,font=ImageFont.truetype(os.path.join(fonts_dir, 'Dobong_Cultural_Routes(TTF).ttf'), 35), fill=(210,210,210))
        image.save(os.path.join(f"{__location__}\\DailyLuck\\DailyLuckImgDate.jpg"))

        try:
            luck_text = ZodiacDict[zodiac]
        except:
            luck_text = "호랑이·토끼·용·뱀·말·양·원숭이·닭·개·돼지·쥐·소 중 하나의 띠를 입력해 주십시오"

        msg = ""
        n = len(luck_text)//10
        for i in range(n):
            msg += luck_text[i*10:(i+1)*10]
            msg += "\n"
        msg += luck_text[n*10:]

        image = Image.open(os.path.join(f"{__location__}\\DailyLuck\\DailyLuckImgDate.jpg"))
        fonts_dir = os.path.join(f"{__location__}\\DailyLuck")
        draw = ImageDraw.Draw(image)
        draw.text((360,95),msg,font=ImageFont.truetype(os.path.join(fonts_dir, 'Dobong_Cultural_Routes(TTF).ttf'), 35), fill=(255,255,255))
        image.save(os.path.join(f"{__location__}\\DailyLuck\\DailyLuckImgEdit.jpg"))

        embed = discord.Embed(title="오늘의 운세", colour=discord.Colour(0x71368a))
        file = discord.File(os.path.join(f"{__location__}\\DailyLuck\\DailyLuckImgEdit.jpg"), filename="image.jpg")
        embed.set_image(url="attachment://image.jpg")
        embed.set_author(name="성의", icon_url="https://pbs.twimg.com/profile_images/2541389832/oph3xdipc43uupewwjau_400x400.png")
        await interaction.response.send_message(embed=embed, file=file)

async def setup(bot):
    await bot.add_cog(Game(bot))
