import discord
from discord import app_commands
from discord.ext import commands, tasks
import pymongo
import json
import os
import random
import datetime
from time import gmtime, strftime

import string,array,time
import asyncio
from discord import Interaction,Reaction,InteractionResponse
from discord.ui import Button, View
item_list_convert = {"rangi_hanbok": "개량한복",
            "saehee_shotglass": "술잔",
            "chiyee_gookja": "국자",
            "rangi_jeogorri": "저고리",
            "chiyee_hairband": "깃털 머리띠",
            "saehee_sotlid": "솥뚜껑",
            "rangi_teeth": "이빨",
            "saehee_beenyo": "비녀",
            "chiyee_julmuni": "줄무늬 그것",
            "legendary_saliva": "대요괴의 침"
}
character_name = {"rangi": "랑이",
                "chiyee": "치이",
                "saehee": "세희"}

list_dev_id = ["339767912841871360", "474389454262370314", "393932860597338123", "185181025104560128"]
all_hi = ["안녀", "안녕", "안뇽", "안뇨", "어서와", "히사시부리", "하이", "반가워", "오랜만이야", "나 또 왔", 
        "좋은 아침", "잘 잤", "좋은 밤", "좋은 저녁", "좋은 점심", "여기야", "반갑다", 
        "돌아왔", "나 왔어", "나 왔", "갔다 왔", "다녀왔"]
all_what = ["뭐해", "뭐하니", "뭐하냐", "뭐하고"]
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
utc = datetime.timezone.utc
rest_time = datetime.time(hour=19, minute=00, tzinfo=utc) #19 00 오전 4시 utf + 9 대한민국
birthday_time = datetime.time(hour=15, minute=00, tzinfo=utc) #15 00 오전 12시 utf + 9 대한민국

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

class Character(discord.ui.View):
    def __init__(self, self_, user_id):
        self.self_ = self_
        self.user_id = user_id
        super().__init__()
        self.add_item(CharacterSelect(self.self_, self.user_id))

class ConfirmGui(discord.ui.View):
    def __init__(self, self_, user_id, birth_date):
        self.self_ = self_
        self.user_id = user_id
        self.birth_date = birth_date
        super().__init__()
        self.add_item(CharacterSelect(self.self_, user_id, birth_date))

class ConfirmButton(discord.ui.Button):
    def __init__(self, self_, button_style, label, custom_id,  character = None, user_id = None, birth_date = None)-> None:
        self.self_= self_
        self.character = character
        self.user_id = user_id
        self.birth_date = birth_date
        super().__init__(
            style=button_style, label=label, custom_id=custom_id
        )

    async def callback(self, interaction: discord.Interaction):
        no = ConfirmGui(self.self_, str(interaction.user.id), self.birth_date) 
        month, day = (self.birth_date).split("/")[0], (self.birth_date).split("/")[1]
        if self.custom_id == "yes" and self.birth_date != None:
            if self.character == "rangi":
                embed= discord.Embed(title=f"낭군님의 생일 {month}월 {day}일을 기억 하겠느니라!",
                    description="절대 잊지 않겠느니라!! 꼭 축하해줄 것이니라!!",color=0x0aa40f)
                embed.set_author(name="랑이", icon_url="https://i.imgur.com/huDPd5o.jpg")
            elif self.character == "chiyee":
                embed= discord.Embed(title=f"오라버니의 생일은 {month}월 {day}일인 거예요!",
                    description="제가 꼭 축하해 드릴 거예요!",color=0x0aa40f)
                embed.set_author(name="치이", icon_url="https://i.imgur.com/aApUYMj.jpg")
            elif self.character == "saehee":
                embed= discord.Embed(title=f"{month}월 {day}일은 저주 받은 날이군요",
                    description="기억나면 뭐 축하하는 척이라도 해드리겠습니다. 기대는 하지 마시지요, 레이드 뛰는 날이면 못해드립니다",color=0x0aa40f)
                embed.set_author(name="세희", icon_url="https://i.imgur.com/7a4oeOi.jpg")
            await interaction.response.edit_message(embed=embed, view=None)
            UserData.update_birthday(self.self_, str(interaction.user.id), self.birth_date)
            UserData.update_birthday_character(self.self_, str(interaction.user.id), self.character)
        elif self.custom_id == "yes" and self.birth_date == None:
            if self.character == "rangi":
                embed= discord.Embed(title=f"내가 낭군님의 생일을 축하해주겠느니라!", color=0x0aa40f)
                embed.set_author(name="랑이", icon_url="https://i.imgur.com/huDPd5o.jpg")
            elif self.character == "chiyee":
                embed= discord.Embed(title=f"오라버니의 생일은 제가 축하해 드리는 거예요!",color=0x0aa40f)
                embed.set_author(name="치이", icon_url="https://i.imgur.com/aApUYMj.jpg")
            elif self.character == "saehee":
                embed= discord.Embed(title=f"왜 하필 접니까 도련님",color=0x0aa40f)
                embed.set_author(name="세희", icon_url="https://i.imgur.com/7a4oeOi.jpg")
            await interaction.response.edit_message(embed=embed, view=None)
            UserData.update_birthday_character(self.self_, str(interaction.user.id), self.character)
        elif self.custom_id == "no":
            await interaction.response.edit_message(view=no)

class CharacterSelect(discord.ui.Select):
    def __init__(self, self_, user_id, birth_date):
        self.self_ = self_
        self.user_id = user_id
        self.birth_date = birth_date
        options=[
            discord.SelectOption(label="랑이", value="rangi"),
            discord.SelectOption(label="치이", value="chiyee"),        
            discord.SelectOption(label="세희", value="saehee")
        ]
        super().__init__(
            placeholder="생일 축하 캐릭터 선택(추후 변경가능)", options=options, min_values=1, max_values=1
        )
        
    async def callback(self, interaction: discord.Interaction):
        view = ConfirmGui(self.self_, str(interaction.user.id), self.birth_date)
        self.character_selected = self.values[0]
        name = character_name[self.character_selected]
        embed=discord.Embed(title=f"{name}(을)를 선택하셨습니다", color=0xe8dbff)
        button_yes = ConfirmButton(self.self_, discord.ButtonStyle.green,"네", "yes", self.character_selected, self.user_id, self.birth_date)
        button_no = ConfirmButton(self.self_, discord.ButtonStyle.danger, "아니요", "no") 
        view.add_item(button_yes)
        view.add_item(button_no)

        await interaction.response.edit_message(view=view, embed=embed)

class ChoseGUI(discord.ui.View):
    def __init__(self, self_, user_id):
        self.self_ = self_
        self.user_id = user_id
        super().__init__()
        self.add_item(GiftSelect(self.self_, user_id))


