#import discord, nacl
import asyncio
import discord
from discord import app_commands
from discord.ext import commands
#import yt_dlp
import typing
import wavelink
import os
import random
import lavalink

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

class Music(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        bot.loop.create_task(self.create_nodes())

    async def create_nodes(self):
        await self.bot.wait_until_ready()
        await wavelink.NodePool.create_node(bot=self.bot, host="127.0.0.1", port="2333", password="youshallnotpass", region="asia")

    @app_commands.command(name="입장", description="음악봇이 입장합니다")
    async def join(self, interaction: discord.Interaction, channel: typing.Optional[discord.VoiceChannel]):
        if channel is None:
            try:
                channel = interaction.user.voice.channel
            except:
                return await interaction.response.send_message("먼저 통화방에 접속해 주십시오")
        
        node = wavelink.NodePool.get_node()
        player = node.get_player(interaction.guild)

        if player is not None:
            if player.is_connected():
                return await interaction.response.send_message("이미 봇이 통화방에 있습니다")
        
        await channel.connect(cls=wavelink.Player)
        await interaction.response.send_message(f'{channel.name}에 입장하였습니다')

    @app_commands.command(name="퇴장", description="음악봇이 퇴장합니다")
    async def leave(self, interaction: discord.Interaction):
        node = wavelink.NodePool.get_node()
        player = node.get_player(interaction.guild)

        if player is None:
            return await interaction.response.send_message("음악봇이 통화방에 없습니다")
        await player.disconnect()
        await interaction.response.send_message("음악봇이 퇴장하였습니다")

    @app_commands.command(name="재생", description="음악을 재생합니다")
    async def play(self, interaction: discord.Interaction, search: str):
        search = await wavelink.YouTubeTrack.search(query=search, return_first=True)
        if not interaction.guild.voice_client:
            vc: wavelink.Player = await interaction.user.voice.channel.connect(cls=wavelink.Player)
        else:
            vc: wavelink.Player = interaction.guild.voice_client

        await vc.play(search)
        await interaction.response.send_message(f'{search} 재생합니다')

    @app_commands.command(name="정지", description="음악 재생을 정지합니다")
    async def stop(self, interaction: discord.Interaction):
        node = wavelink.NodePool.get_node()
        player = node.get_player(interaction.guild)

        if player is None:
            return await interaction.response.send_message("음악봇이 통화방에 없습니다")

        if player.is_playing():
            if player.is_paused():
                await player.resume()
            await player.stop()
            return await interaction.response.send_message("재생이 정지되었습니다")
        else:
            return await interaction.response.send_message("재생되고 있는 음악이 없습니다")

    @app_commands.command(name="일시정지", description="음악 재생을 일시정지합니다")
    async def pause(self, interaction: discord.Interaction):
        node = wavelink.NodePool.get_node()
        player = node.get_player(interaction.guild)

        if player is None:
            return await interaction.response.send_message("음악봇이 통화방에 없습니다")
        
        if not player.is_paused():
            if player.is_playing:
                await player.pause()
                return await interaction.response.send_message("재생중인 음악을 일시정지합니다")
            else:
                return await interaction.response.send_message("재생중인 음악이 없습니다")
        else:
            return await interaction.response.send_message("음악이 이미 일시정지 되었습니다")

    @app_commands.command(name="재개", description="음악 재생을 재개합니다")
    async def resume(self, interaction: discord.Interaction):
        node = wavelink.NodePool.get_node()
        player = node.get_player(interaction.guild)

        if player is None:
            return await interaction.response.send_message("음악봇이 통화방에 없습니다")
        
        if player.is_paused():
            if player.is_playing():
                await player.resume()
                return await interaction.response.send_message("음악 재생이 재개되었습니다")
            else:
                return await interaction.response.send_message("재생중인 음악이 없습니다")
        else:
            return await interaction.response.send_message("음악이 이미 재생중입니다")

async def setup(bot):
    await bot.add_cog(Music(bot))
    
# def __init__(self, bot) -> None:
#         self.bot = bot
#         self.queue = []
#         self.voice_client = ""

#     async def play_music(self):
#         yt_dl_opts = {'format': 'bestaudio/best'}
#         ytdl = yt_dlp.YoutubeDL(yt_dl_opts)
#         ffmpeg_options = {'options': "-vn"}

#         loop = asyncio.get_event_loop()
#         data = await loop.run_in_executor(None, lambda: ytdl.extract_info(self.queue[0], download=False))
#         song = data['url']
#         player = discord.FFmpegPCMAudio(song, **ffmpeg_options)
#         self.voice_client.play(player)

#     @app_commands.command(name="재생", description="음악을 재생합니다")
#     async def play(self, interaction: discord.Interaction, url: str):
#         try:
#             if self.voice_client.is_playing() or self.voice_client.is_paused():
#                 self.queue.append(url)
#                 await interaction.response.send_message(f'재생목록에 {url}을 추가했습니다')
#         except:
#             await interaction.response.send_message(f'음악을 재생합니다')
#             self.queue = []
#             self.voice_client = await interaction.user.voice.channel.connect()
#             self.queue.append(url)

#             while len(self.queue) > 0:
#                 await Music.play_music(self)
#                 print(self.queue)
#                 while self.voice_client.is_playing() or self.voice_client.is_paused():
#                     await asyncio.sleep(0.1)
#                 self.queue.pop(0)
#             try:
#                 await self.bot.voice_clients[0].disconnect()
#                 self.voice_client = ""
#             except:
#                 pass
        
#     @app_commands.command(name="재생목록", description="재생목록을 불러옵니다")
#     async def call_queue(self, interaction: discord.Interaction):
#         await interaction.response.send_message(f'재생목록 {self.queue}')

#     @app_commands.command(name="일시정지", description="재생을 일시정지합니다")
#     async def pause(self, interaction: discord.Interaction):
#         try:
#             self.bot.voice_clients[0].pause()
#             await interaction.response.send_message("음악이 일시정지 되었습니다")
#         except:
#             await interaction.response.send_message("봇이 통화방에 없습니다")

#     @app_commands.command(name="스킵", description="현재 음악을 스킵합니다")
#     async def skip(self, interaction: discord.Interaction):
#         try:
#             if self.voice_client.is_playing() or self.voice_client.is_paused():
#                 self.voice_client.stop()
#                 await interaction.response.send_message("음악이 스킵되었습니다")
#             else:
#                 await interaction.response.send_message("스킵할 음악이 없습니다")
#         except:
#             await interaction.response.send_message("봇이 통화방에 없습니다")

#     @app_commands.command(name="재개", description="재생을 재개합니다")
#     async def resume(self, interaction: discord.Interaction):
#         try:
#             self.bot.voice_clients[0].resume()
#             await interaction.response.send_message("음악을 재개합니다")
#         except:
#             await interaction.response.send_message("봇이 통화방에 없습니다")

#     @app_commands.command(name="퇴장", description="통화방에서 나갑니다")
#     async def leave(self, interaction: discord.Interaction):
#         try:
#             await self.bot.voice_clients[0].disconnect()
#             await interaction.response.send_message("퇴장합니다")
#             self.voice_client = ""
#         except:
#             await interaction.response.send_message("봇이 통화방에 없습니다")