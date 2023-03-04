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
        self.queue = []
        self.voice_client = ""

    async def play_music(self):
        yt_dl_opts = {'format': 'bestaudio/best'}
        ytdl = yt_dlp.YoutubeDL(yt_dl_opts)
        ffmpeg_options = {'options': "-vn"}

        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(self.queue[0], download=False))
        song = data['url']
        player = discord.FFmpegPCMAudio(song, **ffmpeg_options)
        self.voice_client.play(player)

    @app_commands.command(name="재생", description="음악을 재생합니다")
    async def play(self, interaction: discord.Interaction, url: str):
        await interaction.response.send_message(f'음악을 재생합니다')
        self.voice_client = await interaction.user.voice.channel.connect()
        self.queue.append(url)

        while len(self.queue) > 0:
            await Music.play_music(self)
            print(self.queue)
            while self.voice_client.is_playing() or self.voice_client.is_paused():
                await asyncio.sleep(0.1)
            self.queue.pop(0)
        await self.bot.voice_clients[0].disconnect()

    @app_commands.command(name="추가", description="재생목록에 곡을 추가합니다")
    async def add_queue(self, interaction: discord.Interaction, url: str):
        self.queue.append(url)
        await interaction.response.send_message(f'재생목록에 {url}을 추가했습니다')
        
    @app_commands.command(name="재생목록", description="재생목록을 불러옵니다")
    async def call_queue(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'재생목록 {self.queue}')

    @app_commands.command(name="일시정지", description="재생을 일시정지합니다")
    async def pause(self, interaction: discord.Interaction):
        self.bot.voice_clients[0].pause()
        await interaction.response.send_message("음악이 일시정지 되었습니다")

    @app_commands.command(name="스킵", description="현재 음악을 스킵합니다")
    async def skip(self, interaction: discord.Interaction):
        try:
            if self.voice_client.is_playing():
                self.voice_client.stop()
                await interaction.response.send_message("음악이 스킵되었습니다")
            else:
                await interaction.response.send_message("스킵할 음악이 없습니다")
        except:
            await interaction.response.send_message("봇이 통화방에 없습니다")

    @app_commands.command(name="재개", description="재생을 재개합니다")
    async def resume(self, interaction: discord.Interaction):
        self.bot.voice_clients[0].resume()
        await interaction.response.send_message("음악을 재개합니다")

    @app_commands.command(name="퇴장", description="통화방에서 나갑니다")
    async def leave(self, interaction: discord.Interaction):
        await self.bot.voice_clients[0].disconnect()
        await interaction.response.send_message("퇴장합니다")

async def setup(bot):
    await bot.add_cog(Music(bot))
    
