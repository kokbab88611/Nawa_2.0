import discord
from discord import app_commands
from discord.ext import commands
import pymongo
import json
import os
import random
from discord.ext.commands import has_permissions, MissingPermissions

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
class GuildData(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("준비됨")

    def check_guild(self, guild_id: str):
        with open(os.path.join(__location__ + '\\json\\guilds.json'), "r+") as f:
            data = json.load(f)
            if guild_id not in data:
                data[guild_id] = {
                        "warnLimit": 3,
                        "warned": {   
                        }
                    }
                print("길드 없었어")
                with open(os.path.join(__location__ + '\\json\\guilds.json'), "w+") as f:
                    json.dump(data, f, indent=4)
            else:
                pass
    
    def check_user(self, guild_id: str ,user_id: str, user_name: str):
        with open(os.path.join(__location__ + '\\json\\guilds.json'), "r+") as f:
            data = json.load(f)
            if str(user_id) not in data[guild_id]["warned"]:
                data[guild_id]["warned"][user_id] = {
                        "user_name": user_name,
                        "warning": 0
                    }
                print("유저 없었어")
                with open(os.path.join(__location__ + '\\json\\guilds.json'), "w+") as f:
                    json.dump(data, f, indent=4)
            else:
                pass
    
    @app_commands.command(name="경고한도", description="경고 한도를 설정합니다, 경고한도 초과시 관리자에게 알림 /경고한도 (경고 수)")
    @app_commands.checks.has_permissions(kick_members=True)
    async def warnLimit(self, interaction: discord.Interaction, warn_number: int) -> None: 
        #await ctx.invoke(self.bot.get_command('핑'))
        self.check_guild(interaction.guild.id)
        with open(os.path.join(__location__ + '\\json\\guilds.json'), "r+") as f:
            data = json.load(f)
            data[str(interaction.guild.id)]["warnLimit"] = warn_number   
        with open(os.path.join(__location__ + '\\json\\guilds.json'), "w+") as f:
            json.dump(data, f, indent=4)

        embed=discord.Embed(title=f"경고 한도를 {warn_number}로 저장했느니라", description="경고 한도 초과시 관리자가 즉시 조치를 취할 수 있도록 하는 기능이니라", color=0xb0a7d3)
        embed.set_author(name="냥이", icon_url="https://i.imgur.com/ORq6ORB.jpg")
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="경고", description="해당 유저에게 경고 1회를 부여하는 것 이니라 /경고 (멘션or닉네임) (사유)")
    @app_commands.checks.has_permissions(kick_members=True)
    async def warn(self, interaction: discord.Interaction, user: discord.Member, reason: str = "사유 없음") -> None: 
        self.check_guild(str(interaction.guild.id))
        self.check_user(str(interaction.guild.id), str(user.id), str(user.name))
        with open(os.path.join(__location__ + '\\json\\guilds.json'), "r+") as f:
            data = json.load(f)
            data[str(interaction.guild.id)]["warned"][str(user.id)]["warning"] += 1

        with open(os.path.join(__location__ + '\\json\\guilds.json'), "w+") as f:
            json.dump(data, f, indent=4)

        embed=discord.Embed(title=f"{user.name} (이)에게 경고 1회를 부여 하였느니라", description=f"사유: {reason}", color=0xb0a7d3)
        embed.set_author(name="냥이", icon_url="https://i.imgur.com/ORq6ORB.jpg")

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(GuildData(bot))
    