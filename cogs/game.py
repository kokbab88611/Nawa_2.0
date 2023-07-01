import discord,random,string,array,time
import asyncio
from discord import app_commands,Interaction,Reaction,InteractionResponse
from discord.ui import Button, View
from discord.ext import commands, tasks
import random
import os
import PIL
from PIL import Image, ImageFont, ImageDraw
import datetime
from datetime import timezone
from time import gmtime, strftime
import csv

utc = datetime.timezone.utc
rest_time = datetime.time(hour=15, minute=00, tzinfo=utc)
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

DailyLuckMsg = [
        "오늘은 새로운 기회가 찾아올 것입니다.",
        "어려운 일이 있더라도 포기하지 마세요. 그것이 성공으로 가는 길입니다.",
        "긍정적인 에너지를 유지하세요. 주변 사람들에게 영감을 줄 수 있습니다.",
        "과거의 실수를 후회하지 마세요. 그것들은 성장의 기회였습니다.",
        "오늘은 집중력이 높아지는 날입니다. 목표에 집중하세요.",
        "자신에게 자신감을 가지세요. 자신의 능력을 믿어야 성공할 수 있습니다.",
        "예상치 못한 기쁨이 찾아올 것입니다. 기대해도 좋습니다.",
        "주변 사람들과의 소통을 중요시하세요. 협력은 큰 성과를 가져올 수 있습니다.",
        "주어진 일에 최선을 다하세요. 노력은 결실을 맺을 것입니다.",
        "오늘은 명상이나 여가 시간을 갖는 것이 좋습니다. 내면의 평화를 찾을 수 있습니다.",
        "어려움을 만나더라도 꿋꿋하게 나아가세요. 어려움은 단지 시험일 뿐입니다.",
        "긍정적인 사고를 유지하세요. 그것이 문제 해결의 열쇠입니다.",
        "도전에 맞서기를 두려워하지 마세요. 성장과 배움의 기회가 될 수 있습니다.",
        "오늘은 새로운 인연이 생길 수 있는 날입니다. 주변을 주의깊게 봐주세요.",
        "당신의 노력이 인정받을 것입니다. 주변 사람들의 찬사에 귀 기울이세요.",
        "자신의 장점을 활용하세요. 그것이 성공으로 가는 열쇠입니다.",
        "무엇이든 해낼 수 있습니다. 자신에게 자신감을 가지세요.",
        "주변 사람들에게 도움을 구하세요. 협력은 상호 유익한 결과를 가져올 수 있습니다.",
        "오늘은 긍정적인 변화가 있을 것입니다. 기대해도 좋습니다.",
        "새로운 아이디어가 떠오를 것입니다. 창의적인 생각에 주목하세요.",
        "오늘은 안정적인 에너지가 느껴질 것입니다. 안심하고 나아가세요.",
        "어려운 상황에서도 포기하지 마세요. 어려움을 극복할 수 있습니다.",
        "자신에게 도전을 주세요. 능력의 한계를 넘어설 수 있습니다.",
        "오늘은 긍정적인 변화가 찾아올 것입니다. 기회를 잡으세요.",
        "주변 사람들과의 원활한 소통이 중요합니다. 소통은 관계를 개선시킬 수 있습니다.",
        "새로운 기회를 놓치지 마세요. 그것이 성공으로 이끌 수 있습니다.",
        "오늘은 자신의 감정에 귀 기울이는 것이 좋습니다. 내면의 평화를 찾을 수 있습니다.",
        "과거의 실수에 집착하지 마세요. 과거는 이미 지나갔습니다.",
        "오늘은 자신의 장점을 믿어보세요. 그것이 성공으로 가는 길입니다.",
        "어려운 일을 맡기 전에 충분히 준비하세요. 준비는 성공의 핵심입니다.",
        "오늘은 독창적인 아이디어가 떠오를 수 있는 날입니다. 창의력을 발휘해 보세요.",
        "자신을 사랑하고 돌봐주세요. 자기 존중감이 성공으로 이끌어 줄 것입니다.",
        "주변 사람들의 조언에 귀를 기울이세요. 그들의 지혜는 가치가 있을 수 있습니다.",
        "오늘은 운이 좋은 날입니다. 기대를 가져도 좋습니다.",
        "목표를 분명하게 설정하세요. 목표가 뚜렷할수록 성공에 가까워집니다.",
        "자신의 역량을 믿으세요. 그것이 성공을 이끄는 열쇠입니다.",
        "어려움에 직면하더라도 겁내지 마세요. 어려움은 성장을 위한 시험입니다.",
        "오늘은 새로운 도전에 임하는 것이 좋습니다. 성장의 기회가 될 수 있습니다.",
        "긍정적인 마인드셋으로 일하세요. 그것이 성공에 가는 길입니다.",
        "주변 사람들에게 관심을 가져주세요. 그들의 지지는 큰 힘이 될 수 있습니다.",
        "오늘은 예상치 못한 성과를 얻을 수 있는 날입니다. 놀라운 결과를 기대해보세요.",
        "노력에 대한 보상이 찾아올 것입니다. 꾸준한 노력은 결실을 맺을 것입니다.",
        "자신에게 도전하고 성장하세요. 한계를 넘어설 수 있습니다.",
        "오늘은 안정적인 에너지가 넘칠 것입니다. 이에 기대하세요.",
        "어려움을 마주했을 때는 자신을 격려해주세요. 어려움은 단지 장애물일 뿐입니다.",
        "긍정적인 사고방식으로 일하세요. 그것이 문제 해결을 돕습니다.",
        "도전에 맞서기를 두려워하지 마세요. 그것이 성장과 발전의 길입니다.",
        "오늘은 새로운 인연이 찾아올 수 있는 날입니다. 주변 사람들과의 만남을 소중히 여기세요.",
        "당신의 노력과 열정은 인정받을 것입니다. 주변 사람들의 칭찬을 받아들이세요.",
        "자신의 장점을 잘 활용하세요. 그것이 성공을 이끄는 열쇠입니다.",
        "어떤 일이든 해낼 수 있습니다. 자신에게 자신감을 가지세요.",
        "주변 사람들과의 협력을 이끌어내세요. 함께하는 힘은 큰 성과를 이끌어낼 수 있습니다.",
        "오늘은 변화가 있을 수 있는 날입니다. 긍정적으로 변화에 대응하세요.",
        "새로운 아이디어에 주목하세요. 그것이 미래를 열어갈 수 있습니다.",
        "오늘은 안정적인 에너지를 느낄 수 있는 날입니다. 이를 활용하세요.",
        "어려움을 마주했을 때 포기하지 마세요. 어려움은 성공을 위한 시험일 뿐입니다.",
        "자신의 능력을 믿어보세요. 그것이 성공으로 이끌어 줄 것입니다.",
        "오늘은 주변 사람들과의 원활한 소통이 중요합니다. 소통은 관계를 향상시킬 수 있습니다.",
        "새로운 기회를 놓치지 마세요. 그것이 성공으로 이끌 수 있습니다.",
        "오늘은 내면의 평화를 찾을 수 있는 좋은 날입니다. 조용한 시간을 가져보세요.",
        "과거의 실수에 집착하지 마세요. 과거는 이미 지나갔습니다.",
        "오늘은 자신의 장점을 활용해보세요. 그것이 성공을 향한 길입니다.",
        "어려운 일을 맡기 전 충분한 준비를 해야합니다. 준비는 성공의 핵심입니다.",
        "오늘은 창의적인 아이디어가 떠오를 수 있는 날입니다. 창조력을 발휘해보세요.",
        "자신을 사랑하고 돌봐주세요. 자기 존중감이 성공을 이끌어줄 것입니다.",
        "주변 사람들의 조언에 귀를 기울여보세요. 그들의 지혜는 귀중할 수 있습니다.",
        "오늘은 운이 좋은 날입니다. 기대를 가져도 좋습니다.",
        "목표를 명확히 설정하세요. 목표가 뚜렷할수록 성공에 가까워집니다.",
        "자신의 역량을 믿어보세요. 그것이 성공을 이끄는 열쇠입니다.",
        "어려운 상황에 직면해도 두려워하지 마세요. 어려움은 성장을 위한 기회입니다.",
        "오늘은 새로운 도전에 집중해보세요. 성장의 기회가 될 수 있습니다.",
        "긍정적인 사고방식으로 일하세요. 그것이 문제 해결을 돕습니다.",
        "주변 사람들에게 관심을 가져주세요. 그들의 지지는 큰 힘이 될 수 있습니다.",
        "오늘은 예상치 못한 결과를 얻을 수 있는 날입니다. 놀라운 결과를 기대해보세요.",
        "노력한 만큼 보상이 올 것입니다. 꾸준한 노력은 성공으로 이끌어줄 것입니다.",
        "자신에게 도전하고 성장하세요. 한계를 넘어설 수 있습니다.",
        "오늘은 안정감을 느낄 수 있는 날입니다. 이를 활용해보세요.",
        "어려운 상황에서도 포기하지 마세요. 어려움을 극복할 수 있습니다.",
        "자신의 역량을 믿고 나아가세요. 그것이 성공으로 이끄는 열쇠입니다.",
        "오늘은 기대 이상의 결과가 있을 수 있는 날입니다. 긍정적으로 대해보세요.",
        "주변 사람들과의 원활한 소통이 중요합니다. 소통은 관계를 향상시킬 수 있습니다.",
        "새로운 기회를 놓치지 마세요. 그것이 성공으로 이끌 수 있습니다.",
        "오늘은 내면의 평화를 찾을 수 있는 좋은 날입니다. 조용한 시간을 갖추세요.",
        "과거의 실수에 집착하지 마세요. 과거는 이미 지나간 일입니다.",
        "오늘은 자신의 장점을 발휘해보세요. 그것이 성공을 향한 길입니다.",
        "어떤 일이든 해낼 수 있습니다. 자신을 믿어보세요.",
        "주변 사람들과의 협력을 이끌어내세요. 함께 하는 힘은 큰 성과를 이끌어낼 수 있습니다.",
        "오늘은 변화가 있는 날입니다. 긍정적으로 변화에 대응해보세요.",
        "새로운 아이디어에 주목하세요. 그것이 미래를 열어갈 수 있습니다.",
        "오늘은 안정된 에너지를 느낄 수 있는 날입니다. 이를 활용해보세요.",
        "어려움을 마주했을 때 포기하지 않고 극복해보세요. 어려움은 성공을 위한 시험입니다.",
        "자신의 능력을 믿어보세요. 그것이 성공을 이끌어줄 것입니다.",
        "오늘은 주변 사람들과의 원활한 소통이 중요합니다. 상호 작용을 통해 관계를 향상시킬 수 있습니다.",
        "새로운 기회를 놓치지 말고 잡으세요. 그것이 성공으로 이끌 수 있습니다.",
        "오늘은 내면의 평화를 찾을 수 있는 좋은 날입니다. 조용한 시간을 가져보세요.",
        "과거의 실수에 집착하지 않아도 괜찮습니다. 과거는 이미 지나간 일입니다.",
        "오늘은 자신의 장점을 잘 활용해보세요. 그것이 성공을 향한 열쇠입니다.",
        "어려운 상황에 직면했을 때도 포기하지 마세요. 어려움은 성장을 위한 시험입니다.",
        "오늘은 새로운 도전을 맞이하기에 좋은 날입니다. 성장과 발전의 기회가 될 수 있습니다.",
        "긍정적인 사고를 유지하세요. 그것이 성공으로 이끄는 길입니다.",
        "자신의 목표를 분명하게 설정하세요. 명확한 목표는 성공을 향한 길목을 제시해줍니다.",
        "오늘은 도전에 집중해보세요. 도전은 성장과 발전의 기회를 가져다줍니다.",
        "자신의 역량과 잠재력을 믿어보세요. 당신은 놀라운 일을 이룰 수 있습니다.",
        "오늘은 새로운 아이디어가 떠오를 수 있는 날입니다. 창의력을 발휘해 보세요.",
        "주변 사람들과의 협력을 강조해보세요. 함께하는 힘은 큰 성과를 이룰 수 있습니다.",
        "오늘은 변화에 개방적인 태도를 갖추어보세요. 변화는 새로운 가능성을 열어줄 수 있습니다.",
        "자신의 감정에 귀를 기울여보세요. 내면의 조화를 찾을 수 있습니다.",
        "과거의 실수에 집착하지 마세요. 그 대신에 현재에 집중해보세요.",
        "자신의 장점과 재능을 자랑스럽게 생각해보세요. 그것들이 당신의 독특한 매력입니다.",
        "오늘은 자신을 사랑하고 돌보는 시간을 가져보세요. 자기 자신을 소중히 여기는 것이 중요합니다.",
        "주변 사람들의 조언을 듣고 배우려 노력해보세요. 그들은 당신에게 새로운 시각을 제공할 수 있습니다.",
        "오늘은 행운이 함께할 수 있는 날입니다. 긍정적인 기대를 가져보세요.",
        "목표를 명확하게 설정하고 그에 맞춰 행동하세요. 목표는 당신을 성공으로 이끌어줄 것입니다.",
        "자신의 역량과 잠재력을 믿어보세요. 당신은 놀라운 성과를 이룰 수 있습니다.",
        "오늘은 주변 사람들과의 소통에 더욱 신경을 써야 합니다. 소통은 관계를 향상시킬 수 있습니다.",
        "새로운 기회를 놓치지 말고 잡으세요. 그것이 당신의 성공으로 이끌어갈 수 있습니다.",
        "오늘은 내면의 평화와 조화를 찾을 수 있는 좋은 날입니다. 조용한 시간을 갖추세요.",
        "과거의 실수에 과도하게 집착하지 말고, 그 대신에 배움과 성장에 집중하세요.",
        "오늘은 자신의 장점을 최대한으로 활용해보세요. 그것이 성공으로 이끄는 열쇠입니다.",
        "어려운 상황에 직면해도 극복할 수 있습니다. 자신에게 믿음을 가져보세요.",
        "자신의 능력을 자세히 알아보세요. 그것이 성공을 이끄는 중요한 요소입니다.",
        "오늘은 주변 사람들과의 원활한 협력이 필요합니다. 함께 하는 것이 큰 성과를 이룰 수 있습니다.",
        "새로운 시도에 열린 마음을 가져보세요. 그것이 당신에게 더 나은 결과를 가져다줄 수 있습니다.",
        "자신의 창조적인 아이디어를 발휘해보세요. 놀라운 발견을 할 수 있습니다.",
        "오늘은 안정된 에너지를 느낄 수 있는 날입니다. 이를 활용해보세요.",
        "어려운 상황에 직면했을 때도 포기하지 마세요. 어려움은 성장과 배움의 기회입니다.",
        "자신의 능력과 자신감을 믿어보세요. 당신은 놀라운 일을 이룰 수 있습니다.",
        "오늘은 주변 사람들과의 원활한 소통이 중요합니다. 상호 작용을 통해 관계를 더욱 향상시킬 수 있습니다."
        ]

