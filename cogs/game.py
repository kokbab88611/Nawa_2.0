import discord,random,string,array,time
import asyncio
from discord import app_commands,Interaction,Reaction,InteractionResponse
from discord.ui import Button, View
from discord.ext import commands, tasks
import random

class MemoryGameVars():
    def __init__(self):
        self.tries = 0
        self.cards = ["1️⃣", "1️⃣", "2️⃣", "2️⃣", "3️⃣", "3️⃣", "4️⃣", "4️⃣", "5️⃣", "5️⃣", "6️⃣", "6️⃣", "7️⃣", "7️⃣", "8️⃣", "8️⃣"]
        self.cards = random.sample(self.cards, len(self.cards))
        self.cards_dis = ["⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜"]

class MemoryGameDropDown(discord.ui.Select):
    def __init__(self, variables):
        self.variables = variables
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
                view = MemoryGameView(self.variables)
                await interaction.response.edit_message(content="", view=view, embed=embed)
            else:
                base = f"소요 횟수: {self.variables.tries}"
                embed = discord.Embed(
                        title="카드 짝 맞추기",
                        description=base)
                await interaction.response.edit_message(content="", embed=embed)
        else:
            base=Game.MemoryGameGrid(self.variables.cards_dis)
            embed = discord.Embed(
                    title="카드 짝 맞추기",
                    description=base)
            view = MemoryGameView(self.variables)
            await interaction.response.edit_message(content="이미 뒤집힌 카드는 선택할 수 없습니다", view=view, embed=embed)

class MemoryGameView(discord.ui.View):
    def __init__(self, variables):
        super().__init__()
        self.variables = variables
        self.add_item(MemoryGameDropDown(variables))

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
        variables = MemoryGameVars()
        print(variables.cards)
        base=Game.MemoryGameGrid(variables.cards_dis)
        embed = discord.Embed(
                title="카드 짝 맞추기",
                description=base)
        view = MemoryGameView(variables)
        await interaction.response.send_message(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(Game(bot))
