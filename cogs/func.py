import discord
from discord.ext import commands

class Ping(commands.Cog):
  def __init__(self, bot) -> None:
    self.bot = bot
    
  @commands.Cog.listener()
  async def on_ready(self):
    print("준비됨")
  
  @commands.command(name="핑")
  async def ping(self, ctx):
    await ctx.send("퐁이니라!")

  @commands.command(name=";바꿔")
  async def changePresence(self, ctx, *,customName):
    await ctx.send(customName)
    status = discord.Game(name=customName)
    await self.bot.change_presence(status=discord.Status.online, activity=status)
    
async def setup(bot):
  await bot.add_cog(Ping(bot))