import discord,random,string,array
import asyncio
from discord import app_commands,Interaction,Reaction,InteractionResponse
from discord.ui import Button, View
from discord.ext import commands, tasks

blackjack_dict = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'J': 10, 'K': 10, 'Q': 10}

class BlackJackButtons(Button):
    def __init__(self, label, button_style, emoji, custom_id, command_userid, bet_money, user_deck, bot_deck, cards):
        super().__init__(label=label, style=button_style, emoji=emoji, custom_id=custom_id)
        self.custom_id, self.user_rcp, self.command_userid, self.bet_money = str(custom_id), emoji + label, command_userid, bet_money
        self.user_deck = user_deck
        self.bot_deck = bot_deck
        self.cards = cards

    async def create_msg(deck):
        num_ace = 0
        cards_msg = ""
        total = 0
        for i in deck:
            cards_msg += f'{i}, '
            try:
                total += blackjack_dict[i[1]]
            except:
                num_ace += 1
        
        for i in range(num_ace):
            if total + 11 < 22:
                total += 11
            else:
                total += 1
        return total, cards_msg

    async def callback(self, interaction):
        if interaction.user.id == self.command_userid:
            if self.custom_id == "hit":
                self.user_deck.append(self.cards.pop(random.randrange(len(self.cards))))
            else:
                pass
            user_total, user_cards_msg = await BlackJackButtons.create_msg(self.user_deck)
            bot_total, bot_cards_msg = await BlackJackButtons.create_msg(self.bot_deck)
            if user_total < 22:
                msg = user_cards_msg + f'유저: {user_total}' + "\n" + bot_cards_msg + f'봇: {bot_total}' + f'\n 베팅: {self.bet_money}'
                embed = discord.Embed(title='블랙잭', description=msg)
                await interaction.response.edit_message(embed=embed)
            else:
                msg = user_cards_msg + f'유저: {user_total}' + "\n" + bot_cards_msg + f'봇: {bot_total}' + f'\n 베팅: {self.bet_money}' + "\n 너 짐  ㅅㄱ 이돈 내꺼ㅋ"
                embed = discord.Embed(title='블랙잭', description=msg)
                await interaction.response.edit_message(embed=embed, view=None)
        else:
            await interaction.response.send_message(content="너 이거 못눌러", ephemeral=True)

class RcpButtons(Button): #가위바위보 메시지 버튼 생성 오브젝트
    def __init__(self, label, emoji, custom_id, command_userid, bet_money):
        """
    _summary_
    클래스 안으로 값 받아옴
    Args:
        self (obj, 필수): 오브젝트
        label (str, 필수): 버튼이 보여줄 글
        emoji (str, 필수): 버튼에 있을 이모지
        custom_id (str, 필수): 버튼 고유 id
        command_userid (str, 필수): 커맨드 사용한 유저 고유 id
        bet_money (int, 필수): 베팅한 돈
        """
        super().__init__(label=label, style=discord.ButtonStyle.green, emoji=emoji, custom_id=custom_id)
        self.custom_id, self.user_rcp, self.command_userid, self.bet_money = str(custom_id), emoji + label, command_userid, bet_money
    
    async def rcp_result(user_rcp):
        """
        _summary_
        가위바위보 결과 계산함
        Args:
            user_rcp (str, 필수): 무슨 버튼이 눌렸는지 버튼 고유 id 불러온거임
        Return
            bot_rcp (str, 필수): 봇이 뭐냈는지
            result (str, 필수): 이겼는지 졌는지
        """
        rcp_num = random.randint(1,3)
        if rcp_num == 1:
            bot_rcp = "✌️가위"
            if user_rcp == "scissors":
                result = "draw"
            elif user_rcp == "rock":
                result = "win"
            else:
                result = "lose"
        elif rcp_num == 2:
            bot_rcp = "✊바위"
            if user_rcp == "scissors":
                result = "lose"
            elif user_rcp == "rock":
                result = "draw"
            else:
                result = "win"
        else:
            bot_rcp = "✋보"
            if user_rcp == "scissors":
                result = "win"
            elif user_rcp == "rock":
                result = "lose"
            else:
                result = "draw"
        return bot_rcp, result
    
    async def callback(self, interaction):
        """
    _summary_
    버튼 눌렀을 때 반응 구분/실행
    이겼으면 돈 지금
    비기면 돈 뺏음
    지면 돈 뺏음
    Args:
        interaction (discord.interaction, 필수): 버튼 누른 사람 & interaction
        """
        if interaction.user.id == self.command_userid:
            bot_rcp, result = await RcpButtons.rcp_result(self.custom_id)
            if result == "win":
                result = "이김"
                message = f'{self.bet_money} 얻음'
                #money_increase(int(round(self.bet_money * 0.5, 0)), user)
            elif result == "draw":
                result = "비김"
                message = f'{int(round(self.bet_money * 0.5, 0))} 잃음'
                #money_decrease(int(round(self.bet_money * 0.5, 0)), user)
            else:
                result = "짐"
                message = f'{self.bet_money} 잃음'
                #money_decrease(self.bet_money, user)
            if self.bet_money == 0:
                message = "재미용 가위바위보가 좋냐?"
            embed = discord.Embed(title=result, description=f'페이:{bot_rcp}\n나:{self.user_rcp}\n{message}', color=0xb0a7d3)
            embed.set_author(name="폐이", icon_url="https://i.imgur.com/OdIiI2V.jpg")
            await interaction.response.edit_message(content="", embed=embed, view=None)
        else:
            await interaction.response.send_message(content="너 이거 못눌러", ephemeral=True)

