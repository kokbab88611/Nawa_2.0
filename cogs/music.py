import discord, nacl
import asyncio
from discord import app_commands
from discord.ext import commands
import yt_dlp
import os
import random
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

class Music(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @app_commands.command(name="재생", description="음원을 재생합니다")
    async def play(self, interaction: discord.Interaction, url: str):
        yt_dl_opts = {'format': 'bestaudio/best'}
        ytdl = yt_dlp.YoutubeDL(yt_dl_opts)
        ffmpeg_options = {'options': "-vn"}

        voice_client = await interaction.user.voice.channel.connect()
        self.bot.voice_clients[0] = voice_client

        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))

        song = data['url']
        player = discord.FFmpegPCMAudio(song, **ffmpeg_options)

        voice_client.play(player)

    @app_commands.command(name="일시정지", description="재생을 일시정지합니다")
    async def pause(self, interaction: discord.Interaction):
        self.bot.voice_clients[0].pause()

    @app_commands.command(name="재개", description="재생을 재개합니다")
    async def resume(self, interaction: discord.Interaction):
        self.bot.voice_clients[0].resume()

    @app_commands.command(name="퇴장", description="통화방에서 나갑니다")
    async def leave(self, interaction: discord.Interaction):
        await self.bot.voice_clients[0].disconnect()
    
    
async def setup(bot):
    await bot.add_cog(Music(bot))
    
