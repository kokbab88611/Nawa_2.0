import discord
from discord.ext import commands
import os

token = 'NDY0MDk4MzA3MjcxMDMyODQy.GCLAvK.ByV_tr0qtC7vLvMQQRQxKtsHncttjUO0DlMeJ4'

bot = commands.Bot(
    command_prefix="",
    intents=discord.Intents.all(),
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
