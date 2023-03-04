import discord
from discord import app_commands
from discord.ext import commands, tasks
import pymongo
import json
import os
from discord.ext.commands import has_permissions, MissingPermissions
list_dev_id = ["339767912841871360", "474389454262370314", "393932860597338123", "185181025104560128"]
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
class GuildData(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.data = self.get_json()
        print(self.data)
        self.repeat_save_guild.start()

    @commands.Cog.listener()
    async def on_ready(self):
        print("준비됨")

    def set_json(self):
        """_summary_
            guilds JSON 에 self.data를 덮어씌움.
        """
        try:
            with open(os.path.join(__location__ + '\\json\\guilds.json'), "w") as file:
                file.write(json.dump(self.data, file, indent=4))
        except TypeError:
            pass

    def get_json(self) -> dict:
        """_summary_
            guilds JSON 파일을 불러와서 return함
        return Dict
        """
        with open(os.path.join(f"{__location__}\\json\\guilds.json"),'r',encoding='utf-8') as file:
            return json.load(file)
            
    def check_guild(self, guild_id: str):
        """_summary_
            만약 해당 str(guild.id)가 self.data에 없다면 추가함.
        Args:
            guild_id (str, 필수): 해당 guild의 id
        """
        if guild_id not in self.data:
            self.data[guild_id] = {
                    "welcome" : None,
                    "warnLimit": 3,
                    "warned": {   
                    }
                }
            print(f"{guild_id}를 추가함")
        else:
            pass

    def check_user(self, guild_id: str ,user_id: str):
        """_summary_
            유저가 해당 길드에서 경고를 받았었는지 확인. 
            없으면 새로 추가
        Args:
            guild_id (str, 필수): 해당 guild id 
            user_id (str, 필수): 유저 id 
        """
        if user_id not in self.data[guild_id]["warned"]:
            self.data[guild_id]["warned"][user_id] = {
                    "warning": 0
                }
        else:
            pass
    
    @app_commands.command(name="경고한도", description="경고 한도를 설정합니다, 경고한도 초과시 관리자에게 알림 /경고한도 (경고 수)")
    @app_commands.checks.has_permissions(kick_members=True)
    async def warnLimit(self, interaction: discord.Interaction, warn_number: int) -> None: 
        """_summary_
            서버의 경고 한도를 설정함. self.data에 저장
        Args:
            interaction (discord.Interaction): interaction 생성
            warn_number (int, 필수): 경고 한도
        """
        #await ctx.invoke(self.bot.get_command('핑'))
        self.check_guild(str(interaction.guild.id))
        self.data[str(interaction.guild.id)]["warnLimit"] = warn_number   

        embed=discord.Embed(title=f"경고 한도를 {warn_number}로 저장했느니라", description="경고 한도 초과시 관리자가 즉시 조치를 취할 수 있도록 하는 기능이니라", color=0x666666)
        embed.set_author(name="냥이", icon_url="https://i.imgur.com/ORq6ORB.jpg")
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="경고", description="해당 유저에게 경고 1회를 부여하는 것 이니라 /경고 (멘션or닉네임) (사유)")
    @app_commands.checks.has_permissions(kick_members=True)
    
    async def warn(self, interaction: discord.Interaction, user: discord.Member, reason: str = "사유 없음") -> None: 
        """_summary_
            해당 유저에게 경고 1회 부여하고 self.data에 이를 저장함 (*사유는 저장되지 않음)
            kick_member 권한을 갖고 있거나 그 상위 권한을 갖은 관리자만 실행 가능
        Args:
            interaction (discord.Interaction): interaction 생성
            user (discord.Member, 필수): 해당 유저
            reason (str, 옵션): 경고 받은 사유 Defaults to "사유 없음".
        """
        self.check_guild(str(interaction.guild.id))
        self.check_user(str(interaction.guild.id), str(user.id))
        self.data[str(interaction.guild.id)]["warned"][str(user.id)]["warning"] += 1

        embed=discord.Embed(title=f"{user.name} (이)에게 경고 1회를 부여 하였느니라", description=f"사유: {reason}", color=0x666666)
        embed.set_author(name="냥이", icon_url="https://i.imgur.com/ORq6ORB.jpg")

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="경고경감", description="해당 유저의 경고 1회를 경감하는 것 이니라 /경고경감 (멘션or닉네임) (사유)")
    @app_commands.checks.has_permissions(kick_members=True)
    async def warn_reduce(self, interaction: discord.Interaction, user: discord.Member, reason: str = "사유 없음") -> None: 
        """_summary_
            해당 유저의 경고를 1회 줄여주고 self.data에 이를 저장함 (*사유는 저장되지 않음)
            kick_member 권한을 갖고 있거나 그 상위 권한을 갖은 관리자만 실행 가능
        Args:
            interaction (discord.Interaction): interaction 생성
            user (discord.Member, 필수): 해당 유저
            reason (str, 옵션): 경고 경감 사유 Defaults to "사유 없음".
        """
        self.check_guild(str(interaction.guild.id))
        self.check_user(str(interaction.guild.id), str(user.id))
        self.data[str(interaction.guild.id)]["warned"][str(user.id)]["warning"] -= 1

        embed=discord.Embed(title=f"{user.name} (이)의 경고 1회를 줄였느니라", description=f"사유: {reason}", color=0x666666)
        embed.set_author(name="냥이", icon_url="https://i.imgur.com/ORq6ORB.jpg")

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="경고확인", description="경고 받은 유저 확인 /경고확인 유저 멘션")
    async def checkwarn(self, interaction: discord.Interaction, user: discord.Member) -> None:
        """_summary_
        해당 유저 혹은 전체 유저 경고 확인
        Args:
            interaction (discord.Interaction): interaction
            user (discord.Member, 옵션): user멘션 혹은 닉네임
        """
        warned_num = self.data[str(interaction.guild.id)]["warned"][str(user.id)]["warning"]
        embed = discord.Embed(title=f"{user.name}(이)는 {warned_num}번 경고를 받았느니라", description="조심하거라 찌든 때 같은 것아",color=0x666666)
        embed.set_author(name="냥이", icon_url="https://i.imgur.com/ORq6ORB.jpg")

        await interaction.response.send_message(embed=embed)


    @app_commands.command(name="경고목록", description="경고 받은 유저들 목록 /경고목록 (유저 멘션/ 없을시 전체)")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def check_all_warn(self, interaction: discord.Interaction) -> None:
        """_summary_
        모든 유저 경고 확인
        Args:
            interaction (discord.Interaction): interaction
        """
        warned_list = {}
        for user_id in self.data[str(interaction.guild.id)]["warned"].items():
            user_call = await self.bot.fetch_user(user_id[0])
            user_name = user_call.name
            user_warned = self.data[str(interaction.guild.id)]["warned"][user_id[0]]["warning"]
            warned_list[user_name]= user_warned

        embed = discord.Embed(title="경고를 받은 모든 멤버이니라", color=0x666666)
        embed.set_author(name="냥이", icon_url="https://i.imgur.com/ORq6ORB.jpg")
        for id, warned in warned_list.items():
            embed.add_field(name=id, value=warned)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="환영켜기", description="해당 채널에 환영 인사를 합니다 /환영켜기")
    async def welcome_activate(self, interaction: discord.Interaction) -> None:
        """_summary_
        해당 태널에 환영인사를 보내게 활성화
        Args:
            interaction (discord.Interaction): interaction
        """
        self.data[str(interaction.guild.id)]["welcome"] = str(interaction.channel.id)
        embed=discord.Embed(title="해당 Text 채널에서 인사를 하겠느니라!", color=0xebe6e6)
        embed.set_author(name="랑이", icon_url="https://i.imgur.com/huDPd5o.jpg")
        await interaction.response.send_message(embed=embed)
        
    @app_commands.command(name="환영끄기", description="환영 인삿말 끄기 /환영끄기")
    async def welcome_deactivate(self, interaction: discord.Interaction) -> None:
        """_summary_
        해당 태널에  비활성화
        Args:
            interaction (discord.Interaction): interaction
        """
        self.data[str(interaction.guild.id)]["welcome"] = None
        embed=discord.Embed(title="인사를 멈추도록 하겠느니라!", color=0xebe6e6)
        embed.set_author(name="랑이", icon_url="https://i.imgur.com/huDPd5o.jpg")
        await interaction.response.send_message(embed=embed)
        
    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel=member.guild.get_channel(int(self.data[str(member.guild.id)]["welcome"]))
        print(channel)
        try:
            embed=discord.Embed(title=f"{member.guild.name} 서버에 온걸 환영하느니라!", color=0xebe6e6)
            embed.set_thumbnail(url=member.avatar.url)
            embed.set_author(name="랑이", icon_url="https://i.imgur.com/huDPd5o.jpg")
            embed.add_field(name=f"{member.guild.name}", value=f"{member.mention}(야)아 {member.guild.name} 서버에 온것을 환영하느니라!!", inline=False)
            embed.add_field(name="서버 총괄", value=f"문의 또는 질문은 서버 총괄을 담당하는 {member.guild.owner.mention}에게 물어보거라!", inline=False)
            embed.set_footer(text="나와 아해들 디스코드 봇")
            await channel.send(embed=embed)
        except:
            pass


    @commands.command(name=";저장")
    async def savecommand(self, ctx):
        """self.data에 있는 모든 유저 정보를 JSON에 수동으로 저장
            *개발자 전용
        Args:
            ctx (_type_): 메세지 Context
        """
        if str(ctx.author.id) in list_dev_id:
            self.set_json()
            await ctx.send("저장되었습니다.")
        else:
            pass
        
    @commands.Cog.listener()
    async def on_disconnect(self):
        """disconnect시 self.data 자동 저장
        """
        self.set_json()
        
    @tasks.loop(seconds=30)
    async def repeat_save_guild(self):
        """30초 마다 self.data를 JSON파일에 자동저장하고 해당 파일에서 data를 불러옴.
        """
        self.set_json()
        self.data = self.get_json() #필수 코드 아님.

async def setup(bot):
    await bot.add_cog(GuildData(bot))
    
