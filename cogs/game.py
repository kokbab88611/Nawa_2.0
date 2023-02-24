import discord,random,string,array
import asyncio
from discord import app_commands,Interaction,Reaction,InteractionResponse
from discord.ext import commands, tasks
import time, math

class RcpButton(discord.ui.View):
        def __init__(self):
            super().__init__()

        new_embed = discord.Embed(title='embed 2')
        @discord.ui.button(label='True')
        async def true(self, interactionresponse: discord.InteractionResponse, button: discord.ui.Button):
            await interactionresponse.response.edit_message(embed=discord.Embed(title='embed 2'))
            self.stop()
        @discord.ui.button(label='False')
        async def false(self, interactionresponse: discord.InteractionResponse, button: discord.ui.Button):
            await interactionresponse.response.edit_message(embed=discord.Embed(title='embed 3'))
            self.stop()

class Game(commands.Cog):
    channel_id:string
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("준비됨")

    @app_commands.command(name="가위바위보", description="가위바위보를 합니다 페이랑")
    async def rcp(self, interaction: discord.Interaction):
        def rcpnum():
            cur_time = str(time.perf_counter())
            rnd = float(cur_time[::-1][:3:])/1000
            return 0 + rnd*(3-0)
        rcp_num = math.ceil(rcpnum())
    

    @app_commands.command(name="버튼", description="테스트")
    async def button_test(self, interactionresponse: discord.InteractionResponse):
        first_embed = discord.Embed(title='embed 1')

        view = RcpButton()
        await interactionresponse.response.send_message(embed=first_embed, view=view)
        await view.wait()
        #await interaction.message.edit()

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