import discord
from discord import app_commands
from discord.ext import commands, tasks
import pymongo
import json
import os
import random
import datetime
from time import gmtime, strftime
list_dev_id = ["339767912841871360", "474389454262370314", "393932860597338123", "185181025104560128"]
all_hi = ["안녀", "안녕", "안뇽", "안뇨", "어서와", "히사시부리", "하이", "반가워", "오랜만이야", "나 또 왔", 
        "좋은 아침", "잘 잤어", "좋은 밤", "좋은 저녁", "좋은 점심", "여기야", "반갑다", 
        "돌아왔", "나 왔어", "나 왔", "갔다 왔어", "다녀왔"]
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
utc = datetime.timezone.utc
rest_time = datetime.time(hour=19, minute=00, tzinfo=utc) #19 00 오전 4시 utf + 9 대한민국
print(rest_time)
class UserData(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.data = self.get_json()
        print(self.data)
        self.repeat_save_user.start()
        self.reset_attendence.start()
    @commands.Cog.listener()
    async def on_ready(self):
        print("준비됨")

    def set_json(self):
        """_summary_
            users JSON 에 self.data를 덮어씌움.
        """
        try:
            with open(os.path.join(__location__ + '\\json\\users.json'), "w") as file:
                file.write(json.dump(self.data, file, indent=4))
        except TypeError:
            pass

    def get_json(self) -> dict:
        """_summary_
            users JSON 파일을 불러와서 return함
        return Dict
        """
        with open(os.path.join(f"{__location__}\\json\\users.json"),'r',encoding='utf-8') as file:
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
                        "rangi": 0,
                        "rangi_xp": 0,
                        "cheeyi": 0,
                        "cheeyi_xp": 0,
                        "saehee": 0,
                        "saehee_xp": 0,
                    },
                    "money": 30000,
                    "item": {
                        "rangi_teeth": 0, 
                        "rangi_jeogorri": 0,
                        "rangi_habok": 0,
                        "saehee_sotlid": 0,
                        "saehee_beenyo": 0,
                        "saehee_shotglass": 0,
                        "chiyee_hairband": 0,
                        "chiyee_gookja": 0,
                        "chiyee_julmuni" : 0,
                        "legendary_saliva" : 0
                    },
                    "attendence": False
                }
        else:
            pass

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

        self.check_user(user_id)
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

    async def levelup_interaction(self, interaction: discord.Interaction, message):
        await interaction.response.send_message("인터렉션")

    @commands.command(name=";지급", pass_context=True)
    async def give_money(self, ctx, user, money: int):
        """_summary_
            user가 전체가 아니라면 해당 user.id에게 돈 지급. 전체라면 self.data에 있는 모든 유저에게 돈 지급.
            *개발자 전용
        Args:
            ctx (_type_): 메세지 Context
            user (_type_, 옵션): user.id 혹은 "전체"
            money (int, 옵션): 지급할 돈 액수
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
        
    @commands.command(name=";징수", pass_context=True)
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
                    self.data[user_id[0]]["money"] -= money
            else:  
                self.check_user(str(ctx.author.id))
                self.data[str(user)]["money"] -= money
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

    @commands.command(name="아", pass_context=True)
    async def test(self, ctx):
        """_summary_
        레벨기능 테스트 ***임시***
        Args:
            ctx (_type_): 메세지 Context
        """
        await self.give_xp(ctx.author.name , str(ctx.author.id), ctx.channel)

    @commands.command(name="인벤", pass_context=True)
    async def inven(self, ctx):
        self.check_user()
        user_data=self.data[str(ctx.author.id)]
        await ctx.send(f"{user_data}")

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

            embed_attendence = discord.Embed(title=f"출석체크 완료인 거예요!", description="만원 드린 거예요! 가챠에 다 쓰시면 안되는 거예요!!",color=0x0aa40f)
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
        embed.add_field(name="호감도 레벨", value=f"랑이:{level_data['rangi']}\n 치이:{level_data['cheeyi']}\n세희:{level_data['saehee']}", inline=False)
        await interaction.response.send_message(embed=embed)

    @commands.Cog.listener()
    async def on_disconnect(self):
        self.set_json()

    @tasks.loop(seconds=5)
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
            cheeyi_hi = [f"헤헤 안녕 하느냐! {message.author.name}(야)아!",
            "안녕한거예요!!!",
            "꺄우우?! 오신거예요?!",
            "아우우! 반가운거예요!",
            "오라버니!! 아우우우!! 보고싶었던 거예요! 꺄우우..",
            "필요한거 있으시면 말씀하시는 거예요!",
            f"아우우! 저는 잘지내고 있는거예요! {message.author.name} 오라버니는 잘 지내고 계신가요?",
            f"부르신 건가요! {message.author.name} 오라버니!",
            f"아우우! {message.author.name} 오라버니가 인사 해준거예요! 그런거예요!"
            ]
            embed=discord.Embed(title=f"{random.choice(cheeyi_hi)}", color=0x4b84ce)
            embed.set_author(name="치이", icon_url="https://i.imgur.com/aApUYMj.jpg")
            await message.channel.send(embed=embed)
            await self.give_xp(message)
        elif any(x in message.content for x in all_hi) and "세희야" in message.content:
            cheeyi_hi = ["같이 한잔 하시겠습니까?",
            "인사는 생략 하시지요",
            "안녕 하십니까 로리ㅋ... 크흠 아닙니다",
            f"오셨습니까 {message.author.name} 도련님",
            "인사할 시간 없습니다 ",
            "왠일로 저한테 인사 하신겁니까?",
            f"저 말고 랑이 님이나 찾으시지요...",
            f"{message.author.name} 도련님이 저에게 인사를 다 하시고 세상 참 좋아졌군요"
            
            ]
            embed=discord.Embed(title=f"{random.choice(cheeyi_hi)}", color=0x666666)
            embed.set_author(name="세희", icon_url="https://i.imgur.com/7a4oeOi.jpg")
            await message.channel.send(embed=embed)
            await self.give_xp(message)
            
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
        pos = {"Common": 40, "Rare": 45, "Epic": 13, "Legendary": 2}
        item_list = {
            "개량한복": {
                "name" :  "rangi_habok",
                "rarity": "Common",
                "image": "https://i.imgur.com/NHBALeB.png",
            },
            "술 잔": {
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
            "알 수 없는 용액": { #침
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
        
    @app_commands.command(name="선물", description= "선택한 아해에게 선물")
    async def give_gift(self, interaction: discord.Interaction):
        pass

##################################### 미니게임 ####################################################
async def setup(bot):
    await bot.add_cog(UserData(bot))
    
