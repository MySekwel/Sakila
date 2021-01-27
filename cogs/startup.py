import datetime

from discord import Game, state
from discord.ext import commands


class Startup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_connect(self):
        await self.bot.change_presence(
            activity=Game(
                name="Console Adventures",
                start=datetime.datetime.now()
            ),
            status=state.Status.online
        )

    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            print(f"{self.bot.user} is now connected to guild: {guild.name}")


def setup(bot):
    bot.add_cog(Startup(bot))