class Game(commands.Cog):
    channel_id:string
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("준비됨")

    @app_commands.command(name="블랙잭", description="폐이와 블랙잭을 합니다")
    async def blackjack(self, interaction: discord.Interaction, bet_money: int = 0):
        owned_money = 1000
        if bet_money <= owned_money:
            cards = ['s1', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9', 'sJ', 'sK', 'sQ', 'sA', 
            'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'hJ', 'hK', 'hQ', 'hA', 
            'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8', 'd9', 'dJ', 'dK', 'dQ', 'dA', 
            'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'cJ', 'cK', 'cQ', 'cA']

            user_deck = []
            bot_deck = []
            user_total = 0
            bot_total = 0
            for i in range(2):
                user_deck.append(cards.pop(random.randrange(len(cards))))
                bot_deck.append(cards.pop(random.randrange(len(cards))))
            user_total, user_cards_msg = await BlackJackButtons.create_msg(user_deck)
            bot_total, bot_cards_msg = await BlackJackButtons.create_msg(bot_deck)
            msg = user_cards_msg + f'유저: {user_total}' + "\n" + bot_cards_msg + f'봇: {bot_total}' + f'\n 베팅: {bet_money}'
            if user_total != 21:
                view = View()
                view.add_item(BlackJackButtons('히트', discord.ButtonStyle.green, "🃏", "hit", interaction.user.id, bet_money, user_deck, bot_deck, cards))
                view.add_item(BlackJackButtons('스탠드', discord.ButtonStyle.red, "🖐🏻", "stand", interaction.user.id, bet_money, user_deck, bot_deck, cards))
                embed = discord.Embed(title='블랙잭', description=msg)
                await interaction.response.send_message(embed=embed, view=view)
            else:
                if bot_total != 21:
                    msg += f'\n 축하해 ㅋ 블랙잭이농. 옜다 {bet_money * 1.5}'
                    embed = discord.Embed(title='블랙잭', description=msg)
                    await interaction.response.send_message(embed=embed)
                else:
                    msg += f'\n 축하해 ㅋ 블랙잭이농. 근데 비겼쥬 ㅋ'
                    embed = discord.Embed(title='블랙잭', description=msg)
                    await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(content="돈 부족. 너 돈 필요.", ephemeral=True)

    @app_commands.command(name="가위바위보", description="폐이와 가위바위보를 합니다")
    async def buttontest(self, interaction: discord.Interaction, bet_money: int = 0):
        """
        _summary_
        View obj 생성
        view 오브젝트에 버튼 3개 가위바위보 추가
        돈 충분한지 확인
        Args:
            interaction (discord.interaction, 필수): 커맨드 쓴 사람 & interaction
            bet_money (int, 옵션): 돈 걸고싶은만큼
        """
        owned_money = 0
        if bet_money >= owned_money:
            view = View()
            view.add_item(RcpButtons('가위', "✌️", "scissors", interaction.user.id, bet_money))
            view.add_item(RcpButtons('바위', "✊", "rock", interaction.user.id, bet_money))
            view.add_item(RcpButtons('보', "✋", "paper", interaction.user.id, bet_money))
            embed = discord.Embed(title='가위바위보중에 하나 골라')
            await interaction.response.send_message(embed=embed, view=view)
        else:
            await interaction.response.send_message(content="돈 부족. 너 돈 필요.", ephemeral=True)

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

    @app_commands.command(name="가챠", description="호감도템 가챠")
    async def gacha(self, interaction: discord.Interaction):
        pos = {"Common": 40, "Rare": 45, "Epic": 12, "Legendary": 3}

        items = {
            "랑이1": "Common",
            "일반1": "Common",
            "치이1": "Common",
            "랑이2": "Rare",
            "일반2": "Rare",
            "치이2": "Rare",
            "일반3": "Epic",
            "치이3": "Epic",
            "랑이3": "Epic",
            "전설": "Legendary",
        }

        rarity = random.choices(list(pos.keys()), weights=list(pos.values()), k=1)[0]
        item = random.choice([k for k, v in items.items() if v == rarity])

        if rarity == "Legendary":
            emcolor=0xe67e22
        elif rarity == "Epic":
            emcolor=0x71368a
        elif rarity == "Rare":
            emcolor=0x3498db
        else:
            emcolor=0x2ecc71

        if "치이" in item:
            item_pic = "https://i.imgur.com/isUEgXb.png"
        elif "일반" in item:
            item_pic = "https://i.imgur.com/6UifvGD.png"
        elif "랑이" in item:
            item_pic = "https://i.imgur.com/GbH5Htg.png"
        else:
            item_pic = "https://i.imgur.com/FjhHwtU.jpeg"

        embed = discord.Embed(
            title="가챠 결과",
            description=f"{rarity} \n {item}",
            color=emcolor,
        )

        embed.set_image(url=item_pic)
        embed.set_footer(text=f"총 보유량:{item}")
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Game(bot))
