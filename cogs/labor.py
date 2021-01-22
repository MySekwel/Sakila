import asyncio

from discord import utils, Embed, Colour
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType, CommandOnCooldown

import main
import settings


class Labor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Command: Work
    # Description: Mine to earn money
    # Cooldown: 15 seconds
    @commands.command()
    @cooldown(1, 15, BucketType.user)
    async def work(self, ctx):
        query = f"""
            SELECT
            *
            FROM
            users
            WHERE
            user_id={ctx.author.id}
        """
        main.SQL_Cursor.execute(query)
        result = main.SQL_Cursor.fetchone()
        main.SQL_Handle.commit()
        if not result:
            await ctx.send("**You are not registered to the database!**")
            await ctx.send("TIP: `!register`")
            return

        mining = utils.get(self.bot.emojis, name='mining')
        embed = Embed(
            title=f'{str(mining)}Mining in Progress...',
            description='**Current Tool**: Pickaxe',
            colour=Colour.random()
        )
        progress = await ctx.send(embed=embed)
        await asyncio.sleep(15)
        embed = Embed(
            title='Mining Finished!',
            description=f'**You have worked in the mines and earned \
             ${settings.WORK_SALARY} and {settings.WORK_BONUS} exp**',
            colour=Colour.green()
        )
        await progress.edit(
            embed=embed
        )
        query = f"""
            UPDATE
            users
            SET
            user_cash=user_cash+?,
            user_exp=user_exp+?
            WHERE
            user_id={ctx.author.id}
        """
        values = (settings.WORK_SALARY, settings.WORK_BONUS)
        main.SQL_Prepared_Cursor.execute(query, values)
        main.SQL_Handle.commit()

    @work.error
    async def work_error(self, ctx, exc):
        if isinstance(exc, CommandOnCooldown):
            await ctx.send(
                f"Hey <@!{ctx.author.id}> you still have a work in progress," +
                f" why don't you wait for `{exc.retry_after:,.1f}` seconds?"
            )


def setup(bot):
    bot.add_cog(Labor(bot))
