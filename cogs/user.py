import discord
from discord.ext import commands
import pymongo
import urllib.parse
import json
import os

#client = pymongo.MongoClient("mongodb+srv://hyun88611:hyun@88611@cluster0.d0nl1ss.mongodb.net/?retryWrites=true&w=majority")
#db = client.userInformation
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
#print(db)

class User(commands.Cog):
  def __init__(self, bot) -> None:
    self.bot = bot
    
  @commands.Cog.listener()
  async def on_ready(self):
    print("준비됨")
  
  async def saveUser():
    async def wrapper(ctx, func):
      await func()
      with open(os.path.join(__location__, 'users.json')) as f:
        data = json.load(f)
        keys = [users for users in data]
        if ctx.author.id not in data:
          data[ctx.author.id] = {
          "level" : {
            "main":0,
            "rangi":0,
            "cheeyi":0,
            "saehee":0
          },
          "money" : 0,
          "item": []
          }
          await json.dump(data, f)
        else:
          await data[ctx.author.id]
      return wrapper
        
  def nextLevel(level):
     return round( 0.04 * (level ** 3) + 0.8 * (level ** 2) + 2 * level)

  #@saveUser()
  @commands.command(name="핑")
  async def ping(self, ctx):
    await ctx.send("퐁이니라!")


async def setup(bot):
  await bot.add_cog(User(bot))