import os,re,json
import discord
from discord import app_commands,ui
from discord.ext import commands, tasks
from datetime import datetime, timedelta
from discord.ui import Button, Select, View
from cogs.mod import Moderator
list_dev_id = ["339767912841871360", "474389454262370314", "393932860597338123", "185181025104560128"]
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


class WarnSelect(Select):
    """_summary_
        Select UI 사용
        밴, 타임아웃, 킥 선택 할수 있고 선택에 따라서
        설명용 더미 버튼과 킥,밴, 타임아웃을 할 수 있는 버튼 생성
    """
    def __init__(self, user: discord.Member):
        """
            _summary_
                클래스 안으로 값 받아옴
        Args:
            self (obj, 필수): 오브젝트
            user (discord.Member, 필수): 디코 유저
        """
        self.user = user
        options = [
            discord.SelectOption(label="밴", description="경고 한도를 넘은 유저를 밴 합니다", emoji="🚫", value=1),
            discord.SelectOption(label="타임아웃", description="경고 한도를 넘은 유저를 타임아웃 시킵니다", emoji="🕰️", value=2),
            discord.SelectOption(label="킥", description="경고 한도를 넘은 유저를 킥 합니다", emoji="❗", value=3)
        ]
        super().__init__(placeholder='Choose an option', options=options, min_values=1, max_values=1)

    async def callback(self, interaction: discord.Interaction):
        """
        만약 WarnSelect가 Select가 되었다면 그에 따른 버튼을 만든 뒤
        Warnview에서 Select view를 불러오고 거기에 더미 버튼인 버튼과 버튼1을
        Select에 따라 add하고 message의 view를 edit함

        :param interaction:
        :return:
        """
        view = Warnview(self.user)
        if self.values[0] == '1':
            button = WarnButton(discord.ButtonStyle.grey, "현재 선택된 처분: 밴 ", 'dummy', True, self.user)
            button1 = WarnButton(discord.ButtonStyle.green, "확인", '밴', False, self.user)

        elif self.values[0] == '2':
            button = WarnButton(discord.ButtonStyle.grey, "현재 선택된 처분: 타임아웃 ", 'dummy', True, self.user)
            button1 = WarnButton(discord.ButtonStyle.green, "확인", '타임아웃', False, self.user)

        elif self.values[0] == '3':
            button = WarnButton(discord.ButtonStyle.grey, "현재 선택된 처분: 킥 ", 'dummy', True, self.user)
            button1 = WarnButton(discord.ButtonStyle.green, "확인",'킥', False, self.user)

        view.add_item(button)
        view.add_item(button1)
        await interaction.response.edit_message(view=view)

class WarnModal(ui.Modal,title="타임아웃"):
    """_summary_
            Modal UI 사용
            타임아웃에 form을 생성
            이떄 sumbit되는 값은 5~12글자 이여야 하고
            submit 된 값은 time에 저장
            유저에게 (일,시,분)형식으로 적으라고 알려줌
        """
    def __init__(self, user:discord.Member):
        """
            _summary_
                    클래스 안으로 값 받아옴
            Args:
                self (obj, 필수): 오브젝트
                user (discord.Member, 필수): 디코 유저
     """
        super().__init__()
        self.user = user
    time = ui.TextInput(label="타임아웃할 시간을 적어주세요", style=discord.TextStyle.short, placeholder="(일,시,분)형식으로 적어 주세요",required=True,max_length=12,min_length=5)
   
    async def on_submit(self,interaction:discord.Interaction):
        """
        만약 submit이 되었다면 일단 (일,시,분)형식인지 확인하고
        만약 맞다면 day,hour,min으로 나누고 이 값이 int값이 면서 날이 20일 안넘어가지는지 확인
        그후 mod.py에 있는 timeout과 똑같이 작동
        :param interaction:
        :return:
        """
        Time_check=str(self.time)
        if re.match(r'^\d+,\d+,\d+$', Time_check):
            day, hour, min = map(int, Time_check.split(","))
            if isinstance(day, int) and isinstance(hour, int) and isinstance(min, int) and day<=20:
                now = datetime.now().astimezone()
                till = now + timedelta(minutes=min, hours=hour, days=day)
                bantime = timedelta(minutes=min, hours=hour, days=day)
            else:
                return
        else:
            return
        reason="경고 한도 초과"
        embedChannel = discord.Embed(
            title=f"{self.user.name}이 {bantime.days}일 {bantime.seconds // 60 // 60}시간 {(bantime.seconds // 60) % 60}분 {bantime.seconds % 60}초 동안 타임아웃 처리되었습니다",
            description=f"사유: {reason}", color=0xb0a7d3)
        embedChannel.set_author(name="관리자 세희", icon_url="https://i.imgur.com/7a4oeOi.jpg")
        embedUser = discord.Embed(
            title=f"{interaction.guild.name}에서 {bantime.days}일 {bantime.seconds // 60 // 60}시간 {(bantime.seconds // 60) % 60}분 {bantime.seconds % 60}초 동안 타임아웃 처리되었습니다",
            description=f"사유: {reason}", color=0xb0a7d3)
        embedUser.set_author(name="관리자 세희", icon_url="https://i.imgur.com/7a4oeOi.jpg")

        await self.user.send(embed=embedUser)
        await interaction.response.send_message(embed=embedChannel)
        await self.user.timeout(till, reason=reason)

