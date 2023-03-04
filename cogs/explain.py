import os, json
import discord
from discord import app_commands, ui
from discord.ext import commands, tasks
from discord.ui import Button, Select, View

class ComButton(discord.ui.Button):
    def __init__(self, button_style, label, custom_id, able) -> None:

        super().__init__(
            style=button_style, label=label, custom_id=custom_id, disabled=able
        )

    async def callback(self, interaction: discord.Interaction):
        view = helpview()
        if self.custom_id == "normal":
            embed = discord.Embed(
                title="Title",
                description="Sample \n sample",
                colour=discord.Colour.from_rgb(241, 196, 15),
            )
            embed.add_field(name="Text1", value="Sample Text", inline=False)
            embed.add_field(name="Text2", value="Sample Text", inline=False)
            embed.add_field(
                name="\ text1", value="> 1.asd\n> 2.asd\n> 3.asd\n> 4.asd", inline=True
            )
            embed.add_field(
                name="\ text2", value="> 1.asd\n> 2.asd\n> 3.asd\n> 4.asd", inline=True
            )
            embed.set_footer(text="Main")

        elif self.custom_id == "mod":
            embed = discord.Embed(
                title="Title",
                description="Sample \n sample",
                colour=discord.Colour.from_rgb(241, 196, 15),
            )
            embed.add_field(name="Text1", value="Sample Text", inline=False)
            embed.add_field(name="Text2", value="Sample Text", inline=False)
            embed.add_field(
                name="\ text1", value="> 1.asd\n> 2.asd\n> 3.asd\n> 4.asd", inline=True
            )
            embed.add_field(
                name="\ text2", value="> 1.asd\n> 2.asd\n> 3.asd\n> 4.asd", inline=True
            )
            embed.set_footer(text="Main")

        elif self.custom_id == "guild":
            embed = discord.Embed(
                title="Title",
                description="Sample \n sample",
                colour=discord.Colour.from_rgb(241, 196, 15),
            )
            embed.add_field(name="Text1", value="Sample Text", inline=False)
            embed.add_field(name="Text2", value="Sample Text", inline=False)
            embed.add_field(
                name="\ text1", value="> 1.asd\n> 2.asd\n> 3.asd\n> 4.asd", inline=True
            )
            embed.add_field(
                name="\ text2", value="> 1.asd\n> 2.asd\n> 3.asd\n> 4.asd", inline=True
            )
            embed.set_footer(text="Main")

        elif self.custom_id == "game":
            embed = discord.Embed(
                title="Title",
                description="Sample \n sample",
                colour=discord.Colour.from_rgb(241, 196, 15),
            )
            embed.add_field(name="Text1", value="Sample Text", inline=False)
            embed.add_field(name="Text2", value="Sample Text", inline=False)
            embed.add_field(
                name="\ text1", value="> 1.asd\n> 2.asd\n> 3.asd\n> 4.asd", inline=True
            )
            embed.add_field(
                name="\ text2", value="> 1.asd\n> 2.asd\n> 3.asd\n> 4.asd", inline=True
            )
            embed.add_field(
                name="\ text3", value="> 1.asd\n> 2.asd\n> 3.asd\n> 4.asd", inline=True
            )
            embed.set_footer(text="Main")

        button1 = ComButton(discord.ButtonStyle.gray, "일반", "normal", False)
        button2 = ComButton(discord.ButtonStyle.blurple, "모드", "mod", False)
        button3 = ComButton(discord.ButtonStyle.green, "게임", "game", False)
        button4 = ComButton(discord.ButtonStyle.grey, "길드", "guild", False)

        view.add_item(button1)
        view.add_item(button2)
        view.add_item(button3)
        view.add_item(button4)

        await interaction.response.edit_message(view=view, embed=embed)


