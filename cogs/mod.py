import discord
from discord import app_commands, Member
from discord.ext import commands, tasks
from datetime import datetime, timedelta
from discord.ext.commands import has_permissions, MissingPermissions

class Moderator(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("준비됨")

    @app_commands.command(name="강퇴", description="강퇴할 유저를 선택합니다 /강퇴 (닉네임or맨션) (사유)")
    @app_commands.checks.has_permissions(kick_members=True)
    async def kickuser(self, interaction: discord.Interaction, user: discord.Member, *, reason: str = "사유 없음") -> None:
        embedChannel = discord.Embed(title=f"{user.name}(이)를 강퇴했습니다", description=f"사유: {reason}", color=0xb0a7d3)
        embedChannel.set_author(name="관리자 세희", icon_url="https://i.imgur.com/7a4oeOi.jpg")

        embedUser = embed = discord.Embed(title=f"{interaction.guild.name}에서 강퇴 되셨습니다", description=f"사유: {reason}",
                                          color=0xb0a7d3)
        embed.set_author(name="관리자 세희", icon_url="https://i.imgur.com/7a4oeOi.jpg")

        await user.send(embed=embedUser)
        await user.kick(reason=reason)
        await interaction.response.send_message(embed=embedChannel)

    @app_commands.command(name="차단", description="차단할 유저를 선택하고 해당 유저의 메세지를 삭제합니다 /차단 (닉네임or맨션) (X일 메세지 삭제) (사유)")
    @app_commands.checks.has_permissions(ban_members=True)
    async def banUser(self, interaction: discord.Interaction, user: discord.Member, *, reason: str = "사유 없음",
                      delete_message_days: int = 0) -> None:

        embedChannel = discord.Embed(title=f"{user.name}(이)를 차단했습니다", description=f"사유: {reason}", color=0xb0a7d3)
        embedChannel.set_author(name="관리자 세희", icon_url="https://i.imgur.com/7a4oeOi.jpg")

        embedUser = embed = discord.Embed(title=f"{interaction.guild.name}에서 차단 되셨습니다", description=f"사유: {reason}",
                                          color=0xb0a7d3)
        embed.set_author(name="관리자 세희", icon_url="https://i.imgur.com/7a4oeOi.jpg")

        await user.send(embed=embedUser)
        await user.ban(reason=reason, delete_message_days=delete_message_days)
        await interaction.response.send_message(embed=embedChannel)

    @app_commands.command(name="차단해제", description="차단해제할 유저를 선택합니다 /차단해제 (닉네임or맨션) (사유)")
    @app_commands.checks.has_permissions(ban_members=True)
    async def unbanUser(self, interaction: discord.Interaction, user: str, *, reason: str = "사유 없음") -> None:
        print("발동")
        async for entry in interaction.guild.bans(limit=100):
            if str(entry.user) == user:
                await interaction.guild.unban(entry.user, reason=reason)
                embed = discord.Embed(title=f"{entry.user}(이)의 차단을 해제했습니다", description=f"사유: {reason}", color=0xb0a7d3)
                embed.set_author(name="관리자 세희", icon_url="https://i.imgur.com/7a4oeOi.jpg")

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="챗방", description="채팅방을 생성합니다 /챗방 (이름) (주제) (NSFW여부 TRUE 혹은 FALSE)")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def createText(self, interaction: discord.Interaction, name: str, *, topic: str = None,
                         nsfw: bool = False) -> None:
        embed = discord.Embed(title=f"{name} 대화방 생성 완료", color=0xb0a7d3)
        embed.set_author(name="관리자 세희", icon_url="https://i.imgur.com/7a4oeOi.jpg")
        embed.add_field(name="주제", value=f"{topic}", inline=True)
        embed.add_field(name="NSFW", value=f"{nsfw}", inline=True)

        await interaction.guild.create_text_channel(name=name, topic=topic, nsfw=nsfw)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="통화방", description="통화방을 생성합니다 /통화방 (이름) (유저제한 숫자 없을시 제한없음)")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def createCall(self, interaction: discord.Interaction, name: str, user_limit: int = 0) -> None:
        await interaction.guild.create_voice_channel(name=name, user_limit=user_limit)
        if user_limit == 0:
            user_limit = "없음"
        embed = discord.Embed(title=f"{name} 통화방 생성 완료", color=0xb0a7d3)
        embed.set_author(name="관리자 세희", icon_url="https://i.imgur.com/7a4oeOi.jpg")
        embed.add_field(name="유저 제한", value=f"{user_limit}", inline=True)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="삭제", description="메세지를 삭제합니다 /삭제 (제한) (사유)")
    @app_commands.checks.has_permissions(manage_messages=True)
    # @commands.cooldown(1, 5, commands.BucketType.user)
    async def deleteMessage(self, interaction: discord.Interaction, limit: int, *, reason: str = "사유 없음") -> None:

        delete = await interaction.channel.purge(limit=limit + 1)
        print("디퍼")
        await interaction.response.defer()
        embed = discord.Embed(title=f"{len(delete)}개의 메세지를 묵사발 냈습니다", description=f"사유: {reason}", color=0xb0a7d3)
        embed.set_author(name="관리자 세희", icon_url="https://i.imgur.com/7a4oeOi.jpg")

        await interaction.followup.send(embeds=embed, ephemeral=True)

    @app_commands.command(name="타임아웃", description="통화방 접속과 채팅을 특정 시간동안 금지 시킵니다 /타임아웃 (닉네임or맨션) (초) (사유)")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def TimeOutUser(self, interaction: discord.Interaction, user: discord.Member, *, reason: str = "사유 없음",
                              sec: int, min: int = 0, hour: int = 0, day: int = 0) -> None:
            now = datetime.now().astimezone()
            till = now + timedelta(seconds=sec, minutes=min, hours=hour)
            bantime = timedelta(seconds=sec, minutes=min, hours=hour, days=day)
            print(bantime.seconds)

            embedChannel = discord.Embed(
                title=f"{user.name}이 {bantime.days}일 {bantime.seconds // 60 // 60}시간 {(bantime.seconds // 60) % 60}분 {bantime.seconds % 60}초 동안 타임아웃 처리되었습니다",
                description=f"사유: {reason}", color=0xb0a7d3)
            embedChannel.set_author(name="관리자 세희", icon_url="https://i.imgur.com/7a4oeOi.jpg")
            embedUser = discord.Embed(
                title=f"{interaction.guild.name}에서 {bantime.days}일 {bantime.seconds // 60 // 60}시간 {(bantime.seconds // 60) % 60}분 {bantime.seconds % 60}초 동안 타임아웃 처리되었습니다",
                description=f"사유: {reason}", color=0xb0a7d3)
            embedUser.set_author(name="관리자 세희", icon_url="https://i.imgur.com/7a4oeOi.jpg")

            await user.send(embed=embedUser)
            await interaction.response.send_message(embed=embedChannel)
            await user.timeout(till, reason=reason)

    @app_commands.command(name="사면", description="해당 유저의 타임아웃을 해제합니다 /차단 (닉네임or맨션) (사유)")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def unTimeout(self, interaction: discord.Interaction, user: discord.Member, *, reason: str = "사유 없음") -> None:

        embedChannel = discord.Embed(title=f"{user.name}(이)를 사면했습니다", description=f"사유: {reason}", color=0xb0a7d3)
        embedChannel.set_author(name="관리자 세희", icon_url="https://i.imgur.com/7a4oeOi.jpg")
        embedUser = discord.Embed(title=f"{interaction.guild.name}에서 타임아웃이 해제되셨습니다", description=f"사유: {reason}",
                                  color=0xb0a7d3)
        embedUser.set_author(name="관리자 세희", icon_url="https://i.imgur.com/7a4oeOi.jpg")

        await user.send(embed=embedUser)
        await interaction.response.send_message(embed=embedChannel)
        await user.timeout(None, reason=reason)

    @commands.hybrid_command(with_app_command=True)
    async def test(self, ctx):
        await ctx.send("This is a hybrid command!")

    #ERROR
    @kickuser.error
    @banUser.error
    @unbanUser.error
    @createCall.error
    @createText.error
    @unTimeout.error
    @TimeOutUser.error
    @deleteMessage.error
    async def error(self, interaction: discord.Interaction, error):
        embed=discord.Embed(title="기어오르지 마시기 바랍니다...", description="관리자 권한을 들고 오십쇼", color=0xb0a7d3)
        embed.set_author(name="관리자 세희", icon_url="https://i.imgur.com/7a4oeOi.jpg")
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Moderator(bot))