class WarnButton(discord.ui.Button):
    """
    _summary_
            Button UI 사용
            버튼 생성 눌러지는 버튼에 따라서 밴, 타임아웃, 킥 중 하나를 실행
            다만 타임아웃 같은 경우엔 WarnModal로 넘어가서 타임아웃 실행
            그후 타임아웃이 아닌 버튼이라면  self.custom_id를 사용해서 유저 처분을 서버및 유저에게 알림
    """
    def __init__(self, button_style, label, custom_id, able, user) -> None:
        """
            _summary_
            클래스 안으로 값 받아옴
                Args:
                    self (obj, 필수): 오브젝트
                    button_style (style, 필수): 버튼 색상 지정
                    label (str, 필수): 버튼이 보여줄 글
                    custom_id (str, 필수): 버튼 고유 id
                    able(bool,필수): 버튼 활성화 유무
                    user (discord.Member, 필수): 디코 유저
        """
        super().__init__(style=button_style, label=label, custom_id=custom_id, disabled=able)
        self.user = user

    async def callback(self, interaction: discord.Interaction):
        """
        버튼 생성 눌러지는 버튼에 따라서 밴, 타임아웃, 킥 중 하나를 실행
        다만 타임아웃 같은 경우엔 WarnModal로 넘어가서 타임아웃 실행
        그후 타임아웃이 아닌 버튼이라면  self.custom_id를 사용해서 유저 처분을 서버및 유저에게 알림
        :param interaction:
        :return:
        """
        a=0
        if self.custom_id == '밴':
            await self.user.ban(reason="")
        elif self.custom_id == '타임아웃':
            a=1
            await interaction.response.send_modal(WarnModal(self.user))
        elif self.custom_id == '킥':
            await self.user.kick(reason="")
        if a==1:
            return
        embedChannel = discord.Embed(
            title=f"{self.user.name}이 {self.custom_id} 처리되었습니다",
            description=f"사유: 경고한도 초과", color=0xb0a7d3)
        embedChannel.set_author(name="관리자 세희", icon_url="https://i.imgur.com/7a4oeOi.jpg")
        embedUser = discord.Embed(title=f"{interaction.guild.name}에서 {self.custom_id} 처리되었습니다",description=f"사유: 경고한도 초과", color=0xb0a7d3)
        embedUser.set_author(name="관리자 세희", icon_url="https://i.imgur.com/7a4oeOi.jpg")
        await interaction.channel.send(embed=embedChannel)
        await self.user.send(embed=embedUser)

class Warnview(discord.ui.View):
    """
    _summary_
        클래스 안으로 값 받아옴
    Args:
        self (obj, 필수): 오브젝트
        user (discord.Member, 필수): 디코 유저
    """
    def __init__(self, user: discord.Member) -> None:
        super().__init__()
        self.add_item(WarnSelect(user))

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
            만약 경고가 경고 한도를 넘어가면 WarnSelect를 view를 통해 생성함으로서 천분 결정
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

        if self.data[str(interaction.guild.id)]["warnLimit"] <= \
                self.data[str(interaction.guild.id)]["warned"][str(user.id)]["warning"]:
            embed = discord.Embed(title=f"{user.name}의 처분 선택", description=f"사유: 경고 초과", color=0xb0a7d3)
            embed.set_author(name="냥이", icon_url="https://i.imgur.com/ORq6ORB.jpg")
            await interaction.followup.send(embed=embed, view=Warnview(user), ephemeral=True)


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
        self.check_guild(str(interaction.guild.id))
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
    