MemoryGameDict = {1:"<:aya:1122868308144828438>",
2:"<:baduk:1122868299663941783>",
3:"<:chie:1122868288616157214>",
4:"<:gahi:1122868284077903932>",
5:"<:nyangi:1122868279225090149>",
6:"<:rangi:1122868296832782396>",
7:"<:seongi:1122868304210558996>",
8:"<:yeorin:1122868292625895606>"}

class MemoryGameVars():
    def __init__(self):
        self.tries = 0
        self.cards = [f"{MemoryGameDict[1]}", 
        f"{MemoryGameDict[1]}", 
        f"{MemoryGameDict[2]}", 
        f"{MemoryGameDict[2]}", 
        f"{MemoryGameDict[3]}", 
        f"{MemoryGameDict[3]}", 
        f"{MemoryGameDict[4]}", 
        f"{MemoryGameDict[4]}", 
        f"{MemoryGameDict[5]}", 
        f"{MemoryGameDict[5]}", 
        f"{MemoryGameDict[6]}", 
        f"{MemoryGameDict[6]}", 
        f"{MemoryGameDict[7]}", 
        f"{MemoryGameDict[7]}", 
        f"{MemoryGameDict[8]}", 
        f"{MemoryGameDict[8]}"]
        self.cards = random.sample(self.cards, len(self.cards))
        self.cards_dis = ["⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜", "⬜"]

