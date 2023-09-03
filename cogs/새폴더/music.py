import asyncio
import discord
from discord import app_commands
from discord.ext import commands
import typing
import wavelink
import os
import random
from discord.ui import Button, View

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

class MusicPlayerButtons(Button):
    def __init__(self, label, button_style, custom_id, embed, self_):
        super().__init__(label=label, style=button_style, custom_id=custom_id)
        self.custom_id=str(custom_id)
        self.embed=embed
        self.self_ = self_

    async def pause(self, interaction):
        await Music.pause(self.self_, interaction)

    async def resume(self, interaction):
        await Music.resume(self.self_, interaction)

    async def skip(self, interaction):
        await Music.skip(self.self_, interaction)

    async def loop(self, interaction):
        await Music.loop(self.self_, interaction)

    async def callback(self, interaction):
        if self.custom_id == "pause":
            await MusicPlayerButtons.pause(self, interaction)
        elif self.custom_id == "resume":
            await MusicPlayerButtons.resume(self, interaction)
        elif self.custom_id == "skip":
            await MusicPlayerButtons.skip(self, interaction)
        elif self.custom_id == "loop":
            await MusicPlayerButtons.loop(self, interaction)
        else:
            return

class Music(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.queue = {}
        self.authors = {}
        self.loops = {}
        self.server_voicechannel = {}
        self.channels = {}
        self.nodeid = None
        bot.loop.create_task(self.create_nodes())

    async def create_nodes(self):
        await self.bot.wait_until_ready()
        node: wavelink.Node = wavelink.Node(uri='67.10.105.48:2333', password='youshallnotpass')
        await wavelink.NodePool.connect(client=self.bot, nodes=[node])
        self.nodeid = node.id

    @app_commands.command(name="입장", description="음악봇이 입장합니다")
    async def joincommand_kor(self, interaction: discord.Interaction, channel: typing.Optional[discord.VoiceChannel]):
        await self.join(interaction, channel)

    @app_commands.command(name="j", description="음악봇이 입장합니다")
    async def joincommand(self, interaction: discord.Interaction, channel: typing.Optional[discord.VoiceChannel]):
        await self.join(interaction, channel)
           
    async def join(self, interaction: discord.Interaction, channel: typing.Optional[discord.VoiceChannel]):
        if channel is None:
            try:
                self.server_voicechannel[interaction.guild.id] = interaction.user.voice.channel.id
                channel = interaction.user.voice.channel
            except:
                return await interaction.response.send_message("먼저 통화방에 접속해 주십시오")
        
        node = wavelink.NodePool.get_node(self.nodeid)
        player = node.get_player(interaction.guild.id)

        if player is not None:
            try:
                if player.is_connected():
                    return await interaction.response.send_message("이미 봇이 통화방에 있습니다")
            except:
                return await interaction.response.send_message("이미 봇이 다른 통화방에 있습니다")
        
        await channel.connect(cls=wavelink.Player)
        await interaction.response.send_message(f'{channel.name}에 입장하였습니다')

    @app_commands.command(name="퇴장", description="음악봇이 퇴장합니다")
    async def quitcommand_kor(self, interaction: discord.Interaction):
        await self.leave(interaction)

    @app_commands.command(name="q", description="음악봇이 퇴장합니다")
    async def quitcommand(self, interaction: discord.Interaction):
        await self.leave(interaction)

    async def leave(self, interaction: discord.Interaction):
        node = wavelink.NodePool.get_node(self.nodeid)
        player = node.get_player(interaction.guild.id)

        if player is None:
            return await interaction.response.send_message("음악봇이 통화방에 없습니다")
        await player.disconnect()
        await interaction.response.send_message("음악봇이 퇴장하였습니다")
        self.queue[interaction.guild.id] = []

    @app_commands.command(name="재생", description="음악을 재생합니다")
    async def playcommand_kor(self, interaction: discord.Interaction, search: str):
        await self.play(interaction, str(search))

    @app_commands.command(name="p", description="음악을 재생합니다")
    async def playcommand_p(self, interaction: discord.Interaction, search: str):
        await self.play(interaction, str(search))

    @app_commands.command(name="ㅔ", description="음악을 재생합니다")
    async def playcommand_short(self, interaction: discord.Interaction, search: str):
        await self.play(interaction, str(search))

    async def play(self, interaction: discord.Interaction, search: str):
        if search.startswith("https"):
            try:
                search = search.split("&")[0]
            except: 
                pass

        search = await wavelink.YouTubeTrack.search(search)
        search = search[0]

        if not interaction.guild.voice_client:
            try:
                self.server_voicechannel[interaction.guild.id] = interaction.user.voice.channel.id
                vc: wavelink.Player = await interaction.user.voice.channel.connect(cls=wavelink.Player)
            except:
                return await interaction.response.send_message("먼저 통화방에 접속해 주십시오")
        else:
            vc: wavelink.Player = interaction.guild.voice_client

        if interaction.guild.id in self.queue:
            self.queue[interaction.guild.id].append(search)
            self.authors[interaction.guild.id].append(interaction.user.display_name)
            self.channels[interaction.guild.id].append(interaction.channel)          
        else:
            self.queue[interaction.guild.id] = []
            self.authors[interaction.guild.id] = []
            self.channels[interaction.guild.id] = []         
            self.queue[interaction.guild.id].append(search)
            self.authors[interaction.guild.id].append(interaction.user.display_name)
            self.channels[interaction.guild.id].append(interaction.channel)
   
        await interaction.response.send_message(f'{search}이/가 재생목록에 추가되었습니다')

        if not vc.is_playing() and not vc.is_paused():
            while len(self.queue[interaction.guild.id]) > 0:
                
                duration = self.queue[interaction.guild.id][0].length
                duration /= 1000
                durationmin = duration // 60
                durationsec = duration % 60
                embed=discord.Embed(title = self.queue[interaction.guild.id][0], url=self.queue[interaction.guild.id][0].uri,description=self.queue[interaction.guild.id][0].author)
                embed.set_thumbnail(url = self.queue[interaction.guild.id][0].thumbnail)
                embed.add_field(name=f"00:00 ~ {int(durationmin)}:{int(durationsec)}", inline=True)
                embed.set_footer(text=self.authors[interaction.guild.id][0])

                view = View()
                view.add_item(MusicPlayerButtons('↻', discord.ButtonStyle.gray, "loop", embed, self))
                view.add_item(MusicPlayerButtons('II', discord.ButtonStyle.red, "pause", embed, self))
                view.add_item(MusicPlayerButtons('▷', discord.ButtonStyle.green, "resume", embed, self))
                view.add_item(MusicPlayerButtons('▷▷', discord.ButtonStyle.gray, "skip", embed, self))

                await self.channels[interaction.guild.id][0].send(embed=embed, view=view)
                await vc.play(self.queue[interaction.guild.id][0])

                del self.authors[interaction.guild.id][0]
                del self.channels[interaction.guild.id][0]

                while vc.is_playing() or vc.is_paused():
                    await asyncio.sleep(5)
                    #5초마다 노래가 끝났는지 아닌지 확인
                try:
                    if not self.loops[interaction.guild.id]:
                    #사람이 있는지 없는지 확인 후 통화방 나가기
                        self.queue[interaction.guild.id].pop(0)
                except KeyError:
                    self.queue[interaction.guild.id].pop(0)
                    #사람이 있는지 없는지 확인 후 통화방 나가기

        self.loops[interaction.guild.id] = False
        
    @app_commands.command(name="재생목록", description="재생목록을 불러옵니다")
    async def playlistcommand_kor(self, interaction: discord.Interaction):
        await self.play_list(interaction)

    @app_commands.command(name="pl", description="재생목록을 불러옵니다")
    async def playlistcommand(self, interaction: discord.Interaction):
        await self.play_list(interaction)

    async def play_list(self, interaction: discord.Interaction):
        msg = ""
        try:
            if len(self.queue[interaction.guild.id]) > 0:
                play_list = None
                for num, title in enumerate(self.queue[interaction.guild.id]):
                    msg += f'{num}: {title}\n'
                    
                await interaction.response.send_message(msg)
            else:
                await interaction.response.send_message("재생목록이 비어있습니다")
        except KeyError:
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

        if player is None:
            return await interaction.response.send_message("음악봇이 통화방에 없습니다")

        if player.is_playing() or player.is_paused():
            if self.loops[interaction.guild.id]:
                self.loops[interaction.guild.id] = False
                await interaction.response.send_message("음악 반복을 정지합니다")
            else:
                self.loops[interaction.guild.id] = True
                await interaction.response.send_message("현재 음악을 반복합니다")
        else:
            await interaction.response.send_message("음악 재생중이 아닙니다")

    @app_commands.command(name="스킵", description="재생중인 음악을 스킵합니다")
    async def skipcommand_kor(self, interaction: discord.Interaction):
        await self.skip(interaction)

    @app_commands.command(name="s", description="재생중인 음악을 스킵합니다")
    async def skipcommand_short(self, interaction: discord.Interaction):
        await self.skip(interaction)

    @app_commands.command(name="ㄴ", description="재생중인 음악을 스킵합니다")
    async def skipcommand_s(self, interaction: discord.Interaction):
        await self.skip(interaction)

    async def skip(self, interaction: discord.Interaction):
        node = wavelink.NodePool.get_node(self.nodeid)
        player = node.get_player(interaction.guild.id)

        if player is None:
            return await interaction.response.send_message("음악봇이 통화방에 없습니다")

        if player.is_playing():
            if player.is_paused():
                await player.resume()
            self.loops[interaction.guild.id] = False
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
        node = wavelink.NodePool.get_node(self.nodeid)
        player = node.get_player(interaction.guild.id)

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
        node = wavelink.NodePool.get_node(self.nodeid)
        player = node.get_player(interaction.guild.id)

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

    # @app_commands.command(name="말해", description="tts입니다")
    # async def text_to_speech(self, interaction: discord.Interaction, text: str):
    #     node = wavelink.NodePool.get_node(self.nodeid)
    #     vc = node.get_player(interaction.guild.id)

    #     channel = interaction.user.voice.channel
    #     tts = gTTS(text=text, lang="ko")
    #     tts.save(os.path.join(f"{__location__}\\TTS\\text.mp3"))

    #     if not interaction.guild.voice_client:
    #         vc = await channel.connect()

    #     vc.play(discord.FFmpegPCMAudio(os.path.join(f"{__location__}\\TTS\\text.mp3")))
    #     await interaction.response.send_message("말하는중")

async def setup(bot):
    await bot.add_cog(Music(bot))