class VerifyButton(discord.ui.Button):
    def __init__(self, self_, button_style, label, custom_id, item_key: str = None, item:str = None, character:str = None)-> None:
        self.item = item
        self.character = character
        self.item_key = item_key
        self.self_= self_
        self.rangi_item = {"개량한복": random.randrange(1,5),"저고리":  random.randrange(5,10), "이빨":  random.randrange(15,30)}
        self.chiyee_item = {"국자":  random.randrange(1,5),"깃털 머리띠":  random.randrange(5,10), "줄무늬 그것":  random.randrange(20,40)}
        self.saehee_item = {"술잔":  random.randrange(1,5),"솥뚜껑":  random.randrange(5,10), "비녀":  random.randrange(15,30)}
        self.all_items = {
                        "개량한복": random.randrange(1,5),"저고리":  random.randrange(5,10), "이빨":  random.randrange(15,30), 
                        "국자":  random.randrange(1,5),"깃털 머리띠":  random.randrange(5,10), "줄무늬 그것":  random.randrange(15,30),
                        "술잔":  random.randrange(1,5),"솥뚜껑":  random.randrange(5,10), "비녀":  random.randrange(15,30), "대요괴의 침": random.randrange(80,100)}
        super().__init__(
            style=button_style, label=label, custom_id=custom_id
        )

    def check_bonus(self, item, item_dict):
        if item in list(item_dict.keys()):
            xp = round(item_dict[item] * 1.3)
            return xp
        else:
            xp = self.all_items[item]
            return round(xp)
            
    def check_item(self, item_key: str, user_id: str):
        amount =  UserData.get_attribute(self.self_, str(user_id), str(item_key))
        if amount >= 1:
            return True
        else: False
        
    async def callback(self, interaction: discord.Interaction):
        no = ChoseGUI(self.self_, str(interaction.user.id)) 
        if self.custom_id == "yes" and self.check_item(self.item_key, interaction.user.id):
            if self.character == "rangi":
                embed=discord.Embed(title=f"랑이에게 {self.item}(을)를 선물했습니다", description=f"역시 {interaction.user.name} 낭군님 이니라! 정말정말 기쁘니라!!")
                embed.set_author(name="랑이 ", icon_url="https://i.imgur.com/huDPd5o.jpg") 
                xp = self.check_bonus(self.item, self.rangi_item)
            elif self.character == "chiyee":
                embed=discord.Embed(title=f"치이에게 {self.item}(을)를 선물했습니다", description=f"아우우우!? {interaction.user.name} 오라버니에게 항상 받기만 해서 죄송한 거예요!! 감사한 거예요!!")
                embed.set_author(name="치이 ", icon_url="https://i.imgur.com/aApUYMj.jpg")
                xp = self.check_bonus(self.item, self.chiyee_item)
            elif self.character == "saehee":
                embed=discord.Embed(title=f"세희에게 {self.item}(을)를 선물했습니다", description=f"허접투성이 {interaction.user.name} 도련님 치고는 괜찮은 선물이군요, 감사합니다")
                embed.set_author(name="saehee ", icon_url="https://i.imgur.com/7a4oeOi.jpg")
                xp = self.check_bonus(self.item, self.saehee_item)

            UserData.reduce_item(self.self_, str(interaction.user.id), self.item_key)
            await UserData.character_give_xp(self.self_, interaction.user.name, interaction.user.id, interaction.channel, xp, self.character)
            await interaction.response.edit_message(embed=embed, view=None)
            return interaction.message, xp, self.character
        elif self.custom_id == "no":
            await interaction.response.edit_message(view=no)
        else:
            embed=discord.Embed(title=f"{self.item}(을)를 보유하지 않습니다", description="/가챠 커맨드를 통해 뽑으세요")
            await interaction.response.edit_message(embed=embed, view=None)    
            
class CharacterButton(discord.ui.Button):
    def __init__(self, button_style, label, custom_id, item_kor:str, item_key:str, self_, command_userid) -> None:
        self.item_kor = item_kor
        self.item_key = item_key
        self.command_userid = command_userid
        self.self_ = self_
        super().__init__(
            style=button_style, label=label, custom_id=custom_id
        )

    async def callback(self, interaction: discord.Interaction):
        view = View()
        if str(interaction.user.id) == self.command_userid:
            if self.custom_id == "rangi":
                embed=discord.Embed(title=f"랑이에게 {self.item_kor}를 선물하시겠습니까?", description="흐냣?! 진짜 이걸 나에게 주는 것이느냐?")
                embed.set_author(name="랑이 ", icon_url="https://i.imgur.com/huDPd5o.jpg")
            elif self.custom_id == "chiyee":
                embed=discord.Embed(title=f"치이에게 {self.item_kor}를 선물하시겠습니까?", description="아우우우?!! 제게 선물 하시는건가요? 그런건가요!")
                embed.set_author(name="치이 ", icon_url="https://i.imgur.com/aApUYMj.jpg")
            elif self.custom_id == "saehee":
                embed=discord.Embed(title=f"세희에게 {self.item_kor}를 선물하시겠습니까?", description="또 무슨 헛수작이십니까?")
                embed.set_author(name="saehee ", icon_url="https://i.imgur.com/7a4oeOi.jpg")
                
            button_yes = VerifyButton(self.self_, discord.ButtonStyle.green,"네", "yes", self.item_key, self.item_kor, self.custom_id)
            button_no = VerifyButton(self.self_, discord.ButtonStyle.danger, "아니요", "no") 
            view.add_item(button_yes)
            view.add_item(button_no)
        else:
            await interaction.response.send_message(content="선물을 하고 싶으시면 /선물 을 하시면 됩니다 쓰레기 주인님", ephemeral=True)

        await interaction.response.edit_message(view=view, embed=embed)
        
class GiftSelect(discord.ui.Select):
    def __init__(self, self_, user_id):
        self.gift_selected = None
        self.self_ = self_
        self.user_id = user_id
        options=[
            discord.SelectOption(label=f"개량한복 || {UserData.get_attribute(self.self_, str(self.user_id), 'rangi_hanbok')}개 보유중", emoji= "🎁", description="", value="rangi_hanbok") ,
            discord.SelectOption(label=f"술잔 || {UserData.get_attribute(self.self_, str(self.user_id), 'saehee_shotglass')}개 보유중", emoji= "🎁", description="", value="saehee_shotglass") ,
            discord.SelectOption(label=f"국자 || {UserData.get_attribute(self.self_, str(self.user_id), 'chiyee_gookja')}개 보유중", emoji= "🎁", description="", value="chiyee_gookja") ,
            discord.SelectOption(label=f"저고리 || {UserData.get_attribute(self.self_, str(self.user_id), 'rangi_jeogorri')}개 보유중", emoji= "🎁", description="", value="rangi_jeogorri") ,
            discord.SelectOption(label=f"깃털 머리띠 || {UserData.get_attribute(self.self_, str(self.user_id), 'chiyee_hairband')}개 보유중", emoji= "🎁", description="", value="chiyee_hairband") ,
            discord.SelectOption(label=f"솥뚜껑 || {UserData.get_attribute(self.self_, str(self.user_id), 'saehee_sotlid')}개 보유중", emoji= "🎁", description="", value="saehee_sotlid") ,
            discord.SelectOption(label=f"이빨 || {UserData.get_attribute(self.self_, str(self.user_id), 'rangi_teeth')}개 보유중", emoji= "🎁", description="", value="rangi_teeth") ,
            discord.SelectOption(label=f"비녀 || {UserData.get_attribute(self.self_, str(self.user_id), 'saehee_beenyo')}개 보유중", emoji= "🎁", description="", value="saehee_beenyo") ,
            discord.SelectOption(label=f"줄무늬 그것 || {UserData.get_attribute(self.self_, str(self.user_id), 'chiyee_julmuni')}개 보유중", emoji= "🎁", description="", value="chiyee_julmuni") ,
            discord.SelectOption(label=f"대요괴의 침 || {UserData.get_attribute(self.self_, str(self.user_id), 'legendary_saliva')}개 보유중", emoji= "🎁", description="", value="legendary_saliva") ,
        ] 
        super().__init__(
            placeholder="선물 선택", options=options, min_values=1, max_values=1
        )

    async def callback(self, interaction: discord.Interaction):
        if str(interaction.user.id) == self.user_id:
            view = ChoseGUI(self.self_, str(interaction.user.id))
            
            self.gift_selected = self.values[0]
            name = item_list_convert[self.gift_selected]

            embed=discord.Embed(title=f"{name}을 선택하셨습니다", description="누구에게 선물할지 선택해주세요", color=0xe8dbff)

            button_rangi = CharacterButton(discord.ButtonStyle.green, "랑이", "rangi", name, self.gift_selected, self.self_)
            button_chiyee = CharacterButton(discord.ButtonStyle.green, "치이", "chiyee", name, self.gift_selected, self.self_)
            button_saehee = CharacterButton(discord.ButtonStyle.green, "세희", "saehee", name, self.gift_selected, self.self_)    
            view.add_item(button_rangi)
            view.add_item(button_chiyee)
            view.add_item(button_saehee)

            await interaction.response.edit_message(view=view, embed=embed)       
        else:
            await interaction.response.send_message(content="선물을 하고 싶으시면 /선물 을 하시면 됩니다 쓰레기 주인님", ephemeral=True)

