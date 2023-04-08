import os, json
import discord
from discord import app_commands, ui
from discord.ext import commands, tasks
from discord.ui import Button, Select, View

developer_msg = """
개발자(씹덕셋)
> 팀 온가람[오곡밥튀김#3074, 모건#4653, 영후#6983]
"""

helpers_msg = """
베타 테스터
> ㅇㅎㅅ#8507, 백운하#3499, 치이오라버니#4954, yor42#0420,
> 범아#0488, 연하#5992, 은빛고양이#0660, 지홍#7895

Special Thanks to
> Jamess000#2945
"""

msg = """
            ⚆ `/삭제 <메시지 개수>`
            > 메시지를 삭제합니다
            ⚆ `/챗방 <이름> <주제> <NSFW["TRUE"/"FALSE"]>`
            > 채팅방을 생성합니다
            ⚆ `/통화방 <이름> <최대 유저 수[0일시 제한 없음]>`
            > 통화방을 생성합니다
            ⚆ `/초대`
            > 봇 초대 링크를 생성합니다
            ⚆ `/환영끄기`
            > 명령어를 사용한 채팅방의 일반 채널로 설정합니다
            ⚆ `/환영켜기`
            > 명령어를 사용한 채팅방을 환영 채널로 설정합니다
            ⚆ `/도움말`
            > 도움말 리스트를 표시합니다
            ⚆ `/서버`
            > 나와 아해들 다스코드 서버 초대 링크
            +
            ⚆ `/경고확인 <유저#0000>`
            > 선택한 유저의 경고 스택을 차감합니다
            ⚆ `/경고경감 <유저#0000>`
            > 선택한 유저의 경고 스택을 차감합니다
            ⚆ `/경고목록`
            > 경고를 받은 유저 목록을 불러옵니다
            ⚆ `/경고한도 <최대경고수>`
            > 경고 스택 최대 한도를 설정합니다
            ⚆ `/강퇴 <유저#0000>`
            > 선택한 유저를 강퇴합니다
            ⚆ `/차단 <유저#0000>`
            > 선택한 유저를 차단합니다
            ⚆ `/차단해제 <유저#0000>`
            > 선택한 유저의 차단을 해제합니다
            ⚆ `/사면 <유저#0000>`
            > 선택한 유저의 타임아웃을 해제합니다
            ⚆ `/타임아웃 <유저#0000> <시간>`
            > 선택한 유저를 타임아웃합니다
            +
            ⚆ `/선물[캐릭터와 관련있는 아이템 선물 시 30% 추가 경험치 지급]`
            > 선물 지급을 위한 창을 불러옵니다
            ⚆ `/출석`
            > 출석체크합니다
            ⚆ `/정보`
            > 유저의 스테이터스를 표시합니다
            ⚆ `/인벤토리`
            > 유저의 인벤토리를 표시합니다
            ⚆ `/지갑`
            > 유저의 잔고를 표시합니다
            ⚆ `/생일 <월> <일>`
            > 생일 날짜를 저장합니다 (변경 불가능)
            ⚆ `/생일캐릭터`
            > 생일을 축하해줄 캐릭터를 변경합니다
            +
            ⚆ `/가위바위보 <베팅금액>`
            > 페이와 가위바위보를 합니다
            ⚆ `/블랙잭 <베팅금액>`
            > 페이와 블랙잭을 합니다
            ⚆ `/슬롯머신 <베팅금액>`
            > 페이의 슬롯머신을 돌립니다
            ⚆ `/추첨 <추첨 인원> <이름들[','로 구분]>`
            > 이름들 중에서 추첨 인원 수만큼 사람을 뽑습니다
            ⚆ `/가챠[1회 30000원]`
            > 가챠를 돌려 선물용 아이템을 뽑습니다
            ⚆ `/게임정보`
            > 게임 정보 제공 창을 불러옵니다
            +
            ⚆ `/입장`or`/j`
            > 음악봇을 현재 통화방에 입장시킵니다
            ⚆ `/퇴장`or`/q`
            > 음악봇을 현재 통화방에서 퇴장시킵니다
            ⚆ `/재생 <검색어/링크>`or`/p <검색어/링크>`
            > 선택한 음악을 재생목록에 추가합니다
            ⚆ `/재생목록`or`/pl`
            > 재생목록을 불러옵니다
            ⚆ `/일시정지`or`/pp`
            > 현재 재생중인 음악을 일시정지합니다
            ⚆ `/재개`or`/r`
            > 현재 일시정지된 음악을 재개합니다
            ⚆ `/루프`or`/l`
            > 현재 재생중인 음악을 반복/반복해제 합니다
            ⚆ `/스킵`or`/s`
            > 현재 재생중인 음악을 스킵합니다
            +
            ⚆ `인사`
            > ex) 랑이야 좋은 아침!
            ⚆ `뭐해`
            > ex) 랑이야 뭐하고 있어?
            ⚆ `진명`
            > (범이, 연리, 강세희)
            ⚆ '이름 부르기'
            > (랑이야, 치이야, 세희야)
            """
msg = msg.split("+")

