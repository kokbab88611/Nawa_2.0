import discord, nacl
from discord import app_commands
from discord.ext import commands
import yt_dlp
import os
import random
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

#FFMPEG_PATH = os.path.join(f"{__location__}\\ffmpeg\\bin\\ffmpeg.exe")

class Music(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @app_commands.command(name="재생", description="음원을 재생합니다")
    async def play(self, interaction: discord.Interaction, url: str):
        vc = self.bot.voice_clients[0]
        YDL_OPTIONS = {'format': 'bestaudio'}
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        #if not vc.is_playing() and not vc.is_paused():
        with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            URL = info['formats'][0]['url']
            #source = await discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS)
            #source = await discord.FFmpegOpusAudio.from_probe(URL, method='fallback')
            source = await discord.FFmpegOpusAudio.from_probe(URL, **FFMPEG_OPTIONS)
            vc.play(source)


    @app_commands.command(name="입장", description="통화방에 연결합니다")
    async def join(self, interaction: discord.Interaction):
        channel = interaction.user.voice.channel
        await channel.connect()

    

    @app_commands.command(name="퇴장", description="통화방에서 나갑니다")
    async def leave(self, interaction: discord.Interaction):
        await self.bot.voice_clients[0].disconnect()
    

async def setup(bot):
    await bot.add_cog(Music(bot))
    