class BlackJackButtons(Button):
    def __init__(self, label, button_style, emoji, custom_id, command_userid, bet_money, user_deck, bot_deck, cards, self_):
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
        self.self_ = self_

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
                msg = user_cards_msg + f' 유저: {user_total}' + "\n" + bot_cards_msg + f' 봇: {bot_total}' + f'\n 획득: {self.bet_money}' + "\n [......졌어.쳐다보지마]"
                embed = discord.Embed(title='블랙잭', description=msg, color=0xb0a7d3)
                embed.set_author(name="폐이", icon_url="https://i.imgur.com/OdIiI2V.jpg")
                await interaction.response.edit_message(embed=embed, view=None)
                await UserData.give_money(self.self_, interaction.user.id, (int(round(self.bet_money*2, 0))))
            elif user_total == bot_total:
                msg = user_cards_msg + f' 유저: {user_total}' + "\n" + bot_cards_msg + f' 봇: {bot_total}' + f'\n 잃음: 0' + "\n [동점.....나, 사랑해?]"
                embed = discord.Embed(title='블랙잭', description=msg, color=0xb0a7d3)
                embed.set_author(name="폐이", icon_url="https://i.imgur.com/OdIiI2V.jpg")
                await interaction.response.edit_message(embed=embed, view=None)
                await UserData.give_money(self.self_, interaction.user.id, (int(round(self.bet_money*1, 0))))
            else:
                msg = user_cards_msg + f' 유저: {user_total}' + "\n" + bot_cards_msg + f' 봇: {bot_total}' + f'\n 잃음: {self.bet_money}' + "\n [이겼어.허접.]"
                embed = discord.Embed(title='블랙잭', description=msg, color=0xb0a7d3)
                embed.set_author(name="폐이", icon_url="https://i.imgur.com/OdIiI2V.jpg")
                await interaction.response.edit_message(embed=embed, view=None)
        else:
            msg = user_cards_msg + f' 유저: {user_total}' + "\n" + bot_cards_msg + f' 봇: {bot_total}' + f'\n 획득: {self.bet_money}' + "\n [......버스트.실수.]"
            embed = discord.Embed(title='블랙잭', description=msg, color=0xb0a7d3)
            embed.set_author(name="폐이", icon_url="https://i.imgur.com/OdIiI2V.jpg")
            await interaction.response.edit_message(embed=embed, view=None)
            await UserData.give_money(self.self_, interaction.user.id, (int(round(self.bet_money*2, 0))))

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
            msg = user_cards_msg + f' 유저: {user_total}' + "\n" + bot_cards_msg + f' 봇: ...' + f'\n 잃음: {self.bet_money}' + "\n [버스트.허접.]"
            embed = discord.Embed(title='블랙잭', description=msg, color=0xb0a7d3)
            embed.set_author(name="폐이", icon_url="https://i.imgur.com/OdIiI2V.jpg")
            await interaction.response.edit_message(embed=embed, view=None)

    async def doubledown(self, interaction):
        self.bet_money = self.bet_money * 2

        self.user_deck.append(self.cards.pop(random.randrange(len(self.cards))))
        user_total, user_cards_msg = await BlackJackButtons.create_msg(self.user_deck, False)
        bot_total, bot_cards_msg = await BlackJackButtons.create_msg(self.bot_deck, True)
        if user_total <= 21:
            bot_total, bot_cards_msg = await BlackJackButtons.create_msg(self.bot_deck, False)
            while bot_total < 17:
                self.bot_deck.append(self.cards.pop(random.randrange(len(self.cards))))
                bot_total, bot_cards_msg = await BlackJackButtons.create_msg(self.bot_deck, False)
            user_total, user_cards_msg = await BlackJackButtons.create_msg(self.user_deck, False)

            if bot_total < 22:
                if user_total > bot_total:
                    msg = user_cards_msg + f' 유저: {user_total}' + "\n" + bot_cards_msg + f' 봇: {bot_total}' + f'\n 획득: {self.bet_money}' + "\n [......졌어.쳐다보지마]"
                    embed = discord.Embed(title='블랙잭', description=msg, color=0xb0a7d3)
                    embed.set_author(name="폐이", icon_url="https://i.imgur.com/OdIiI2V.jpg")
                    await interaction.response.edit_message(embed=embed, view=None)
                    await UserData.give_money(self.self_, interaction.user.id, (int(round(self.bet_money*-0.5, 0))))
                    await UserData.give_money(self.self_, interaction.user.id, (int(round(self.bet_money*2, 0))))
                elif user_total == bot_total:
                    msg = user_cards_msg + f' 유저: {user_total}' + "\n" + bot_cards_msg + f' 봇: {bot_total}' + f'\n 잃음: 0' + "\n [동점.....나, 사랑해?]"
                    embed = discord.Embed(title='블랙잭', description=msg, color=0xb0a7d3)
                    embed.set_author(name="폐이", icon_url="https://i.imgur.com/OdIiI2V.jpg")
                    await interaction.response.edit_message(embed=embed, view=None)
                    await UserData.give_money(self.self_, interaction.user.id, (int(round(self.bet_money*0.5, 0))))
                else:
                    msg = user_cards_msg + f' 유저: {user_total}' + "\n" + bot_cards_msg + f' 봇: {bot_total}' + f'\n 잃음: {self.bet_money}' + "\n [이겼어.허접.]"
                    embed = discord.Embed(title='블랙잭', description=msg, color=0xb0a7d3)
                    embed.set_author(name="폐이", icon_url="https://i.imgur.com/OdIiI2V.jpg")
                    await interaction.response.edit_message(embed=embed, view=None)
                    await UserData.give_money(self.self_, interaction.user.id, (int(round(self.bet_money*-0.5, 0))))
            else:
                msg = user_cards_msg + f' 유저: {user_total}' + "\n" + bot_cards_msg + f' 봇: {bot_total}' + f'\n 획득: {self.bet_money}' + "\n [......버스트.실수.]"
                embed = discord.Embed(title='블랙잭', description=msg, color=0xb0a7d3)
                embed.set_author(name="폐이", icon_url="https://i.imgur.com/OdIiI2V.jpg")
                await interaction.response.edit_message(embed=embed, view=None)
                await UserData.give_money(self.self_, interaction.user.id, (int(round(self.bet_money*-0.5, 0))))
                await UserData.give_money(self.self_, interaction.user.id, (int(round(self.bet_money*2, 0))))
        else:
            msg = user_cards_msg + f' 유저: {user_total}' + "\n" + bot_cards_msg + f' 봇: ...' + f'\n 잃음: {self.bet_money}' + "\n [버스트.허접.]"
            embed = discord.Embed(title='블랙잭', description=msg, color=0xb0a7d3)
            embed.set_author(name="폐이", icon_url="https://i.imgur.com/OdIiI2V.jpg")
            await interaction.response.edit_message(embed=embed, view=None)
            await UserData.give_money(self.self_, interaction.user.id, (int(round(self.bet_money*-0.5, 0))))

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
            elif self.custom_id == "doubledown":
                await BlackJackButtons.doubledown(self, interaction)
            else:
                await BlackJackButtons.stand(self, interaction)
        else:
            await interaction.response.send_message(content="[.....도둑.판결.쓰레기]", ephemeral=True)

