import discord,random,string,array
import asyncio
from discord import app_commands,Interaction,Reaction,InteractionResponse
from discord.ui import Button, View
from discord.ext import commands, tasks

class RcpButtons(Button):
    def __init__(self, label, emoji, custom_id, command_usrid):
        super().__init__(label=label, style=discord.ButtonStyle.green, emoji=emoji, custom_id=custom_id)
        self.custom_id = str(custom_id)
        self.usr_rcp = emoji + label
        self.command_usrid = command_usrid

    async def rcp_result(usr_rcp):
            rcp_num = random.randint(1,3)
            if rcp_num == 1:
                bot_rcp = "✌️가위"
                if usr_rcp == "scissors":
                    result = "비김"
                elif usr_rcp == "rock":
                    result = "이김"
                else:
                    result = "짐"
            elif rcp_num == 2:
                bot_rcp = "✊바위"
                if usr_rcp == "scissors":
                    result = "짐"
                elif usr_rcp == "rock":
                    result = "비김"
                else:
                    result = "이김"
            else:
                bot_rcp = "✋보"
                if usr_rcp == "scissors":
                    result = "이김"
                elif usr_rcp == "rock":
                    result = "짐"
                else:
                    result = "비김"
            return bot_rcp, result

    async def callback(self, interaction):
        button_usrid = interaction.user.id
        if button_usrid == self.command_usrid:
            bot_rcp, result = await RcpButtons.rcp_result(self.custom_id)
            embed = discord.Embed(title=result, description=f'페이:{bot_rcp} \n 나:{self.usr_rcp}', color=0xb0a7d3)
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

    @app_commands.command(name="가위바위보", description="합니다 가위바위보를 페이랑")
    async def buttontest(self, interaction: discord.Interaction):
        command_usrid = interaction.user.id
        scissors_button = RcpButtons('가위', "✌️", "scissors", command_usrid)
        rock_button = RcpButtons('바위', "✊", "rock", command_usrid)
        paper_button = RcpButtons('보', "✋", "paper", command_usrid)
        view = View()
        view.add_item(scissors_button)
        view.add_item(rock_button)
        view.add_item(paper_button)
        first_embed = discord.Embed(title='가위바위보중에 하나 골라')
        await interaction.response.send_message(embed=first_embed, view=view)

    @app_commands.command(name="추첨", description="추첨기를 생성합니다")
    async def raname(self, interaction: discord.Interaction, join: int = 1, people: str = ""):
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
