import discord
from discord import app_commands
from discord.ext import commands
import os
import nacl
from gtts import gTTS

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

class CommonConmmand(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @app_commands.command(name="초대")
    async def invite_link(self, interaction: discord.Interaction):
        embed=discord.Embed(title="초대 링크", url="https://discord.com/api/oauth2/authorize?client_id=515416848477585410&permissions=8&scope=bot", description="많은 관심 감사합니다!", color=0xafc2f3)
        embed.set_footer(text="나와 아해들")        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="서버")
    async def server_link(self, interaction: discord.Interaction):
        embed=discord.Embed(title="링크", url="https://discord.gg/ay6YMxX", description="소통해요!", color=0xafc2f3)
        embed.set_footer(text="나와 아해들 디스코드 서버")
        await interaction.response.send_message(embed=embed)

    # @app_commands.command(name="말해", description="tts입니다")
    # async def text_to_speech(self, interaction: discord.Interaction, text: str):
    #     channel = interaction.user.voice.channel
    #     tts = gTTS(text=text, lang="ko")
    #     tts.save(os.path.join(f"{__location__}\\TTS\\text.mp3"))

    #     await interaction.response.send_message("하는중")
    #     if not interaction.guild.voice_client:
    #         try:
    #             vc = await channel.connect()
    #         except:
    #             return await interaction.response.send_message("먼저 통화방에 접속해 주십시오")
    #     else:
    #         vc = interaction.guild.voice_client

    #     vc.play(discord.FFmpegPCMAudio(os.path.join(f"{__location__}\\TTS\\text.mp3")))

async def setup(bot):
    await bot.add_cog(CommonConmmand(bot))
    