class RcpButtons(Button):
    def __init__(self, label, emoji, custom_id, command_userid, bet_money, self_):
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
        self.self_ = self_
    
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
                result = "[운빨 망겜 안할래]"
                message = f'{self.bet_money * 2} 얻음'
                await UserData.give_money(self.self_, interaction.user.id, (int(round(self.bet_money*3, 0))))
            elif result == "draw":
                result = "[비겼으니 돈은 반만 가져감]"
                message = f'{int(round(self.bet_money * 0.5, 0))} 잃음'
                await UserData.give_money(self.self_, interaction.user.id, (int(round(self.bet_money*0.5, 0))))
            else:
                result = "[ㅋ 너 나 절대 못이김]"
                message = f'{self.bet_money} 잃음'
            if self.bet_money == 0:
                message = "[돈도 못거는 쫄보 였음?]"
            embed = discord.Embed(title=result, description=f'페이:{bot_rcp}\n나:{self.user_rcp}\n{message}', color=0xb0a7d3)
            embed.set_author(name="폐이", icon_url="https://i.imgur.com/OdIiI2V.jpg")
            await interaction.response.edit_message(content="", embed=embed, view=None)
        else:
            await interaction.response.send_message(content="[.....도둑.판결.쓰레기]", ephemeral=True)

#___________________________________________________________________________________________________________________________________________

