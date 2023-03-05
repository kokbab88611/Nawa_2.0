import asyncio
import discord
from discord import app_commands
from discord.ext import commands
import typing
import wavelink
import os
import random

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

class Music(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.queue = []
        self.loops = False
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
        self.queue = []

    @app_commands.command(name="재생", description="음악을 재생합니다")
    async def play(self, interaction: discord.Interaction, search: str):
        search = await wavelink.YouTubeTrack.search(query=search, return_first=True)
        if not interaction.guild.voice_client:
            try:
                vc: wavelink.Player = await interaction.user.voice.channel.connect(cls=wavelink.Player)
            except:
                return await interaction.response.send_message("먼저 통화방에 접속해 주십시오")
        else:
            vc: wavelink.Player = interaction.guild.voice_client

        self.queue.append(search)
        await interaction.response.send_message(f'{search}이/가 재생목록에 추가되었습니다')

        if not vc.is_playing() and not vc.is_paused():
            while len(self.queue) > 0:
                await vc.play(self.queue[0])
                while vc.is_playing() or vc.is_paused():
                    await asyncio.sleep(0.1)
                if not self.loops:
                    self.queue.pop(0)

    @app_commands.command(name="재생목록", description="재생목록을 불러옵니다")
    async def play_list(self, interaction: discord.Interaction):
        msg = ""
        if len(self.queue) > 0:
            for num, title in enumerate(self.queue):
               msg += f'{num}: {title}\n'
            await interaction.response.send_message(msg)
        else:
            await interaction.response.send_message("재생목록이 비어있습니다")

    @app_commands.command(name="루프", description="재생중인 음악을 반복합니다")
    async def loop(self, interaction: discord.Interaction):
        node = wavelink.NodePool.get_node()
        player = node.get_player(interaction.guild)

        if player is None:
            return await interaction.response.send_message("음악봇이 통화방에 없습니다")

        if player.is_playing() or player.is_paused():
            if self.loops:
                self.loops = False
                await interaction.response.send_message("음악 반복을 정지합니다")
            else:
                self.loops = True
                await interaction.response.send_message("현재 음악을 반복합니다")
        else:
            await interaction.response.send_message("음악 재생중이 아닙니다")

    @app_commands.command(name="스킵", description="재생중인 음악을 스킵합니다")
    async def stop(self, interaction: discord.Interaction):
        node = wavelink.NodePool.get_node()
        player = node.get_player(interaction.guild)

        if player is None:
            return await interaction.response.send_message("음악봇이 통화방에 없습니다")

        if player.is_playing():
            if player.is_paused():
                await player.resume()
            self.loops = False
            await player.stop()
            return await interaction.response.send_message("음악이 스킵되었습니다")
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
            return await interaction.response.send_message("음악이 이미 재생중이거나 재생중인 음악이 없습니다")

async def setup(bot):
    await bot.add_cog(Music(bot))
