import discord
from discord.ext import commands, tasks
from discord.ext.commands import Context
from discord import app_commands
import os

token = 'NDY0MDk4MzA3MjcxMDMyODQy.GCLAvK.ByV_tr0qtC7vLvMQQRQxKtsHncttjUO0DlMeJ4'

class Nawa(commands.Bot):
  def __init__(self):
    super().__init__(
        command_prefix="",
        intents=discord.Intents.all(),
        sync_command=True
    )
    
  async def setup_hook(self):
    """ Cog폴드에 있는 Cog와 슬래시 커맨드를 sync함
        해당 코드가 없으면 슬래시 커맨드가 작동되지 않을뿐더러 자동완성 기능또한 사용불가
    """
    for file in os.listdir('./cogs'):
      if file.endswith('.py'):
        await self.load_extension(f'cogs.{file[:-3]}')
        print(f"{file[:-3]}을 불러왔느니라!")
    synced = await bot.tree.sync()
    print(f"{len(synced)}개의 커맨드를 sync했느니라!")

  async def on_ready(self):
      print("준비되었느니라!")
  
  # async def reloadCog(self):
  #   """Cog 폴더에 있는 파일들을 다시 불러옴
  #   """
  #   for file in os.listdir('./cogs'):
  #     if file.endswith('.py'):
  #       await self.reload_extension(f'cogs.{file[:-3]}')
  #       print(f"{file[:-3]}를 재정비 했느니라!") 

bot = Nawa()     
bot.run(token=token)
  