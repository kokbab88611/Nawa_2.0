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
                print(self.data)
                file.write(json.dump(self.data, file, indent=4))
        except TypeError:
            pass

    def get_json(self) -> dict:
        """_summary_
            guilds JSON 파일을 불러와서 return함
        return Dict
        """
        with open(os.path.join(f"{__location__}\\json\\guilds.json"),'r',encoding='utf-8') as file:
            print("저장됨")
            return json.load(file)
            
    def check_guild(self, guild_id: str):
        """_summary_
            만약 해당 str(guild.id)가 self.data에 없다면 추가함.
        Args:
            guild_id (str, 필수): 해당 guild의 id
        """
        if guild_id not in self.data:
            self.data[guild_id] = {
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

        embed=discord.Embed(title=f"경고 한도를 {warn_number}로 저장했느니라", description="경고 한도 초과시 관리자가 즉시 조치를 취할 수 있도록 하는 기능이니라", color=0xb0a7d3)
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
        self.check_user(str(interaction.guild.id), str(user.id), str(user.name))
        self.data[str(interaction.guild.id)]["warned"][str(user.id)]["warning"] += 1

        embed=discord.Embed(title=f"{user.name} (이)에게 경고 1회를 부여 하였느니라", description=f"사유: {reason}", color=0xb0a7d3)
        embed.set_author(name="냥이", icon_url="https://i.imgur.com/ORq6ORB.jpg")

        await interaction.response.send_message(embed=embed)

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
    
