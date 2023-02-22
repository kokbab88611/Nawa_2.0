import discord
from discord.ext import commands
import pymongo
import urllib.parse
import json
import os
import asyncio
import random

#client = pymongo.MongoClient("mongodb+srv://hyun88611:hyun@88611@cluster0.d0nl1ss.mongodb.net/?retryWrites=true&w=majority")
#db = client.userInformation
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
#print(db)

class User(commands.Cog):
  def __init__(self, bot) -> None:
    self.bot = bot
    with open(os.path.join(__location__ + '/json', 'users.json')) as f:
      self.userData = json.load(f)

  def level_up(self, userId):
    current_xp = self.userData[userId]["level"]["xp"]
    current_lvl = self.userData[userId]["level"]["main"]
    
    if current_xp >= round(0.04 * (current_lvl ** 3) + 0.8 * (current_lvl ** 2) + 2 * current_lvl):
      self.userData[userId]["main"] += 1
      return True
    else: 
      return False
  
  async def save(self):
    await self.bot.wait_untill_ready()
    while not self.bot.is_close():
      with open(os.path.join(__location__ + '/json', 'users.json')) as f:
        json.dump(self.userData, f)
      await asyncio.sleep(5)

  @commands.Cog.listener()
  async def on_ready(self):
    print("준비됨")
  
  async def saveUser():
    async def wrapper(ctx, func):
      func()
      with open(os.path.join(__location__ + '/json', 'users.json')) as f:
        data = json.load(f)
        keys = [users for users in data]
        if ctx.author.id not in data:
          data[ctx.author.id] = {
          "level" : {
            "main":1,
            "xp": 0,
            "rangi":0,
            "cheeyi":0,
            "saehee":0
          },
          "money" : 0,
          "item": [],
          "attendence": False
          }
          json.dump(data, f)
        
        random_xp = random.randint(1,2)
        userId
      return wrapper
        
  def nextLevel(level):
     return round( 0.04 * (level ** 3) + 0.8 * (level ** 2) + 2 * level)

  @saveUser()
  @commands.command(name="핑")
  async def ping(self, ctx):
    await ctx.send("퐁이니라!")


async def setup(bot):
  await bot.add_cog(User(bot))