####################################################################################################################################
class InfoSelect(Select):
    def __init__(self):

        options = [
            discord.SelectOption(
                label="메인", description="도박 시스템의 기본적인 설명 및 주의 사항", emoji="🎮", value=11
            ),
            discord.SelectOption(
                label="커맨드", description="재화에 관한 설명", emoji="📔", value=22
            ),
            discord.SelectOption(
                label="게임1", description="게임에 관한 설명", emoji="🎮", value=33
            ),
            discord.SelectOption(
                label="게임2", description="게임에 관한 설명", emoji="🎮", value=44
            ),
            discord.SelectOption(
                label="게임3", description="게임에 관한 설명", emoji="🎮", value=55
            ),
        ]
        super().__init__(
            placeholder="Choose an option", options=options, min_values=1, max_values=1
        )

    ####################################################################################################################################
    async def callback(self, interaction: discord.Interaction):

        view = helpview()
        if self.values[0] == "11":
            embed = discord.Embed(
                title="Title",
                description="",
                colour=discord.Colour.from_rgb(241, 196, 15),
            )
            embed.add_field(name="Text1", value="Sample Text", inline=False)
            embed.add_field(name="Text2", value="Sample Text", inline=False)
            embed.add_field(
                name="\📖 Rules", value="> 1.asd\n> 2.asd\n> 3.asd\n> 4.asd", inline=True
            )
            embed.set_footer(text="Main")
        elif self.values[0] == "22":
            embed = discord.Embed(
                title="Command",
                description="Sample \n sample",
                colour=discord.Colour.from_rgb(241, 196, 15),
            )
            embed.add_field(name="Text1", value="Sample Text", inline=False)
            embed.add_field(name="Text2", value="Sample Text", inline=False)
            embed.add_field(
                name="\ text1", value="> 1.asd\n> 2.asd\n> 3.asd\n> 4.asd", inline=True
            )
            embed.add_field(
                name="\ text2", value="> 1.asd\n> 2.asd\n> 3.asd\n> 4.asd", inline=True
            )
            embed.add_field(
                name="\ text3", value="> 1.asd\n> 2.asd\n> 3.asd\n> 4.asd", inline=True
            )
            embed.set_footer(text="Main")
            button1 = ComButton(discord.ButtonStyle.gray, "일반", "normal", False)
            button2 = ComButton(discord.ButtonStyle.blurple, "모드", "mod", False)
            button3 = ComButton(discord.ButtonStyle.green, "게임", "game", False)
            button4 = ComButton(discord.ButtonStyle.grey, "길드", "guild", False)

            view.add_item(button1)
            view.add_item(button2)
            view.add_item(button3)
            view.add_item(button4)

        elif self.values[0] == "33":
            embed = discord.Embed(
                title="Title",
                description="Sample \n sample",
                colour=discord.Colour.from_rgb(241, 196, 15),
            )
            embed.add_field(name="Text1", value="Sample Text", inline=False)
            embed.add_field(
                name="상세 룰",
                value="[게임1](https://namu.wiki/w/%EB%82%98%EB%AC%B4%EC%9C%84%ED%82%A4:%EB%8C%80%EB%AC%B8)",
                inline=False,
            )
            embed.add_field(
                name=" 배당금1", value="> 1.asd\n> 2.asd\n> 3.asd\n> 4.asd", inline=True
            )
            embed.set_footer(text="Main")

        elif self.values[0] == "44":
            embed = discord.Embed(
                title="Title",
                description="Sample \n sample",
                colour=discord.Colour.from_rgb(241, 196, 15),
            )
            embed.add_field(name="Text1", value="Sample Text", inline=False)
            embed.add_field(
                name="상세 룰",
                value="[게임1](https://namu.wiki/w/%EB%82%98%EB%AC%B4%EC%9C%84%ED%82%A4:%EB%8C%80%EB%AC%B8)",
                inline=False,
            )
            embed.add_field(
                name="배당금1", value="> 1.asd\n> 2.asd\n> 3.asd\n> 4.asd", inline=True
            )
            embed.set_footer(text="Main")

        elif self.values[0] == "55":
            embed = discord.Embed(
                title="Title",
                description="Sample \n sample",
                colour=discord.Colour.from_rgb(241, 196, 15),
            )
            embed.add_field(name="Text1", value="Sample Text", inline=False)
            embed.add_field(
                name="상세 룰",
                value="[게임1](https://namu.wiki/w/%EB%82%98%EB%AC%B4%EC%9C%84%ED%82%A4:%EB%8C%80%EB%AC%B8)",
                inline=False,
            )
            embed.add_field(
                name="배당금1", value="> 1.asd\n> 2.asd\n> 3.asd\n> 4.asd", inline=True
            )
            embed.set_footer(text="Main")
        await interaction.response.edit_message(view=view, embed=embed)


