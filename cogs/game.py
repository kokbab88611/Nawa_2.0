import discord,random,string,array
import asyncio
from discord import app_commands,Interaction,Reaction,InteractionResponse
from discord.ui import Button, View
from discord.ext import commands, tasks

class RcpButtons(Button):
    def __init__(self, label, emoji, custom_id, command_userid, bet_money):
        super().__init__(label=label, style=discord.ButtonStyle.green, emoji=emoji, custom_id=custom_id)
        self.custom_id, self.user_rcp, self.command_userid, self.bet_money = str(custom_id), emoji + label, command_userid, bet_money

    async def rcp_result(user_rcp):
        rcp_num = random.randint(1,3)
        if rcp_num == 1:
            bot_rcp = "✌️가위"
            if user_rcp == "scissors":
                result = "draw"
            elif user_rcp == "rock":
                result = "win"
            else:
                result = "lose"
        elif rcp_num == 2:
            bot_rcp = "✊바위"
            if user_rcp == "scissors":
                result = "lose"
            elif user_rcp == "rock":
                result = "draw"
            else:
                result = "win"
        else:
            bot_rcp = "✋보"
            if user_rcp == "scissors":
                result = "win"
            elif user_rcp == "rock":
                result = "lose"
            else:
                result = "draw"
        return bot_rcp, result

    async def callback(self, interaction):
        if interaction.user.id == self.command_userid:
            bot_rcp, result = await RcpButtons.rcp_result(self.custom_id)
            if result == "win":
                result = "이김"
                message = f'{self.bet_money} 얻음'
                #money_increase(self.bet_money, user)
            elif result == "draw":
                result = "비김"
                message = f'{int(round(self.bet_money * 0.5, 0))} 잃음'
                #money_decrease(int(round(self.bet_money * 0.5, 0)), user)
            else:
                result = "짐"
                message = f'{self.bet_money} 잃음'
                #money_decrease(self.bet_money, user)
            embed = discord.Embed(title=result, description=f'페이:{bot_rcp}\n나:{self.user_rcp}\n{message}', color=0xb0a7d3)
            await interaction.response.edit_message(content="", embed=embed, view=None)
        else:
            await interaction.response.send_message(content="너 이거 못눌러", ephemeral=True)

class Game(commands.Cog):
    channel_id:string
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("준비됨")

    @app_commands.command(name="가위바위보", description="폐이와 가위바위보를 합니다")
    async def buttontest(self, interaction: discord.Interaction, bet_money: int):
        #if bet_money > owned_money:
        if bet_money:
            view = View()
            view.add_item(RcpButtons('가위', "✌️", "scissors", interaction.user.id, bet_money))
            view.add_item(RcpButtons('바위', "✊", "rock", interaction.user.id, bet_money))
            view.add_item(RcpButtons('보', "✋", "paper", interaction.user.id, bet_money))
            embed = discord.Embed(title='가위바위보중에 하나 골라')
            await interaction.response.send_message(embed=embed, view=view)
        else:
            await interaction.response.send_message(content="돈 부족. 너 돈 필요.", ephemeral=True)

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

    @app_commands.command(name="가챠", description="호감도템 가챠")
    async def gacha(self, interaction: discord.Interaction):
        pos = {"Common": 40, "Rare": 45, "Epic": 12, "Legendary": 3}

        items = {
            "랑이1": "Common",
            "일반1": "Common",
            "치이1": "Common",
            "랑이2": "Rare",
            "일반2": "Rare",
            "치이2": "Rare",
            "일반3": "Epic",
            "치이3": "Epic",
            "랑이3": "Epic",
            "전설": "Legendary",
        }

        rarity = random.choices(list(pos.keys()), weights=list(pos.values()), k=1)[0]
        item = random.choice([k for k, v in items.items() if v == rarity])

        if rarity == "Legendary":
            emcolor=0xe67e22
        elif rarity == "Epic":
            emcolor=0x71368a
        elif rarity == "Rare":
            emcolor=0x3498db
        else:
            emcolor=0x2ecc71

        if "치이" in item:
            item_pic = "https://i.imgur.com/isUEgXb.png"
        elif "일반" in item:
            item_pic = "https://i.imgur.com/6UifvGD.png"
        elif "랑이" in item:
            item_pic = "https://i.imgur.com/GbH5Htg.png"
        else:
            item_pic = "https://i.imgur.com/FjhHwtU.jpeg"

        embed = discord.Embed(
            title="가챠 결과",
            description=f"{rarity} \n {item}",
            color=emcolor,
        )

        embed.set_image(url=item_pic)
        embed.set_footer(text=f"총 보유량:{item}")
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Game(bot))
