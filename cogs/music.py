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
<<<<<<< Updated upstream
#         bot.loop.create_task(self.create_nodes())
=======
        self.nodeid = None
        bot.loop.create_task(self.create_nodes())
>>>>>>> Stashed changes

    async def cog_load(self):
        await self.create_nodes()
        
    async def create_nodes(self):
<<<<<<< Updated upstream
#         await self.bot.wait_until_ready()
        self.node:wavelink.Node = await wavelink.NodePool.create_node(bot=self.bot, host="127.0.0.1", port="2333", password="youshallnotpass", region="asia")
=======
        await self.bot.wait_until_ready()
        node: wavelink.Node = wavelink.Node(uri='http://localhost:2333', password='youshallnotpass')
        await wavelink.NodePool.connect(client=self.bot, nodes=[node])
        self.nodeid = node.id
>>>>>>> Stashed changes

    @app_commands.command(name="입장", description="음악봇이 입장합니다")
    async def joincommand_kor(self, interaction: discord.Interaction, channel: typing.Optional[discord.VoiceChannel]):
        await self.join(interaction, channel)

    @app_commands.command(name="j", description="음악봇이 입장합니다")
    async def joincommand(self, interaction: discord.Interaction, channel: typing.Optional[discord.VoiceChannel]):
        await self.join(interaction, channel)
           
    async def join(self, interaction: discord.Interaction, channel: typing.Optional[discord.VoiceChannel]):
        if channel is None:
            try:
                channel = interaction.user.voice.channel
            except:
                return await interaction.response.send_message("먼저 통화방에 접속해 주십시오")
        
<<<<<<< Updated upstream
#         node = wavelink.NodePool.get_node()
        player = self.node.get_player(interaction.guild)
=======
        node = wavelink.NodePool.get_node(self.nodeid)
        player = node.get_player(interaction.guild.id)
>>>>>>> Stashed changes

        if player is not None:
            if player.is_connected():
                return await interaction.response.send_message("이미 봇이 통화방에 있습니다")
        
        await channel.connect(cls=wavelink.Player)
        await interaction.response.send_message(f'{channel.name}에 입장하였습니다')

    @app_commands.command(name="퇴장", description="음악봇이 퇴장합니다")
    async def quitcommand_kor(self, interaction: discord.Interaction):
        await self.leave(interaction)

    @app_commands.command(name="q", description="음악봇이 퇴장합니다")
    async def quitcommand(self, interaction: discord.Interaction):
        await self.leave(interaction)

    async def leave(self, interaction: discord.Interaction):
<<<<<<< Updated upstream
#         node = wavelink.NodePool.get_node()
        player = self.node.get_player(interaction.guild)
=======
        node = wavelink.NodePool.get_node(self.nodeid)
        player = node.get_player(interaction.guild.id)
>>>>>>> Stashed changes

        if player is None:
            return await interaction.response.send_message("음악봇이 통화방에 없습니다")
        await player.disconnect()
        await interaction.response.send_message("음악봇이 퇴장하였습니다")
        self.queue = []

    @app_commands.command(name="재생", description="음악을 재생합니다")
    async def playcommand_kor(self, interaction: discord.Interaction, search: str):
        await self.play(interaction, str(search))

    @app_commands.command(name="p", description="음악을 재생합니다")
    async def playcommand(self, interaction: discord.Interaction, search: str):
        await self.play(interaction, str(search))

<<<<<<< Updated upstream
    async def play(self, interaction: discord.Interaction, search: wavelink.YouTubeTrack):
#         if search.startswith("https"):
#             try:
#                 search = search.split("&")[0]
#             except: 
#                 pass
#         search = await wavelink.YouTubeTrack.search(query=search, return_first=True)
=======
    async def play(self, interaction: discord.Interaction, search: str):
        if search.startswith("https"):
            try:
                search = search.split("&")[0]
            except: 
                pass
        search = await wavelink.YouTubeTrack.search(search, return_first=True)

>>>>>>> Stashed changes
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
    async def playlistcommand_kor(self, interaction: discord.Interaction):
        await self.play_list(interaction)

    @app_commands.command(name="pl", description="재생목록을 불러옵니다")
    async def playlistcommand(self, interaction: discord.Interaction):
        await self.play_list(interaction)

    async def play_list(self, interaction: discord.Interaction):
        msg = ""
        if len(self.queue) > 0:
            for num, title in enumerate(self.queue):
               msg += f'{num}: {title}\n'
            await interaction.response.send_message(msg)
        else:
            await interaction.response.send_message("재생목록이 비어있습니다")

    @app_commands.command(name="루프", description="재생중인 음악을 반복합니다")
    async def loopcommand_kor(self, interaction: discord.Interaction):
        await self.loop(interaction)

    @app_commands.command(name="l", description="재생중인 음악을 반복합니다")
    async def loopcommand(self, interaction: discord.Interaction):
        await self.loop(interaction)

    async def loop(self, interaction: discord.Interaction):
        node = wavelink.NodePool.get_node(self.nodeid)
        player = node.get_player(interaction.guild.id)

        if not player:
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
    async def skipcommand_kor(self, interaction: discord.Interaction):
        await self.skip(interaction)

    @app_commands.command(name="s", description="재생중인 음악을 스킵합니다")
    async def skipcommand(self, interaction: discord.Interaction):
        await self.skip(interaction)

    async def skip(self, interaction: discord.Interaction):
<<<<<<< Updated upstream
#         node = wavelink.NodePool.get_node()
        player = self.node.get_player(interaction.guild)
=======
        node = wavelink.NodePool.get_node(self.nodeid)
        player = node.get_player(interaction.guild.id)
>>>>>>> Stashed changes

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
    async def pausecommand_kor(self, interaction: discord.Interaction):
        await self.pause(interaction)

    @app_commands.command(name="pp", description="음악 재생을 일시정지합니다")
    async def pausecommand(self, interaction: discord.Interaction):
        await self.pause(interaction)

    async def pause(self, interaction: discord.Interaction):
<<<<<<< Updated upstream
#         node = wavelink.NodePool.get_node()
        player = self.node.get_player(interaction.guild)
=======
        node = wavelink.NodePool.get_node(self.nodeid)
        player = node.get_player(interaction.guild.id)
>>>>>>> Stashed changes

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
    async def resumecommand_kor(self, interaction: discord.Interaction):
        await self.resume(interaction)

    @app_commands.command(name="r", description="음악 재생을 재개합니다")
    async def resumecommand(self, interaction: discord.Interaction):
        await self.resume(interaction)

    async def resume(self, interaction: discord.Interaction):
<<<<<<< Updated upstream
#         node = wavelink.NodePool.get_node()
        player = self.node.get_player(interaction.guild)
=======
        node = wavelink.NodePool.get_node(self.nodeid)
        player = node.get_player(interaction.guild.id)
>>>>>>> Stashed changes

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