class UserData(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.data = self.get_json()
        self.repeat_save_user.start()
        self.reset_attendence.start()
        self.self_ = self
        #UserData.self_
    @commands.Cog.listener()
    async def on_ready(self):
        print("준비됨")
        
    def get_attribute(self, user_id: str, item):
        amount =  self.data[str(user_id)]["item"][item]
        return amount

    def reduce_item(self, user_id: str, item):
        self.data[user_id]["item"][item] -=1
    
    def set_json(self):
        """_summary_
            users JSON 에 self.data를 덮어씌움.
        """
        try:
            with open(os.path.join(__location__ + '/json/users.json'), "w") as file:
                file.write(json.dump(self.data, file, indent=4))
        except TypeError:
            pass

    def get_json(self) -> dict:
        """_summary_
            users JSON 파일을 불러와서 return함
        return Dict
        """
        with open(os.path.join(f"{__location__}/json/users.json"),'r',encoding='utf-8') as file:
            return json.load(file)

    def check_user(self, user_id: str):
        """_summary_
            만약 해당 str(user.id)가 self.data에 없다면 추가함.
        Args:
            user_id (str, 필수): 해당 user의 id
        """
        if user_id not in self.data:
            self.data[user_id] = {
                    "level": {
                        "main": 1,
                        "xp": 0,
                        "rangi": 1,
                        "rangi_xp": 0,
                        "chiyee": 1,
                        "chiyee_xp": 0,
                        "saehee": 1,
                        "saehee_xp": 0,
                    },
                    "money": 30000,
                    "item": {
                        "rangi_teeth": 0, 
                        "rangi_jeogorri": 0,
                        "rangi_hanbok": 0,
                        "saehee_sotlid": 0,
                        "saehee_beenyo": 0,
                        "saehee_shotglass": 0,
                        "chiyee_hairband": 0,
                        "chiyee_gookja": 0,
                        "chiyee_julmuni" : 0,
                        "legendary_saliva" : 0
                    },
                    "attendence": False,
                    "birthday": False,
                    "birthday_character": "rangi"
                }
        else:
            pass

    def update_birthday(self, user_id: str, date:str) -> None:
        self.data[user_id]["birthday"] = date
    
    def update_birthday_character(self, user_id: str, character: str)-> None:
        self.data[user_id]["birthday_character"] = character

    def character_level_up(self, user_id: str, character: str) -> bool:
        """_summary_
            유저가 레벨업 했는지 확인함.
        Args:
            user_id (str,필수): 메세지를 보낸 해당 유저의 id
        Returns:
            _type_: 업을 했다면 true를 return함
        """
        current_xp = self.data[user_id]["level"][character+"_xp"]
        current_lvl = self.data[user_id]["level"][character]

        if current_xp >= round(((current_lvl+1)/0.3)**2)+40:
            self.data[user_id]["level"][character] += 1
            self.data[user_id]["level"][character+"_xp"] = 0
            return True

        return False
    # async def apply_xp(self, user_id, xp: int)
    
    async def character_give_xp(self, user_name, user_id, channel, xp: int, character: str):
        """_summary_
            매세지를 보낸 유저에게 xp를 1~2사이로 랜덤 부여. 레벨업을 했는지 확인하여 True를 받으면 self.data레벨을 올림
        Args:
            ctx (_type_): 메세지 Context
        """
        user_id = str(user_id)
        
        self.data[user_id]["level"][character+"_xp"] += xp
        if self.character_level_up(user_id, character):
            
            rangi_congrats = [f"{user_name}(야)아! 이런 선물은 어디에서 가지고 오는 것이냐? 역시 나를 너무 잘 아는것이니라~",
                              "흐냐아아! 선물을 엄청 받았느니라! 역시 우리 낭군님 밖에 없느니라~",
                              "ㅇ...이렇게 많은 선물을 받아도 되는지 모르겠느니라! 나도 뭔가를 주고 싶느니라!!!"]
            chiyee_congrats = [f"꺄우우우!!! 선물을 너무 많이 받은 거예요!! {user_name} 오라버니 밖에 없는 거예요!!",
                               f"(파닥파닥파닥) ㅇ.. 이게 다 {user_name} 오라버니에게 받은 선물인 거예요!!!",
                               f"아우우!! {user_name} 오라버니가 최고인 거예요!! 그런 거예요!!"]
            saehee_congrats = ["저에게 주신 모든 선물은 환불이 불가능 합니다.",
                               f"{user_name} 도련님 께서는 돈이 남아 도시는지요?",
                               "뭐 바라는 거라도 있습니까? 슬슬 말하실 때도 되셨습니다."]
            if character == "rangi":
                embed=discord.Embed(title=f"{random.choice(rangi_congrats)}", description=f"호감도 {self.data[user_id]['level'][character]} 달성!", color=0x7a90e1)
                embed.set_author(name="랑이", icon_url="https://i.imgur.com/huDPd5o.jpg")
            elif character == "chiyee":
                embed=discord.Embed(title=f"{random.choice(chiyee_congrats)}", description=f"호감도 {self.data[user_id]['level'][character]} 달성!", color=0x7a90e1)
                embed.set_author(name="치이", icon_url="https://i.imgur.com/aApUYMj.jpg")
            elif character == "saehee":
                embed=discord.Embed(title=f"{random.choice(saehee_congrats)}", description=f"호감도 {self.data[user_id]['level'][character]} 달성!", color=0x7a90e1)
                embed.set_author(name="세희", icon_url="https://i.imgur.com/7a4oeOi.jpg")
            
            await channel.send(embed=embed, delete_after=10) 

    def level_up(self, user_id: str) -> bool:
        """_summary_
            유저가 레벨업 했는지 확인함.
        Args:
            user_id (str,필수): 메세지를 보낸 해당 유저의 id
        Returns:
            _type_: 레벨업을 했다면 true를 return함
        """
        current_xp = self.data[user_id]["level"]["xp"]
        current_lvl = self.data[user_id]["level"]["main"]

        if current_xp >= round((4 * (current_lvl ** 3)) / 5):
            return True
        return False
    
    async def give_xp(self,message):
        """_summary_
            매세지를 보낸 유저에게 xp를 1~2사이로 랜덤 부여. 레벨업을 했는지 확인하여 True를 받으면 self.data레벨을 올림
        Args:
            ctx (_type_): 메세지 Context
        """
        user_name = message.author.name
        user_id = str(message.author.id)
        channel = message.channel

        embed=discord.Embed(title="아우우! {}(으)로 레벨 업 하신거예요!!", description="{}")
        embed.set_author(name="치이", icon_url="https://i.imgur.com/m4rkhda.jpg")

        self.check_user(str(user_id))
        random_xp = random.randint(1, 2)
        self.data[user_id]["level"]["xp"] += random_xp
        if self.level_up(user_id):
            self.data[user_id]["level"]["main"] += 1
            congrats = [f"축하드리는거예요 {user_name} 오라버니!!",
                        f"{user_name} 오라버니 고생이 많으신거예요!",
                        f"아우우!! 벌써 {self.data[user_id]['level']['main']}레벨인 거에요 오라버니!",
                        f"아우? 엄청 빠르신거예요! 축하드려요 {user_name} 오라버니!",
                        f"아우우우! {self.data[user_id]['level']['main']}레벨 달성은 축하드리지만.. 오라버니도 현생을 사셔야 하는 거예요... ",
                        f"랑이님! 아무리 그래도 이런 축하는 제가 하고 싶은 거예요! 아우우우!!!\n헤헤 {user_name}(야)아! {self.data[user_id]['level']['main']}레벨 축하하느니라!!"
                        ]
            embed=discord.Embed(title=f"아우우! {self.data[user_id]['level']['main']}(으)로 레벨 업 하신거예요!!", description=f"{random.choice(congrats)}", color=0x7a90e1)
            embed.set_author(name="치이", icon_url="https://i.imgur.com/m4rkhda.jpg")
            
            await channel.send(embed=embed, reference=message, delete_after=10)  

    @app_commands.command(name="지갑", description="현재 돈 보유량을 확인합니다")
    async def check_money(self, interaction: discord.Interaction):
        self.check_user(str(interaction.user.id))
        money = self.data[str(interaction.user.id)]['money']
        money = format(money, ',d')
        embed=discord.Embed(title="지갑", description=f"{money}원", color=0xafc2f3)
        await interaction.response.send_message(embed=embed)

    async def give_money(self, user_id, money: int):
        """_summary_
            user 돈 지급용 function
        Args:
            user_id (_type_, 필수): 지급 대상 user.id
            money (int, 필수): 지급할 돈 액수
        """
        self.check_user(str(user_id))
        self.data[str(user_id)]["money"] += money   

    @commands.command(name=";지급", pass_context=True)
    async def take_money(self, ctx, user, money: int):
        """_summary_
            user가 전체가 아니라면 해당 user.id에게 돈 징수. 전체라면 self.data에 있는 모든 유저에게 돈 징수.
            *개발자 전용
        Args:
            ctx (_type_): 메세지 Context
            user (_type_, 옵션): user.id 혹은 "전체"
            money (int, 옵션): 징수할 돈 액수
        """
        if str(ctx.author.id) in list_dev_id:
            if user == "전체":
                for user_id in self.data.items():
                    self.data[user_id[0]]["money"] += money
            else:  
                self.check_user(str(ctx.author.id))
                self.data[str(user)]["money"] += money
        else:
            pass

    @commands.command(name="핑")
    async def ping(self, ctx):
        """_summary_
            테스트용 핑퐁
        Args:
            ctx (_type_): 메세지 Context
        """
        await ctx.send("퐁이니라!")

    @app_commands.command(name="인벤토리", description="인벤토리를 불러옵니다")
    async def inventory(self, interaction: discord.Interaction):
        self.check_user(str(interaction.user.id))
        user_data = self.data[str(interaction.user.id)]
        item_info = "".join([f"{key}: {value}\n" for key, value in user_data["item"].items()])
        embed = discord.Embed(title=f"{interaction.user.name}의 인벤토리", color=0x0aa40f)
        embed.set_author(name="치이", icon_url="https://i.imgur.com/7a4oeOi.jpg")
        embed.add_field(name="아이템 보유량", value=item_info)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="출석", description="출석체크")
    async def attendence(self, interaction: discord.Interaction):
        self.check_user(str(interaction.user.id))
        attendence_bool = self.data[str(interaction.user.id)]["attendence"]

        if attendence_bool == False:
            self.data[str(interaction.user.id)]["money"] += 10000
            self.data[str(interaction.user.id)]["attendence"] = True

            embed_attendence = discord.Embed(title= "출석체크 완료인 거예요!", description="만원 드린 거예요! 가챠에 다 쓰시면 안되는 거예요!!",color=0x0aa40f)
            embed_attendence.set_author(name="치이", icon_url="https://i.imgur.com/aApUYMj.jpg")
            embed_attendence.add_field(name="돈 보유량", value=f"{self.data[str(interaction.user.id)]['money']}원")
            
            await interaction.response.send_message(embed=embed_attendence)
        else:
            embed_reject = discord.Embed(title=f"아우우!! 욕심이 많으신 거예요!", description="이미 드린 거예요! 또 드릴 수는 없는 거예요!",color=0x0aa40f)
            embed_reject.set_author(name="치이", icon_url="https://i.imgur.com/aApUYMj.jpg")
            embed_reject.add_field(name="돈 보유량", value=f"{self.data[str(interaction.user.id)]['money']}원")

            await interaction.response.send_message(embed=embed_reject)

    @tasks.loop(time= rest_time)
    async def reset_attendence(self):
        for user_id in self.data.items():
            self.data[user_id[0]]["attendence"] = False

    # @tasks.loop(time= birthday_time)
    # async def check_birthday(self):
    #     time = datetime.datetime.now()
    #     month_day = f"{time.month}/{time.day}"
    #     for user_id in self.data.items():
    #         if self.data[user_id[0]]["birthday"] == month_day:
    #             user = discord.utils.get(self.bot.guilds.members, id= user_id[0])
    #             if user:
    #                 embed 보내기 https://i.imgur.com/wZMgKhQ.png
    #                 user.send(embed)

    @app_commands.command(name="생일캐릭터", description="캐릭터변경")
    async def birthday_character(self, interaction: discord.Interaction):
        self.check_user(str(interaction.user.id))


    @app_commands.command(name="생일", description="생일설정 *변경 불가 /생일 월 일")
    async def birthday(self, interaction: discord.Interaction, month: int, date: int):
        self.check_user(str(interaction.user.id))
        birthday_data = self.data[str(interaction.user.id)]["birthday"]
        birth_date = f"{month}/{date}"
        date_time_obj = datetime.datetime.strptime(birth_date, '%m/%d')
        birth_date = f"{date_time_obj.month}/{date_time_obj.day}"
        if birthday_data == False:
            view = ConfirmGui(self, str(interaction.user.id), birth_date)
            embed_birthday = discord.Embed(title= f"생일을 {date_time_obj.month}월 {date_time_obj.day}일로 설정 하실건가요!", description="다시는 바꾸실 수 없는거예요! 아시겠나요!",color=0x0aa40f)
            embed_birthday.set_author(name="치이", icon_url="https://i.imgur.com/aApUYMj.jpg")
            await interaction.response.send_message(view=view, embed=embed_birthday)

        else:
            embed_reject = discord.Embed(title=f"이미 생일을 설정 하신 거예요!!", description="생일은 바꾸실 수 없는 거예요!!",color=0x0aa40f)
            embed_reject.set_author(name="치이", icon_url="https://i.imgur.com/aApUYMj.jpg")

            await interaction.response.send_message(embed=embed_reject)

    @app_commands.command(name="정보", description="유저 정보를 불러옵니다")
    async def user_information(self, interaction: discord.Interaction):
        self.check_user(str(interaction.user.id))
        with open('users.json') as f:
            data = json.load(f)

        if str(interaction.user.id) not in self.data:
            await interaction.response.send_message("등록되지 않은 유저입니다.")
            return
        user_data = self.data[str(interaction.user.id)]
        level_data = user_data['level']
        embed = discord.Embed(title=f"{interaction.user.name}의 프로필",description=f"Lv. {level_data['main']} \nExp: {level_data['xp']}/5000", color=0x0aa40f)
        embed.set_author(name="치이", icon_url="https://i.imgur.com/7a4oeOi.jpg")
        embed.add_field(name="호감도 레벨", value=f"랑이:{level_data['rangi']}\n 치이:{level_data['chiyee']}\n세희:{level_data['saehee']}", inline=False)
        await interaction.response.send_message(embed=embed)

    @commands.Cog.listener()
    async def on_disconnect(self):
        self.set_json()

    @tasks.loop(seconds=30)
    async def repeat_save_user(self):
        self.set_json()
        self.get_json()

