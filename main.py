import discord
import asyncio
from discord.ext import commands, tasks
from discord.ext.commands import Context
from discord import app_commands

import os
token = 'NDY0MDk4MzA3MjcxMDMyODQy.GCLAvK.ByV_tr0qtC7vLvMQQRQxKtsHncttjUO0DlMeJ4'

intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix="", intents=intents, help_command=None)
extensions = ['cogs.func']

@bot.event  
async def on_ready():
  print("준비됐느니라!", bot.user)

async def loadCog():
  for file in os.listdir('./cogs'):
    if file.endswith('.py'):
      await bot.load_extension(f'cogs.{file[:-3]}')
      print(f"{file[:-3]} called")
      
async def main():
  async with bot:
    await loadCog()
    await bot.start(token)

asyncio.run(main())
   