class ComButton(discord.ui.Button):
    def __init__(self, button_style, label, custom_id) -> None:

        super().__init__(
            style=button_style, label=label, custom_id=custom_id
        )

    async def callback(self, interaction: discord.Interaction):
        view = helpview()
        if self.custom_id == "sys":
            embed = discord.Embed(
                title="🚩 관리 (관리자 전용)",
                description="",
                colour=discord.Colour.from_rgb(241, 196, 15),
            )
            embed.add_field(name="", value=msg[0], inline=True)

        elif self.custom_id == "warn":
            embed = discord.Embed(
                title="⚠️ 처벌 (관리자 전용)",
                description="",
                colour=discord.Colour.from_rgb(241, 196, 15),
            )
            embed.add_field(name="", value=msg[1], inline=True)

        elif self.custom_id == "interact":
            embed = discord.Embed(
                title="💌 상호작용",
                description="",
                colour=discord.Colour.from_rgb(241, 196, 15),
            )
            embed.add_field(name="", value=msg[2], inline=True)

        elif self.custom_id == "game":
            embed = discord.Embed(
                title="🎲 게임",
                description="",
                colour=discord.Colour.from_rgb(241, 196, 15),
            )
            embed.add_field(name="", value=msg[3], inline=True)

        elif self.custom_id == "music":
            embed = discord.Embed(
                title="🎹 음악",
                description="",
                colour=discord.Colour.from_rgb(241, 196, 15),
            )
            embed.add_field(name="", value=msg[4], inline=True)

        elif self.custom_id == "talk":
            embed = discord.Embed(
                title="👋 대화",
                description="",
                colour=discord.Colour.from_rgb(241, 196, 15),
            )
            embed.add_field(name="", value=msg[5], inline=True)
        

        button1 = ComButton(discord.ButtonStyle.grey, "🚩관리🚩", "sys")
        button2 = ComButton(discord.ButtonStyle.grey, "⚠️처벌⚠️", "warn")
        button3 = ComButton(discord.ButtonStyle.grey, "💌상호작용💌", "interact")
        button4 = ComButton(discord.ButtonStyle.grey, "🎲게임🎲", "game")
        button5 = ComButton(discord.ButtonStyle.grey, "🎹음악🎹", "music")
        button6 = ComButton(discord.ButtonStyle.grey, "👋대화👋", "talk")

        view.add_item(button1)
        view.add_item(button2)
        view.add_item(button3)
        view.add_item(button4)
        view.add_item(button5)
        view.add_item(button6)

        await interaction.response.edit_message(view=view, embed=embed)


####################################################################################################################################
class InfoSelect(Select):
    def __init__(self):

        options = [
            discord.SelectOption(
                label="나아봇", description="나아봇 소개", emoji="😊", value=11 #스마일 이미지 랑이 커스텀 이미지로 변경 예정(가능하면)
            ),
            discord.SelectOption(
                label="명령어", description="명령어 조회", emoji="📔", value=22
            ),
            discord.SelectOption(
                label="개발자 정보", description="개발자 정보", emoji="📇", value=33
            ),
            discord.SelectOption(
                label="도움을 주신 분들", description="도움을 준 사람들", emoji="❤️", value=44
            ),
        ]
        super().__init__(
            placeholder="Choose an option", options=options, min_values=1, max_values=1
        )

    ####################################################################################################################################
    async def callback(self, interaction: discord.Interaction):

        view = helpview()
        if self.values[0] == "11":
            embed = discord.Embed(
                title="나아봇 소개",
                description="",
                colour=discord.Colour.from_rgb(241, 196, 15),
            )
        elif self.values[0] == "22":
            embed = discord.Embed(
                title="명령어",
                description="원하시는 명령어 범주를 선택하십시오",
                colour=discord.Colour.from_rgb(241, 196, 15),
            )
            
            button1 = ComButton(discord.ButtonStyle.grey, "🚩관리🚩", "sys")
            button2 = ComButton(discord.ButtonStyle.grey, "⚠️처벌⚠️", "warn")
            button3 = ComButton(discord.ButtonStyle.grey, "💌상호작용💌", "interact")
            button4 = ComButton(discord.ButtonStyle.grey, "🎲게임🎲", "game")
            button5 = ComButton(discord.ButtonStyle.grey, "🎹음악🎹", "music")
            button6 = ComButton(discord.ButtonStyle.grey, "👋대화👋", "talk")

            view.add_item(button1)
            view.add_item(button2)
            view.add_item(button3)
            view.add_item(button4)
            view.add_item(button5)
            view.add_item(button6)

        elif self.values[0] == "33":
            embed = discord.Embed(
                title="개발자",
                description="",
                colour=discord.Colour.from_rgb(241, 196, 15),
            )
            embed.add_field(name="", value=developer_msg, inline=False)

        elif self.values[0] == "44":
            embed = discord.Embed(
                title="도움을 주신 분들",
                description="",
                colour=discord.Colour.from_rgb(241, 196, 15),
            )
            embed.add_field(name="", value=helpers_msg, inline=False)

        await interaction.response.edit_message(view=view, embed=embed)


