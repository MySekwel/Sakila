import asyncio

from discord import Embed, Colour
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType

from cogs import user
from main import Connection


class Miner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @cooldown(1, 5, BucketType.user)
    async def virtualmarket(self, ctx):
        if not user.registered(ctx.author):
            embed = Embed(
                title="ERROR",
                description="You are not registered to the database!\n**TIP:** `!register`",
                colour=Colour.red()
            )
            await ctx.channel.trigger_typing()
            await asyncio.sleep(2)
            await ctx.send(embed=embed)
            return

        query = """
            SELECT
            crypto_rig
            FROM
            crypto
            WHERE
        """
        Connection.SQL_Cursor.execute(query)
        Connection.SQL_Handle.commit()


def setup(bot):
    bot.add_cog(Miner(bot))