class MemoryGameDropDown(discord.ui.Select):
    def __init__(self, variables, command_userid):
        self.variables = variables
        self.command_userid = command_userid
        options = [
            discord.SelectOption(
                label="A1", value=0),
            discord.SelectOption(
                label="A2", value=1),
            discord.SelectOption(
                label="A3", value=2),
            discord.SelectOption(
                label="A4", value=3),
            discord.SelectOption(
                label="B1", value=4),
            discord.SelectOption(
                label="B2", value=5),
            discord.SelectOption(
                label="B3", value=6),
            discord.SelectOption(
                label="B4", value=7),
            discord.SelectOption(
                label="C1", value=8),
            discord.SelectOption(
                label="C2", value=9),
            discord.SelectOption(
                label="C3", value=10),
            discord.SelectOption(
                label="C4", value=11),
            discord.SelectOption(
                label="D1", value=12),
            discord.SelectOption(
                label="D2", value=13),
            discord.SelectOption(
                label="D3", value=14),
            discord.SelectOption(
                label="D4", value=15),
        ]

        super().__init__(placeholder="원하시는 카드를 선택하십시오", options=options, min_values=2, max_values=2)

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id == self.command_userid:
            lst = []
            for i in range(len(self.variables.cards_dis)):
                if self.variables.cards_dis[i] != "⬜":
                    if self.variables.cards_dis[i] in lst:
                        lst.remove(self.variables.cards_dis[i])
                    else:
                        lst.append(self.variables.cards_dis[i])
            for i in lst:
                self.variables.cards_dis[self.variables.cards_dis.index(i)] = "⬜"

            if self.variables.cards_dis[int(self.values[0])] == "⬜" and self.variables.cards_dis[int(self.values[1])] == "⬜":
                self.variables.tries += 1
                self.variables.cards_dis[int(self.values[0])], self.variables.cards_dis[int(self.values[1])] = self.variables.cards[int(self.values[0])], self.variables.cards[int(self.values[1])]

                if "⬜" in self.variables.cards_dis:
                    base=Game.MemoryGameGrid(self.variables.cards_dis)
                    embed = discord.Embed(
                            title="카드 짝 맞추기",
                            description=base)
                    view = MemoryGameView(self.variables, self.command_userid)
                    await interaction.response.edit_message(content="", view=view, embed=embed)
                else:
                    base = f"소요 횟수: {self.variables.tries}"
                    embed = discord.Embed(
                            title="카드 짝 맞추기",
                            description=base)
                    await interaction.response.edit_message(content="", embed=embed, view=None)
            else:
                base=Game.MemoryGameGrid(self.variables.cards_dis)
                embed = discord.Embed(
                        title="카드 짝 맞추기",
                        description=base)
                view = MemoryGameView(self.variables, self.command_userid)
                await interaction.response.edit_message(content="이미 뒤집힌 카드는 선택할 수 없습니다", view=view, embed=embed)
        else:
            await interaction.response.send_message(content="타인의 게임에 관여할 수 없습니다", ephemeral=True)