############################################ 대화 기능 ###############################################
    @commands.Cog.listener()
    async def on_message(self, message):
        contents = message.content.split(" ")
        if message.author.bot: 
            return None
        if any(x in message.content for x in all_hi) and "랑이야" in message.content:
            rangi_hi = [f"헤헤 안녕 하느냐! {message.author.name}(야)아!",
            f"{message.author.name}(야)아! 안녕하느냐!",
            "반갑느니라!!",
            f"흐냐앗! 왔느냐 {message.author.name}(야)아!",
            "돌아왔구나! 보고싶었느니라!",
            "너가 없는 동안.. 나는 심심했느니라...ㅠㅠ",
            "헤헤 왔으니 이제 놀아주는 것이느냐!",
            "오늘 하루는 어떠하였느냐!? 평화롭지 않느냐! 헤헤",
            f"{message.author.name}(이)가 왔으니 같이 놀아주거라아아!! 놀아주거라!!!! 심심하니라!!",
            "너의 하루는 어땠느냐? 나는 낭군님만 기다리고 있었느니라!",
            f"흐냐아앗!! 내가 얼마나 기다렸는지 알고있느냐!! 하루종일 {message.author.name}(이)만 기다렸느니라!",
            "사랑 하나 주면 안 잡아 먹느니라-♡ 헤헤"
            ]
            embed=discord.Embed(title=f"{random.choice(rangi_hi)}", color=0xebe6e6)
            embed.set_author(name="랑이", icon_url="https://i.imgur.com/huDPd5o.jpg")
            await message.channel.send(embed=embed)
            await self.give_xp(message)
        elif any(x in message.content for x in all_hi) and "치이야" in message.content:
            chiyee_hi = ["안녕한거예요!!!",
            "꺄우우?! 오신거예요?!",
            "아우우! 반가운거예요!",
            "오라버니!! 아우우우!! 보고싶었던 거예요! 꺄우우..",
            "필요한거 있으시면 말씀하시는 거예요!",
            f"아우우! 저는 잘지내고 있는거예요! {message.author.name} 오라버니는 잘 지내고 계신가요?",
            f"부르신 건가요! {message.author.name} 오라버니!",
            f"아우우! {message.author.name} 오라버니가 인사 해준거예요! 그런거예요!"
            ]
            embed=discord.Embed(title=f"{random.choice(chiyee_hi)}", color=0x4b84ce)
            embed.set_author(name="치이", icon_url="https://i.imgur.com/aApUYMj.jpg")
            await message.channel.send(embed=embed)
            await self.give_xp(message)
        elif any(x in message.content for x in all_hi) and "세희야" in message.content:
            saehee_hi = ["같이 한잔 하시겠습니까?",
            "인사는 생략 하시지요",
            "안녕 하십니까 로리ㅋ... 크흠 아닙니다",
            f"오셨습니까 {message.author.name} 도련님",
            "인사할 시간 없습니다 ",
            "왠일로 저한테 인사 하신겁니까?",
            f"저 말고 랑이 님이나 찾으시지요...",
            f"{message.author.name} 도련님이 저에게 인사를 다 하시고 세상 참 좋아졌군요"
            ]
            embed=discord.Embed(title=f"{random.choice(saehee_hi)}", color=0x666666)
            embed.set_author(name="세희", icon_url="https://i.imgur.com/7a4oeOi.jpg")
            await message.channel.send(embed=embed)
            await self.give_xp(message)
            
        elif any(x in message.content for x in all_what) and "랑이야" in message.content:
            rangi_what =[
            f"헤헤, {message.author.name}(이)가 오기를 기다리고 있었느니라!! 잘했느냐? 그럼 쓰다듬어 주거라!",
            "냥이랑 놀고 있었느니라!!",
            "심심하느니라... 같이 놀아주거라!!",
            "으냐아아!! 도와주거라!!! 공부하기 싫느니라! 나래가 쫓아오느니라!!!",
            "바둑이 놀아주고 있었느니라!",
            "흐냐앙.. 낮잠 자고 있었느니라.."
        ]
            embed=discord.Embed(title=f"{random.choice(rangi_what)}", color=0xebe6e6)
            embed.set_author(name="랑이", icon_url="https://i.imgur.com/huDPd5o.jpg")
            await message.channel.send(embed=embed)
            await self.give_xp(message)
            
        elif any(x in message.content for x in all_what) and "치이야" in message.content:
            chiyee_what = [
            "아우우우....언제오는지 기다리ㄱ.. ㅇ.아니 그냥 있었던거에요! 그런 거예요!",
            f"심심한거에요 {message.author.name} 오라버니랑 같이 놀고싶....?!? 언제 오신 거예요!?",
            "폐이 놀아주고 있는 거에요!! 같이 노실건가요?",
            "집 정리 한거예요! 힘든거예요!",
            "밥 준비 하는거예요!! 기다리시면 불러 드릴 거예요!",
            "아우우!! 계속 기다리고 있었던 거예요!"
        ]
            
            embed=discord.Embed(title=f"{random.choice(chiyee_what)}", color=0x4b84ce)
            embed.set_author(name="치이", icon_url="https://i.imgur.com/aApUYMj.jpg")
            await message.channel.send(embed=embed)
            await self.give_xp(message)
            
        elif any(x in message.content for x in all_what) and "세희야" in message.content:
            saehee_what = [
            "안주인님이랑 놀고 있습니다",
            "같이 한잔 하실겁니까..",
            "주인님 뒷처리 중입니다...",
            "레이드 뛸때는 바둑이도 안건듭니다",
            "나와호랑이님을 쓰ㄱ... 실례 세계관이 망가질뻔했군요",
            "안주인님 덕질합니다",
            "꼭 알려드려야 합니까?",
            "제가 꼭 알려드려야 됩니까",
            "눈은 장식이십니까?"
        ]
            embed=discord.Embed(title=f"{random.choice(saehee_what)}", color=0x666666)
            embed.set_author(name="세희", icon_url="https://i.imgur.com/7a4oeOi.jpg")
            await message.channel.send(embed=embed)
            await self.give_xp(message)

    @commands.command(name="랑이야")
    async def rangi_call(self, ctx, position = None):
        rangi = [
            '으냐앗! 왜 부르느냐?',
            '으에!?...갑자기 왜 그러느냐?.',
            '내가 보고 싶었느냐?',
            '놀아주는 것이느냐!! ',
            '내가 보고 싶었느냐?',
            'ㄴ..내가 필요한 것이냐!',
            '나는 사랑 받고 싶느니라~!',
            '흐에에에?! 불렀느냐?!',
            '으냣!? 내가 도와줄게 있느냐?!',
            '여기있느니라!',
            '네 곁에 항상 있느니라!',
            '언제든 말만 하거라! 내가 다~ 들어주겠느니라!!',
            '나는 네 곁에 있느니라! 말만 하거라!',
            '웅? 불렀느냐?',
        ]
        if position == None:
            embed=discord.Embed(title=f"{random.choice(rangi)}", color=0xebe6e6)
            embed.set_author(name="랑이", icon_url="https://i.imgur.com/huDPd5o.jpg")
            await self.give_xp(ctx)
            await ctx.send(embed=embed)
        else:
            pass

    @commands.command(name="범이야")
    async def rangi_realname(self, ctx):
        rangi = [
            "으냐아아앗!!",
            "문제가 생긴 것이냐!!!",
            "무슨 일 이느냐!!!",
            "낭군님아!! 불렀느냐!!",
            "헤..헤헤 바로 옆에 있느니라!",
        ]
        embed=discord.Embed(title=f"{random.choice(rangi)}", color=0xebe6e6)
        embed.set_author(name="범이", icon_url="https://i.imgur.com/huDPd5o.jpg")
        await self.give_xp(ctx)
        await ctx.send(embed=embed)

    @commands.command(name="치이야")
    async def chiyee_call(self, ctx, position = None):
        chiyee = [
            '꺄우우? 왜 부르시는 건가요?',
            '드디어 절 불러주신 거예요!',
            '무슨 일 있는거예요!?!',
            '도움이 필요한 건가요?',
            '아우우? 무슨일인 건가요!?',
            '저는 항상 오라버니 옆에 있는거예요',
            '놀아 주시는 건가요?',
            '폐이 놀아줘야 되는거예요!',
            '어디 안가고 잘 지내는 거예요!',
            '필요하신게 있으면 말씀 하시는거예요!',
            '그 짧은 시간에 제가 보고싶었던 건가요?',
        ]
        if position == None:
            embed=discord.Embed(title=f"{random.choice(chiyee)}", color=0x4b84ce)
            embed.set_author(name="치이", icon_url="https://i.imgur.com/aApUYMj.jpg")
            await self.give_xp(ctx)
            await ctx.send(embed=embed)  
        else:
            pass

    @commands.command(name="연리야")
    async def chiyee_realname(self, ctx):
        chiyee = [
            "꺄우우우우우?!!",
            "오라버니! 너무 막 부르시는 거예요!!",
            "진명이 있는건 좋은거예요!!",
            "꺄우?! 갑자기 무슨 일이 신가요!",
            "ㅊ...창피하게 막 부르시면 안되는거예요!!",
        ]
        embed=discord.Embed(title=f"{random.choice(chiyee)}", color=0x4b84ce)
        embed.set_author(name="연리", icon_url="https://i.imgur.com/aApUYMj.jpg")
        await self.give_xp(ctx)
        await ctx.send(embed=embed)
        
    @commands.command(name="세희야")
    async def saehee_call(self, ctx, position = None):
        saehee = [  
            '예 주인님',
            '부르셨습니까?',
            '말씀하시면 됩니다',
            '문제라도 있으십니까?',
            '또 제가 필요한겁니까?',
            '또 뭡니까?',
            '썪ㅇ... 크흠 아닙니다 뭐.... 필요한게 있으십니까?',
            '안주인님이랑 놀아주시죠',
            '크게 안부르셔도 들립니다',
            '계속 듣고 있습니다',
        ]
        if position == None:
            embed=discord.Embed(title=f"{random.choice(saehee)}", color=0x666666)
            embed.set_author(name="강세희", icon_url="https://i.imgur.com/7a4oeOi.jpg")
            await self.give_xp(ctx)
            await ctx.send(embed=embed)
        else:
            pass
            
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        pass
###################################### 가챠/호감도 ##################################################
    @commands.command(name="핑")
    async def ping(self, ctx):
        """_summary_
            테스트용 핑퐁
        Args:
            ctx (_type_): 메세지 Context
        """
        await ctx.send("퐁이니라!")

    @app_commands.command(name="가챠", description="호감도템 가챠")
    async def gacha(self, interaction: discord.Interaction):
        self.check_user(str(interaction.user.id))
        pos = {"Common": 40, "Rare": 45, "Epic": 13, "Legendary": 2}
        item_list = {
            "개량한복": {
                "name" :  "rangi_hanbok",
                "rarity": "Common",
                "image": "https://i.imgur.com/NHBALeB.png",
            },
            "술잔": {
                "name" :  "saehee_shotglass",   
                "rarity": "Common",
                "image": "https://i.imgur.com/NHBALeB.png",
            },
            "국자": {
                "name" :  "chiyee_gookja",
                "rarity": "Common",
                "image": "https://i.imgur.com/NHBALeB.png",
            },
            "저고리": {
                "name" :  "rangi_jeogorri",
                "rarity": "Rare",
                "image": "https://i.imgur.com/NHBALeB.png",
            },
            "깃털 머리띠": {
                "name" :  "chiyee_hairband",
                "rarity": "Rare",
                "image": "https://i.imgur.com/NHBALeB.png",
            },
            "솥뚜껑": {
                "name" :  "saehee_sotlid",
                "rarity": "Rare",
                "image": "https://i.imgur.com/NHBALeB.png",
            },
            "이빨": {
                "name" :  "rangi_teeth",
                "rarity": "Epic",
                "image": "https://i.imgur.com/NHBALeB.png",
            },
            "비녀": {
                "name" :  "saehee_beenyo",
                "rarity": "Epic",
                "image": "https://i.imgur.com/NHBALeB.png",
            },
            "줄무늬 그것": {
                "name" :  "chiyee_julmuni",
                "rarity": "Epic",
                "image" : "https://i.imgur.com/NHBALeB.png",
            },
            "대요괴의 침": { #침
                "name" :  "legendary_saliva",
                "rarity": "Legendary", 
                "image" : "https://i.imgur.com/NHBALeB.png", 
            }
        }
        rarity = random.choices(list(pos.keys()), weights=list(pos.values()), k=1)[0]
        item = random.choice([k for k, v in item_list.items() if v["rarity"] == rarity])

        if rarity == "Legendary":
            emcolor=0xe67e22
        elif rarity == "Epic":
            emcolor=0x71368a
        elif rarity == "Rare":
            emcolor=0x3498db
        else:
            emcolor=0x2ecc71

        cost = 30000
        if self.data[str(interaction.user.id)]['money'] >= cost:
            self.data[str(interaction.user.id)]['money'] -= cost

            item_pic = item_list[item]["image"]
            self.data[str(interaction.user.id)]["item"][item_list[item]["name"]] += 1
            
            embed = discord.Embed(
                title="가챠 결과",
                description=f"{rarity} \n {item}",
                color=emcolor,
            )

            embed.set_image(url=item_pic)
            embed.set_footer(text=f"총 보유량:{self.data[str(interaction.user.id)]['item'][item_list[item]['name']]}")
            await interaction.response.send_message(embed=embed)
        else:
            embed=discord.Embed(title="돈이 부족합니다", description="돈 좀 벌고 오시죠")
            await interaction.response.send_message(embed=embed)

        
    @app_commands.command(name="선물", description= "선택한 아해에게 선물")
    async def give_gift(self, interaction: discord.Interaction):
        self.check_user(str(interaction.user.id))
        view = ChoseGUI(self, str(interaction.user.id))
        embed=discord.Embed(title="선물 보유량", color=0xd4e9c4)
        for item in self.data[str(interaction.user.id)]["item"]:
            item_kor = item_list_convert[item]
            amount = self.data[str(interaction.user.id)]["item"][item]
            embed.add_field(name=item_kor, value=amount)
        await interaction.response.send_message(view=view, embed=embed)

    """
    @app_commands.command(name="랜덤",description="랜덤으로 유저를 뽑습니다")
    async def random_pick(self, interaction: discord.Interaction, channel_id: str ,message_id: str):
        channel_obj = await interaction.guild.fetch_channel(int(channel_id))
        message_obj = await channel_obj.fetch_message((int(message_id)))
        message_reaction = message_obj.reactions
        print(message_reaction)
        users = []
        async for user in message_reaction.users():
            users.append(user)
        print(users)
        won = random.sample(users, 5)
        await interaction.response.send_message(won)
        print(won)"""

