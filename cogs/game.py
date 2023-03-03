import discord,random,string,array,time
import asyncio
from discord import app_commands,Interaction,Reaction,InteractionResponse
from discord.ui import Button, View
from discord.ext import commands, tasks

blackjack_dict = {'1':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'J':10, 'K':10, 'Q':10}
slotmachine_dict = {1:"<:slot_1:1081172877233102892>",
2:"<:slot_2:1081172892034801706>",
3:"<:slot_3:1081172902617038879>",
4:"<:slot_4:1081172912331042856>",
5:"<:slot_5:1081172922812604446>",
6:"<:slot_6:1081172931729702922>",
7:"<:slot_7:1081172941246578778>",
8:"<:slot_8:1081172951606505472>",
9:"<:slot_9:1081172962411036753>",
11:"<a:slot_fruits:1081172981620936734>"}

class BlackJackButtons(Button):
    def __init__(self, label, button_style, emoji, custom_id, command_userid, bet_money, user_deck, bot_deck, cards):
        """
        _summary_
        클래스 안으로 값 받아옴
        Args:
            self (obj, 필수): 오브젝트
            label (str, 필수): 버튼이 보여줄 글
            button_style (str, 필수): 버튼 색
            emoji (str, 필수): 버튼에 있을 이모지
            custom_id (str, 필수): 버튼 고유 id
            command_userid (str, 필수): 커맨드 사용한 유저 고유 id
            bet_money (int, 필수): 베팅한 돈
            user_deck (list, 필수): 유저의 덱 정보
            bot_deck (list, 필수): 봇의 덱 정보
            cards (list, 필수): 남은 카드 정보
        """
        super().__init__(label=label, style=button_style, emoji=emoji, custom_id=custom_id)
        self.custom_id, self.user_rcp, self.command_userid, self.bet_money = str(custom_id), emoji + label, command_userid, bet_money
        self.user_deck = user_deck
        self.bot_deck = bot_deck
        self.cards = cards

    async def create_msg(deck, bot):
        """
        _summary_
        받은 덱 값 합산
        덱 메시지 생성
        Args:
            deck (list, 필수): 결과 계산을 위한 덱
            bot (boolean, 필수): 봇인지 아닌지에 따라 용도에 맞는 메시지 형태 리턴
        Returns:
            total: 받은 덱 값 합산
            cards_msg: 덱 메시지 생성
        """
        num_ace = 0
        cards_msg = ""
        total = 0
        for i in deck:
            cards_msg += f'{i}, '
            try:
                total += blackjack_dict[i[1]]
            except:
                num_ace += 1
        if total + num_ace > 21:
            total += num_ace
        else:
            for i in range(num_ace + 1):
                num = (11 * (num_ace - i)) + (1 * i)
                if num + total < 22:
                    total += num
                    break
        cards_msg = cards_msg[0:-2]
        if bot:
            cards_msg = cards_msg[0:2]
        return total, cards_msg

    async def stand(self, interaction):
        """
        _summary_
        stand 버튼 누르면 작동
        봇의 덱 채우기
        봇의 덱 합산이 16이 넘을때까지 hit
        봇의 덱 결과에 따른 답변/결과
        Args:
            self (obj, 필수): 버튼에 대한 정보를 담는 오브젝트
            interaction (discord.interaction, 필수): interaction에 대한 정보를 담는 오브젝트
        """
        bot_total, bot_cards_msg = await BlackJackButtons.create_msg(self.bot_deck, False)
        while bot_total < 17:
            self.bot_deck.append(self.cards.pop(random.randrange(len(self.cards))))
            bot_total, bot_cards_msg = await BlackJackButtons.create_msg(self.bot_deck, False)
        user_total, user_cards_msg = await BlackJackButtons.create_msg(self.user_deck, False)

        if bot_total < 22:
            if user_total > bot_total:
                msg = user_cards_msg + f' 유저: {user_total}' + "\n" + bot_cards_msg + f' 봇: {bot_total}' + f'\n 베팅: {self.bet_money}' + "\n 당신이 이겼습니다!"
                embed = discord.Embed(title='블랙잭', description=msg, color=0xb0a7d3)
                embed.set_author(name="폐이", icon_url="https://i.imgur.com/OdIiI2V.jpg")
                await interaction.response.edit_message(embed=embed, view=None)
            elif user_total == bot_total:
                msg = user_cards_msg + f' 유저: {user_total}' + "\n" + bot_cards_msg + f' 봇: {bot_total}' + f'\n 베팅: {self.bet_money}' + "\n 동점이네요!"
                embed = discord.Embed(title='블랙잭', description=msg, color=0xb0a7d3)
                embed.set_author(name="폐이", icon_url="https://i.imgur.com/OdIiI2V.jpg")
                await interaction.response.edit_message(embed=embed, view=None)
            else:
                msg = user_cards_msg + f' 유저: {user_total}' + "\n" + bot_cards_msg + f' 봇: {bot_total}' + f'\n 베팅: {self.bet_money}' + "\n 제가 이겼군요!"
                embed = discord.Embed(title='블랙잭', description=msg, color=0xb0a7d3)
                embed.set_author(name="폐이", icon_url="https://i.imgur.com/OdIiI2V.jpg")
                await interaction.response.edit_message(embed=embed, view=None)
        else:
            msg = user_cards_msg + f' 유저: {user_total}' + "\n" + bot_cards_msg + f' 봇: {bot_total}' + f'\n 베팅: {self.bet_money}' + "\n 제 버스트네요!"
            embed = discord.Embed(title='블랙잭', description=msg, color=0xb0a7d3)
            embed.set_author(name="폐이", icon_url="https://i.imgur.com/OdIiI2V.jpg")
            await interaction.response.edit_message(embed=embed, view=None)

    async def hit(self, interaction):
        """
        _summary_
        hit 버튼 누르면 작동
        유저의 덱 채우기
        유저의 덱 결과에 따른 답변/결과
        Args:
            self (obj, 필수): 버튼에 대한 정보를 담는 오브젝트
            interaction (discord.interaction, 필수): interaction에 대한 정보를 담는 오브젝트
        """
        self.user_deck.append(self.cards.pop(random.randrange(len(self.cards))))
        user_total, user_cards_msg = await BlackJackButtons.create_msg(self.user_deck, False)
        bot_total, bot_cards_msg = await BlackJackButtons.create_msg(self.bot_deck, True)
        if user_total == 21:
            await BlackJackButtons.stand(self, interaction)
        elif user_total < 22:
            msg = user_cards_msg + f' 유저: {user_total}' + "\n" + bot_cards_msg + f' 봇: ...' + f'\n 베팅: {self.bet_money}'
            embed = discord.Embed(title='블랙잭', description=msg, color=0xb0a7d3)
            embed.set_author(name="폐이", icon_url="https://i.imgur.com/OdIiI2V.jpg")
            await interaction.response.edit_message(embed=embed)
        else:
            msg = user_cards_msg + f' 유저: {user_total}' + "\n" + bot_cards_msg + f' 봇: ...' + f'\n 베팅: {self.bet_money}' + "\n 버스트하셨습니다!"
            embed = discord.Embed(title='블랙잭', description=msg, color=0xb0a7d3)
            embed.set_author(name="폐이", icon_url="https://i.imgur.com/OdIiI2V.jpg")
            await interaction.response.edit_message(embed=embed, view=None)

    async def callback(self, interaction):
        """
        _summary_
        어떤 버튼이든 누르면 작동
        누른 버튼에 맞는 기능(function)으로 연결
        명령어 사용자 외 사용자의 버튼 사용 방지
        Args:
            self (obj, 필수): 버튼에 대한 정보를 담는 오브젝트
            interaction (discord.interaction, 필수): interaction에 대한 정보를 담는 오브젝트
        """
        if interaction.user.id == self.command_userid:
            if self.custom_id == "hit":
                await BlackJackButtons.hit(self, interaction)
            else:
                await BlackJackButtons.stand(self, interaction)
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
            user_rcp (str, 필수): 무슨 버튼이 눌렸는지 버튼 고유 id 불러옴
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
        이겼으면 돈 지급
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

    async def embed_create_slotmachine(var_list, result, interaction):
        """
        _summary_
        값들을 받아서 슬롯머신의 형태로 유저에게 보여주는 펑션
        Args:
            interaction (discord.interaction, 필수): 커맨드 쓴 사람 & interaction
            var_list (list, 필수): 알맞은 상징 디스플레이를 위한 리스트
            result (str, 필수): 계산된 결과 값 디스플레이
        """
        embed = discord.Embed(title="🎰𝕊𝕃𝕆𝕋𝕊🎰", description=f'——————\n|{slotmachine_dict[var_list[0]]}|{slotmachine_dict[var_list[1]]}|{slotmachine_dict[var_list[2]]}|\n——————\n{result}', color=0xb0a7d3)
        embed.set_author(name="폐이", icon_url="https://i.imgur.com/OdIiI2V.jpg")
        try:
            await interaction.response.send_message(embed=embed)
        except:
            await interaction.edit_original_response(embed=embed)

    @app_commands.command(name="슬롯머신", description="폐이의 슬롯머신을 돌립니다")
    async def slotmachine(self, interaction: discord.Interaction, bet_money: int):
        """
        _summary_
        돈 충분한지 확인
        임의의 값 3개 만들고 그에 맞는 결과 도출
        유저에게 슬롯이 돌아가는 모습 디스플레이
        Args:
            interaction (discord.interaction, 필수): 커맨드 쓴 사람 & interaction
            bet_money (int, 필수): 돈 걸고 싶은만큼
        """
        owned_money = 100
        if bet_money <= owned_money:
            var1 = random.randint(1,9)
            var2 = random.randint(1,9)
            var3 = random.randint(1,9)
            var_list = [[11,11,11],[var1,11,11],[var1,var2,11],[var1,var2,var3]]
            for i in var_list:
                embed = await Game.embed_create_slotmachine(i, "결과: ...", interaction)
                await asyncio.sleep(1)
            if var1 == 1 and var2 == 1 and var3 == 1:
                result = "잭팟입니다!"
            elif var1 == var2 and var2 == var3:
                result = "트리플입니다!"
            elif var1 == var2 or var1 == var3 or var2 == var3:
                result = "페어입니다!"
            else:
                result = "꽝입니다!"
            embed = await Game.embed_create_slotmachine(var_list[3], result, interaction)
        else:
            await interaction.response.send_message(content="돈 부족. 너 돈 필요.", ephemeral=True)

    @app_commands.command(name="블랙잭", description="폐이와 블랙잭을 합니다")
    async def blackjack(self, interaction: discord.Interaction, bet_money: int = 0):
        """
        _summary_
        View obj 생성
        view 오브젝트에 버튼 2개 hit, stand 추가
        돈 충분한지 확인
        카드 덱 정의
        유저, 봇 각각 카드 2장씩 할당, 이에 따른 조건부 결과(블랙잭 등)
        Args:
            interaction (discord.interaction, 필수): 커맨드 쓴 사람 & interaction
            bet_money (int, 옵션): 돈 걸고 싶은만큼
        """
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
            user_total, user_cards_msg = await BlackJackButtons.create_msg(user_deck, False)
            bot_total, bot_cards_msg = await BlackJackButtons.create_msg(bot_deck, True)
            msg = user_cards_msg + f' 유저: {user_total}' + "\n" + bot_cards_msg + f' 봇: ...' + f'\n 베팅: {bet_money}'
            
            if user_total != 21:
                if bot_total == 21:
                    msg += f'\n 제가 블랙잭이군요!'
                    embed = discord.Embed(title='블랙잭', description=msg, color=0xb0a7d3)
                    embed.set_author(name="폐이", icon_url="https://i.imgur.com/OdIiI2V.jpg")
                    await interaction.response.send_message(embed=embed)
                else:
                    view = View()
                    view.add_item(BlackJackButtons('히트', discord.ButtonStyle.green, "🃏", "hit", interaction.user.id, bet_money, user_deck, bot_deck, cards))
                    view.add_item(BlackJackButtons('스탠드', discord.ButtonStyle.red, "🖐🏻", "stand", interaction.user.id, bet_money, user_deck, bot_deck, cards))
                    embed = discord.Embed(title='블랙잭', description=msg, color=0xb0a7d3)
                    embed.set_author(name="폐이", icon_url="https://i.imgur.com/OdIiI2V.jpg")
                    await interaction.response.send_message(embed=embed, view=view)
            else:
                if bot_total != 21:
                    msg += f'\n 블랙잭 축하드려요!'
                    embed = discord.Embed(title='블랙잭', description=msg, color=0xb0a7d3)
                    embed.set_author(name="폐이", icon_url="https://i.imgur.com/OdIiI2V.jpg")
                    await interaction.response.send_message(embed=embed)
                else:
                    msg += f'\n 저희 둘 다 블랙잭인가봅니다!'
                    embed = discord.Embed(title='블랙잭', description=msg, color=0xb0a7d3)
                    embed.set_author(name="폐이", icon_url="https://i.imgur.com/OdIiI2V.jpg")
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
            bet_money (int, 옵션): 돈 걸고 싶은만큼
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
