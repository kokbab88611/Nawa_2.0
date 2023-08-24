import discord
from discord.ext import commands
import os

token = 'NTE1NDE2ODQ4NDc3NTg1NDEw.GYje9-.J12NOzBJHPo4UN9Sixd-ELSG3laAdIDuLgCLzQ'
intents=discord.Intents.all()
intents.presences = False
bot = commands.Bot(
    command_prefix="",
    intents=intents,
    sync_commands=True
)

extensions = []

async def load_cogs():
    for file in os.listdir('./cogs'):
        if file.endswith('.py'):
            await bot.load_extension(f'cogs.{file[:-3]}')
            print(f"{file[:-3]}을 불러왔느니라!")
    synced = await bot.tree.sync()
    print(f"{len(synced)}개의 커맨드를 sync했느니라!")

@bot.event
async def setup_hook():
    """ 
    Cog폴드에 있는 Cog와 슬래시 커맨드를 sync함
    해당 코드가 없으면 슬래시 커맨드가 작동되지 않을뿐더러 자동완성 기능또한 사용불가
    """
    await load_cogs()

@bot.event
async def on_ready():
    print(bot.user.name)

bot.run(token)
 