####################################################################################################################################
class GInfoSelect(Select):
    def __init__(self):

        options = [
            discord.SelectOption(
                label="메인", description="도박 시스템의 기본적인 설명 및 주의 사항", emoji="🎮", value=1
            ),
            discord.SelectOption(
                label="재화", description="재화에 관한 설명", emoji="🎮", value=2
            ),
            discord.SelectOption(
                label="게임1", description="게임에 관한 설명", emoji="🎮", value=3
            ),
            discord.SelectOption(
                label="게임2", description="게임에 관한 설명", emoji="🎮", value=4
            ),
            discord.SelectOption(
                label="게임3", description="게임에 관한 설명", emoji="🎮", value=5
            ),
        ]
        super().__init__(
            placeholder="Choose an option", options=options, min_values=1, max_values=1
        )

    ####################################################################################################################################
    async def callback(self, interaction: discord.Interaction):

        if self.values[0] == "1":
            embed = discord.Embed(
                title="Title",
                description="",
                colour=discord.Colour.from_rgb(241, 196, 15),
            )
            embed.add_field(name="Text1", value="Sample Text", inline=False)
            embed.add_field(name="Text2", value="Sample Text", inline=False)
            embed.add_field(
                name="\📖 Rules", value="> 1.asd\n> 2.asd\n> 3.asd\n> 4.asd", inline=True
            )
            embed.set_footer(text="Main")
        elif self.values[0] == "2":
            embed = discord.Embed(
                title="Title",
                description="Sample \n sample",
                colour=discord.Colour.from_rgb(241, 196, 15),
            )
            embed.add_field(name="Text1", value="Sample Text", inline=False)
            embed.add_field(name="Text2", value="Sample Text", inline=False)
            embed.add_field(
                name="\ text1", value="> 1.asd\n> 2.asd\n> 3.asd\n> 4.asd", inline=True
            )
            embed.add_field(
                name="\ text2", value="> 1.asd\n> 2.asd\n> 3.asd\n> 4.asd", inline=True
            )
            embed.add_field(
                name="\ text3", value="> 1.asd\n> 2.asd\n> 3.asd\n> 4.asd", inline=True
            )
            embed.set_footer(text="Main")

        elif self.values[0] == "3":
            embed = discord.Embed(
                title="Title",
                description="Sample \n sample",
                colour=discord.Colour.from_rgb(241, 196, 15),
            )
            embed.add_field(name="Text1", value="Sample Text", inline=False)
            embed.add_field(
                name="상세 룰",
                value="[게임1](https://namu.wiki/w/%EB%82%98%EB%AC%B4%EC%9C%84%ED%82%A4:%EB%8C%80%EB%AC%B8)",
                inline=False,
            )
            embed.add_field(
                name=" 배당금1", value="> 1.asd\n> 2.asd\n> 3.asd\n> 4.asd", inline=True
            )
            embed.set_footer(text="Main")

        elif self.values[0] == "4":
            embed = discord.Embed(
                title="Title",
                description="Sample \n sample",
                colour=discord.Colour.from_rgb(241, 196, 15),
            )
            embed.add_field(name="Text1", value="Sample Text", inline=False)
            embed.add_field(
                name="상세 룰",
                value="[게임1](https://namu.wiki/w/%EB%82%98%EB%AC%B4%EC%9C%84%ED%82%A4:%EB%8C%80%EB%AC%B8)",
                inline=False,
            )
            embed.add_field(
                name="배당금1", value="> 1.asd\n> 2.asd\n> 3.asd\n> 4.asd", inline=True
            )
            embed.set_footer(text="Main")

        elif self.values[0] == "5":
            embed = discord.Embed(
                title="Title",
                description="Sample \n sample",
                colour=discord.Colour.from_rgb(241, 196, 15),
            )
            embed.add_field(name="Text1", value="Sample Text", inline=False)
            embed.add_field(
                name="상세 룰",
                value="[게임1](https://namu.wiki/w/%EB%82%98%EB%AC%B4%EC%9C%84%ED%82%A4:%EB%8C%80%EB%AC%B8)",
                inline=False,
            )
            embed.add_field(
                name="배당금1", value="> 1.asd\n> 2.asd\n> 3.asd\n> 4.asd", inline=True
            )
            embed.set_footer(text="Main")

        view = infoview()
        await interaction.response.edit_message(view=view, embed=embed)


####################################################################################################################################
class infoview(discord.ui.View):
    """
    _summary_
        클래스 안으로 값 받아옴
    Args:
        self (obj, 필수): 오브젝트
        user (discord.Member, 필수): 디코 유저
    """

    def __init__(self) -> None:
        super().__init__()
        self.add_item(GInfoSelect())


####################################################################################################################################
class helpview(discord.ui.View):
    def __init__(self) -> None:
        super().__init__()
        self.add_item(InfoSelect())


####################################################################################################################################


class Explain(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("준비됨")

    @app_commands.command(name="게임정보", description="게임정보")
    async def GameInfo(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Title",
            description="Sample textSample textSample textSample textSample textSample text\nSample text",
            colour=discord.Colour.from_rgb(241, 196, 15),
        )
        await interaction.response.send_message(embed=embed, view=infoview())

    @app_commands.command(name="도움말", description="도움말")
    async def Help(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Title",
            description="Sample textSample textSample textSample textSample textSample text\nSample text",
            colour=discord.Colour.from_rgb(241, 196, 15),
        )
        await interaction.response.send_message(embed=embed, view=helpview())


async def setup(bot):
    await bot.add_cog(Explain(bot))