class MemoryGameView(discord.ui.View):
    def __init__(self, variables, command_userid):
        super().__init__()
        self.add_item(MemoryGameDropDown(variables, command_userid))

class Game(commands.Cog):
    channel_id:string
    def __init__(self, bot) -> None:
        self.bot = bot
        self.reset_attendence.start()

    @commands.Cog.listener()
    async def on_ready(self):
        print("준비됨")

    @app_commands.command(name="추첨", description="추첨기를 생성합니다")
    async def raname(self, interaction: discord.Interaction, people: str, join: int = 1):
        if people:
            arr = people.split(",")
            if len(arr) < join:
                await interaction.response.send_message("참가자가 충분하지 않습니다!")
                return
            arry: str = ""
            for i in range(join):
                result = random.randint(0, len(arr) - 1)
                arry += f"{i + 1}: {arr[result]}\n"
                del arr[result]

            embed = discord.Embed(title="추첨 완료", color=0xb0a7d3)
            embed.set_author(name="페이", icon_url="https://i.imgur.com/7a4oeOi.jpg")
            embed.add_field(name="당첨자", value=arry, inline=True)
            await interaction.response.send_message(embed=embed)

    def MemoryGameGrid(cards_dis):
        base= f"""⬛1️⃣2️⃣3️⃣4️⃣
        🇦{cards_dis[0]}{cards_dis[1]}{cards_dis[2]}{cards_dis[3]}
        🇧{cards_dis[4]}{cards_dis[5]}{cards_dis[6]}{cards_dis[7]}
        🇨{cards_dis[8]}{cards_dis[9]}{cards_dis[10]}{cards_dis[11]}
        🇩{cards_dis[12]}{cards_dis[13]}{cards_dis[14]}{cards_dis[15]}"""
        return base

    @app_commands.command(name="카드짝", description="카드 짝 맞추기 게임을 플레이합니다")
    async def MemoryGame(self, interaction: discord.Interaction):
        command_userid = interaction.user.id
        variables = MemoryGameVars()
        base=Game.MemoryGameGrid(variables.cards_dis)
        embed = discord.Embed(
                title="카드 짝 맞추기",
                description=base)
        view = MemoryGameView(variables, command_userid)
        await interaction.response.send_message(embed=embed, view=view)

    @app_commands.command(name="운세", description="오늘의 운세입니다")
    async def DailyLuck(self, interaction: discord.Interaction):
        user_id = interaction.user.id

        f = open(os.path.join(f"{__location__}\\DailyLuck\\DailyLuckCSV.csv"), 'r')
        fr = csv.reader(f)
        luck_text = ""

        for line in fr:
            if line[0] == str(user_id):
                luck_text = line[1]
                break

        f.close()
        
        if luck_text == "":
            luck_text = DailyLuckMsg[random.randint(0,127)]
            f = open(os.path.join(f"{__location__}\\DailyLuck\\DailyLuckCSV.csv"), 'a', newline='')
            fw = csv.writer(f)
            fw.writerow([user_id, luck_text])
            f.close()

        cur_time = datetime.datetime.now(timezone.utc)
        cur_time += datetime.timedelta(hours=9)
        date_text = cur_time.strftime("%m")+"월"+" "+cur_time.strftime("%d")+"일"
        
        image = Image.open(os.path.join(f"{__location__}\\DailyLuck\\DailyLuckImg.jpg"))
        fonts_dir = os.path.join(f"{__location__}\\DailyLuck")
        draw = ImageDraw.Draw(image)
        draw.text((410,40),date_text,font=ImageFont.truetype(os.path.join(fonts_dir, 'Dobong_Cultural_Routes(TTF).ttf'), 35), fill=(210,210,210))
        image.save(os.path.join(f"{__location__}\\DailyLuck\\DailyLuckImgDate.jpg"))

        msg = ""
        n = len(luck_text)//10
        for i in range(n):
            msg += luck_text[i*10:(i+1)*10]
            msg += "\n"
        msg += luck_text[n*10:]

        image = Image.open(os.path.join(f"{__location__}\\DailyLuck\\DailyLuckImgDate.jpg"))
        fonts_dir = os.path.join(f"{__location__}\\DailyLuck")
        draw = ImageDraw.Draw(image)
        draw.text((360,95),msg,font=ImageFont.truetype(os.path.join(fonts_dir, 'Dobong_Cultural_Routes(TTF).ttf'), 35), fill=(255,255,255))
        image.save(os.path.join(f"{__location__}\\DailyLuck\\DailyLuckImgEdit.jpg"))

        embed = discord.Embed(title="오늘의 운세", colour=discord.Colour(0x71368a))
        file = discord.File(os.path.join(f"{__location__}\\DailyLuck\\DailyLuckImgEdit.jpg"), filename="image.jpg")
        embed.set_image(url="attachment://image.jpg")
        embed.set_author(name="성의", icon_url="https://pbs.twimg.com/profile_images/2541389832/oph3xdipc43uupewwjau_400x400.png")
        await interaction.response.send_message(embed=embed, file=file)

    @tasks.loop(time= rest_time)
    async def reset_attendence(self):
        f = open(os.path.join(f"{__location__}\\DailyLuck\\DailyLuckCSV.csv"), "w")
        f.truncate()
        f.close()

    def RecruitMsg(topic, people, lst):
        msg = ""
        if len(lst) > 0:
            for i in range(len(lst)):
                msg += f"{i}. {lst[i]}\n"
        else:
            msg += "아직 아무도 모집되지 않았습니다"
        return msg

    async def RecruitEnd(interaction, topic):
        for i in range(604800):
            await asyncio.sleep(1)
            print(i,"초")
        embed = discord.Embed(
                title=f"{topic}",
                description="모집 시간이 만료되었습니다",
                colour=discord.Colour(0xE67E22))
        embed.set_author(name="나래", icon_url="https://i.imgur.com/i0SbMqN.jpg")
        try:
            await interaction.response.edit_message(embed=embed, view=None)
        except:
            await interaction.edit_original_response(embed=embed,view=None)

    @app_commands.command(name="모집", description="인원수만큼 사람을 모집합니다")
    async def recruit(self, interaction: discord.Interaction, topic: str, people: int=10):
        lst = []
        msg = Game.RecruitMsg(topic, people, lst)

        exit_button = Button(label="취소", style=discord.ButtonStyle.red, emoji="🏃")
        join_button = Button(label="참여", style=discord.ButtonStyle.green, emoji="🥑")
        async def join_button_callback(interaction):
            if len(lst) >= people:
                await interaction.response.send_message("이미 모집이 끝났습니다", ephemeral=True)
            else:
                if str(interaction.user) in lst:
                    await interaction.response.send_message("이미 참여했습니다", ephemeral=True)
                else:
                    lst.append(str(interaction.user))
                    msg = Game.RecruitMsg(topic, people, lst)
                    embed = discord.Embed(
                            title=f"{topic} : {len(lst)}/{people}",
                            description=msg,
                            colour=discord.Colour(0xE67E22))
                    embed.set_author(name="나래", icon_url="https://i.imgur.com/i0SbMqN.jpg")
                    await interaction.response.edit_message(embed=embed, view=view)

        async def exit_button_callback(interaction):
            if str(interaction.user) in lst:
                lst.remove(str(interaction.user))
                msg = Game.RecruitMsg(topic, people, lst)
                embed = discord.Embed(
                        title=f"{topic} : {len(lst)}/{people}",
                        description=msg,
                        colour=discord.Colour(0xE67E22))
                embed.set_author(name="나래", icon_url="https://i.imgur.com/i0SbMqN.jpg")
                await interaction.response.edit_message(embed=embed, view=view)
            else:
                await interaction.response.send_message("참여하지 않은 인원은 참여를 취소할 수 없습니다", ephemeral=True)
        
        exit_button.callback = exit_button_callback
        join_button.callback = join_button_callback
        view = View(timeout=None)
        view.add_item(join_button)
        view.add_item(exit_button)
        embed = discord.Embed(
                title=f"{topic} : {len(lst)}/{people}",
                description=msg,
                colour=discord.Colour(0xE67E22))
        embed.set_author(name="나래", icon_url="https://i.imgur.com/i0SbMqN.jpg")

        await interaction.response.send_message(embed=embed, view=view)

        await Game.RecruitEnd(interaction, topic)

async def setup(bot):
    await bot.add_cog(Game(bot))
