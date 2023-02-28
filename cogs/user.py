import discord
from discord import app_commands
from discord.ext import commands, tasks
import pymongo
import json
import os
import random
list_dev_id = ["339767912841871360", "474389454262370314", "393932860597338123", "185181025104560128"]
all_hi = ["안녀", "안녕", "안뇽", "안뇨", "어서와", "히사시부리", "하이", "반가워", "오랜만이야", "나 또 왔", 
        "좋은 아침", "잘 잤어", "좋은 밤", "좋은 저녁", "좋은 점심", "여기야", "반갑다", 
        "돌아왔", "나 왔어", "나 왔", "갔다 왔어", "다녀왔"]
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
class UserData(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.data = self.get_json()
        print(self.data)
        self.repeat_save_user.start()

    @commands.Cog.listener()
    async def on_ready(self):
        print("준비됨")

    def set_json(self):
        """_summary_
            users JSON 에 self.data를 덮어씌움.
        """
        try:
            with open(os.path.join(__location__ + '\\json\\users.json'), "w") as file:
                print(self.data)
                file.write(json.dump(self.data, file, indent=4))
        except TypeError:
            pass

    def get_json(self) -> dict:
        """_summary_
            users JSON 파일을 불러와서 return함
        return Dict
        """
        with open(os.path.join(f"{__location__}\\json\\users.json"),'r',encoding='utf-8') as file:
            print("저장됨")
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
                        "cheeyi": 0,
                        "saehee": 0
                    },
                    "money": 30000,
                    "item": {
                        "a": 1,
                        "b": 0,
                        "c": 99
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
    
    async def give_xp(self, username ,user_id: str, channel: discord.channel):

        """_summary_
            매세지를 보낸 유저에게 xp를 1~2사이로 랜덤 부여. 레벨업을 했는지 확인하여 True를 받으면 self.data레벨을 올림
        Args:
            ctx (_type_): 메세지 Context
        """
        embed=discord.Embed(title="아우우! {}(으)로 레벨 업 하신거예요!!", description="{}")
        embed.set_author(name="치이", icon_url="https://i.imgur.com/m4rkhda.jpg")

        self.check_user(user_id)
        random_xp = random.randint(1, 2)
        self.data[user_id]["level"]["xp"] += random_xp
        if self.level_up(user_id):
            self.data[user_id]["level"]["main"] += 1
            congrats = [f"축하드리는거 예요 {username} 오라버니!!",
                        f"{username} 오라버니 고생이 많으신거예요!",
                        f"아우우!! 벌써 {self.data[user_id]['level']['main']}레벨인 거에요 오라버니!",
                        f"아우? 엄청 빠르신거예요! 축하드려요 {username} 오라버니!",
                        f"아우우우! {self.data[user_id]['level']['main']}레벨 달성은 축하드리지만.. 오라버니도 현생을 사셔야 하는 거예요... ",
                        f"랑이님! 아무리 그래도 이런 축하는 제가 하고 싶은 거예요! 아우우우!!! 헤헤 {username}아! {self.data[user_id]['level']['main']}레벨 축하하느니라!!"
                        ]
            embed=discord.Embed(title=f"아우우! {self.data[user_id]['level']['main']}(으)로 레벨 업 하신거예요!!", description=f"{random.choice(congrats)}", color=0x7a90e1)
            embed.set_author(name="치이", icon_url="https://i.imgur.com/m4rkhda.jpg")
            
            await channel.send(embed=embed)   

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
                for x in self.data.items():
                    self.data[x[0]]["money"] += money
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
                for x in self.data.items():
                    self.data[x[0]]["money"] -= money
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
        print("저장됨")

############################################ 대화 기능 ###########################################################
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot: 
            return None
        if any(x in message.content for x in all_hi) and "랑이야" in message.content:
            rangi_hi = [f"헤헤 안녕 하느냐! {message.author.name}아!",
            f"{message.author.name}아! 안녕하느냐!",
            "반갑느니라!!",
            f"흐냐앗! 왔느냐 {message.author.name}(아)야!",
            "돌아왔구나! 보고싶었느니라!",
            "너가 없는 동안.. 나는 심심했느니라...ㅠㅠ",
            "헤헤 왔으니 이제 놀아주는 것이느냐!",
            "오늘 하루는 어떠하였느냐!? 평화롭지 않느냐! 헤헤",
            f"{message.author.name}(이)가 왔으니 같이 놀아주거라아아!! 놀아주거라!!!! 심심하니라!!"
            "너의 하루는 어땠느냐? 나는 낭군님만 기다리고 있었느니라!"
            f"흐냐아앗!! 내가 얼마나 기다렸는지 알고있느냐!! 하루종일 {message.author.name}(이)만 기다렸느니라!"
            ]
            embed=discord.Embed(title=f"{random.choice(rangi_hi)}", color=0xebe6e6)
            embed.set_author(name="랑이", icon_url="https://i.imgur.com/10PqwRq.jpg")
            contents = message.content.split(" ")
            await message.channel.send(embed=embed)
            await self.give_xp(message.author.name, str(message.author.id), message.channel)
            
            
            
async def setup(bot):
    await bot.add_cog(UserData(bot))
    
