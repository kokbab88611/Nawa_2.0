import discord
from discord.ext import commands, tasks

class Admin(commands.Cog):
  def __init__(self, bot) -> None:
    self.bot = bot
  
  @commands.Cog.listener()
  async def on_ready(self):
    print("준비됨")

async def setup(bot):
  await bot.add_cog(Admin(bot))