##################################### 미니게임 #################################################### UserData.give_money(self, user_id, money)
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
        self.check_user(str(interaction.user.id))
        owned_money = self.data[str(interaction.user.id)]["money"]
        if bet_money < 0:
            await interaction.response.send_message(content="[너 거지. 정.직.하.게. 돈 벌어와]", ephemeral=True)
            pass
        elif bet_money <= owned_money:
            await UserData.give_money(self, interaction.user.id, (bet_money * -1))
            var1 = random.randint(1,9)
            var2 = random.randint(1,9)
            var3 = random.randint(1,9)
            var_list = ([11,11,11],[var1,11,11],[var1,var2,11],[var1,var2,var3])
            for i in var_list:
                embed = await UserData.embed_create_slotmachine(i, "결과: ...", interaction)
                await asyncio.sleep(1)
            if var1 == 1 and var2 == 1 and var3 == 1:
                result = "[잭팟 ㅊㅊ]"
                result += f'\n획득: {int(round(bet_money*100, 0))}'
                await UserData.give_money(self, interaction.user.id, (int(round(bet_money*101, 0))))
            elif var1 == var2 and var2 == var3:
                result = "[트리플. 좀 치네]"
                result += f'\n획득: {int(round(bet_money*5, 0))}'
                await UserData.give_money(self, interaction.user.id, (int(round(bet_money*6, 0))))
            elif var1 == var2 or var1 == var3 or var2 == var3:
                result = "[페어네 나랑 치이 처럼]"
                result += f'\n획득: {int(round(bet_money*1.5, 0))}'
                await UserData.give_money(self, interaction.user.id, (int(round(bet_money*2.5, 0))))
            else:
                result = "[꽝... 허접 ㅋ]"
                result += f'\n잃음: {bet_money}'
            embed = await UserData.embed_create_slotmachine(var_list[3], result, interaction)
        else:
            await interaction.response.send_message(content="[돈 부족. 판결. 사기꾼]", ephemeral=True)

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
        self.check_user(str(interaction.user.id))
        owned_money = self.data[str(interaction.user.id)]["money"]
        if bet_money < 0:
            await interaction.response.send_message(content="[너 거지.  정.직.하.게. 돈 벌어와]", ephemeral=True)
            pass
        elif bet_money <= owned_money:
            await UserData.give_money(self, interaction.user.id, (bet_money * -1))
            cards = ['s2', 's3', 's4', 's5', 's6', 's7', 's8', 's9', 'sJ', 'sK', 'sQ', 'sA', 
            'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'hJ', 'hK', 'hQ', 'hA', 
            'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8', 'd9', 'dJ', 'dK', 'dQ', 'dA', 
            'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'cJ', 'cK', 'cQ', 'cA']

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
                    msg += f'\n [블랙잭...허접 ㅋ]'
                    embed = discord.Embed(title='블랙잭', description=msg, color=0xb0a7d3)
                    embed.set_author(name="폐이", icon_url="https://i.imgur.com/OdIiI2V.jpg")
                    await interaction.response.send_message(embed=embed)
                else:
                    view = View()
                    view.add_item(BlackJackButtons('히트', discord.ButtonStyle.green, "🃏", "hit", interaction.user.id, bet_money, user_deck, bot_deck, cards, self))
                    view.add_item(BlackJackButtons('스탠드', discord.ButtonStyle.red, "🖐🏻", "stand", interaction.user.id, bet_money, user_deck, bot_deck, cards, self))
                    if owned_money >= bet_money * 2:
                        view.add_item(BlackJackButtons('더블다운', discord.ButtonStyle.grey, "💰", "doubledown", interaction.user.id, bet_money, user_deck, bot_deck, cards, self))
                    embed = discord.Embed(title='블랙잭', description=msg, color=0xb0a7d3)
                    embed.set_author(name="폐이", icon_url="https://i.imgur.com/OdIiI2V.jpg")
                    await interaction.response.send_message(embed=embed, view=view)
            else:
                if bot_total != 21:
                    msg += f'\n [블랙잭 ㅊㅊ]\n획득: {int(round(bet_money*1.5, 0))}'
                    embed = discord.Embed(title='블랙잭', description=msg, color=0xb0a7d3)
                    embed.set_author(name="폐이", icon_url="https://i.imgur.com/OdIiI2V.jpg")
                    await interaction.response.send_message(embed=embed)
                    await UserData.give_money(self, interaction.user.id, (int(round(bet_money*2.5, 0))))
                else:
                    msg += f'\n [블랙잭..둘다?]\n잃음: {bet_money}'
                    embed = discord.Embed(title='블랙잭', description=msg, color=0xb0a7d3)
                    embed.set_author(name="폐이", icon_url="https://i.imgur.com/OdIiI2V.jpg")
                    await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(content="[돈 부족. 판결. 사기꾼]", ephemeral=True)

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
        self.check_user(str(interaction.user.id))
        owned_money = self.data[str(interaction.user.id)]["money"]
        if bet_money < 0:
            await interaction.response.send_message(content="[너 거지.  정.직.하.게. 돈 벌어와]", ephemeral=True)
            pass
        elif bet_money <= owned_money:
            await UserData.give_money(self, interaction.user.id, (bet_money * -1))
            view = View()
            view.add_item(RcpButtons('가위', "✌️", "scissors", interaction.user.id, bet_money, self))
            view.add_item(RcpButtons('바위', "✊", "rock", interaction.user.id, bet_money, self))
            view.add_item(RcpButtons('보', "✋", "paper", interaction.user.id, bet_money, self))
            embed = discord.Embed(title='[넌 나 못이김]')
            await interaction.response.send_message(embed=embed, view=view)
        else:
            await interaction.response.send_message(content="[돈 부족. 판결. 사기꾼]", ephemeral=True)

async def setup(bot):
    await bot.add_cog(UserData(bot))
    