####################################################################################################################################
class GInfoSelect(Select):
    def __init__(self):

        options = [
            discord.SelectOption(
                label="가위바위보", description="폐이와의 가위바위보", emoji="✌️", value=1
            ),
            discord.SelectOption(
                label="블랙잭", description="폐이와의 블랙잭", emoji="🃏", value=2
            ),
            discord.SelectOption(
                label="슬롯머신", description="폐이의 슬롯머신", emoji="🎰", value=3
            ),
        ]
        super().__init__(
            placeholder="Choose an option", options=options, min_values=1, max_values=1
        )

    ####################################################################################################################################
    async def callback(self, interaction: discord.Interaction):

        if self.values[0] == "1":
            embed = discord.Embed(
                title="✌️ 가위바위보",
                description="",
                colour=discord.Colour.from_rgb(241, 196, 15),
            )
            embed.add_field(name="명령어", value="`/가위바위보 <베팅금액>`", inline=False)
            embed.add_field(name="\📖 플레이 방법", value="> -가위, 바위, 보 중 하나에 해당하는 버튼을 누릅니다", inline=True)
            embed.add_field(name="\💰 상품", value="> 승리: 걸었던 돈의 두배를 받습니다\n> 패배: 걸었던 돈을 잃습니다\n> 비김: 걸었던 돈의 절반을 잃습니다", inline=True)

        elif self.values[0] == "2":
            embed = discord.Embed(
                title="🃏 블랙잭",
                description="",
                colour=discord.Colour.from_rgb(241, 196, 15),
            )
            embed.add_field(name="명령어", value="`/블랙잭 <베팅금액>`", inline=False)
            embed.add_field(name="\📖 플레이 방법", value="> -시작할 때 카드 두 장을 받습니다\n> -자신이 가진 카드값의 합이 22보다 작고 21에 가까우면 승리합니다\n> -카드값의 합이 21을 초과 시 바로 패배합니다\n> -처음 두 장의 카드의 합이 21일 경우 블랙잭으로 승리합니다\n> -'히트'시 새 카드를 한장 받습니다\n> -'스탠드'시 현재 가드 조합으로 결과를 받습니다", inline=True)
            embed.add_field(name="\💰 상품", value="> 블랙잭: 걸었던 금액의 1.5배만큼을 받습니다\n> 승리: 걸었던 금액만큼을 받습니다\n> 패배: 걸었던 돈을 잃습니다\n> 비김: 걸었던 돈을 잃습니다", inline=True)

        elif self.values[0] == "3":
            embed = discord.Embed(
                title="🎰 슬롯머신",
                description="",
                colour=discord.Colour.from_rgb(241, 196, 15),
            )
            embed.add_field(name="명령어", value="`/슬롯머신 <베팅금액>`", inline=False)
            embed.add_field(name="\📖 플레이 방법", value="> -돈을 걸고 슬롯머신을 돌립니다(명령어를 사용)\n> 잭팟: 3개의 종 그림\n> 트리플: 3개의 같은 그림\n> 페어: 2개의 같은 그림\n> 꽝: 0개의 같은 그림", inline=True)
            embed.add_field(name="\💰 상품", value="> 잭팟: 걸었던 금액의 100배의 돈을 받습니다\n> 트리플: 걸었던 금액의 5배의 돈을 받습니다\n> 페어: 걸었던 금액의 1.5배의 돈을 받습니다\n> 꽝: 걸었던 돈을 잃습니다", inline=True)

        view = infoview()
        await interaction.response.edit_message(view=view, embed=embed)

# ⚆ `/가위바위보 <베팅금액>` 1.5 5 100
# > 페이와 가위바위보를 합니다
# ⚆ `/블랙잭 <베팅금액>`
# > 페이와 블랙잭을 합니다
# ⚆ `/슬롯머신 <베팅금액>`
# > 페이의 슬롯머신을 돌립니다

####################################################################################################################################
class infoview(View):
    """
    _summary_
        클래스 안으로 값 받아옴
    Args:
        self (obj, 필수): 오브젝트
        user (discord.Member, 필수): 디코 유저
    """

    def __init__(self) -> None:
        super().__init__()
        self.add_item(GInfoSelect())


####################################################################################################################################
class helpview(discord.ui.View):
    def __init__(self) -> None:
        super().__init__()
        self.add_item(InfoSelect())

####################################################################################################################################


class Explain(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("준비됨")

    @app_commands.command(name="게임정보", description="게임정보")
    async def GameInfo(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="게임정보",
            description="정보를 얻고 싶은 게임을 선택해 주십시오",
            colour=discord.Colour.from_rgb(241, 196, 15),
        )
        await interaction.response.send_message(embed=embed, view=infoview())

    @app_commands.command(name="도움말", description="도움말")
    async def Help(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="도움말",
            description="도움을 원하시는 범주를 선택해 주십시오",
            colour=discord.Colour.from_rgb(241, 196, 15),
        )
        await interaction.response.send_message(embed=embed, view=helpview())


async def setup(bot):
    await bot.add_cog(Explain(bot))