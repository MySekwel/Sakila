import asyncio

from discord import utils, Embed, Colour
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType, CommandOnCooldown

from main import Connection
import settings


class Labor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Command: Work
    # Description: Mine to earn money
    # Cooldown: 15 - Default
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
        Connection.SQL_Cursor.execute(query)
        result = Connection.SQL_Cursor.fetchone()
        Connection.SQL_Handle.commit()
        uid = result[0]
        if not result:
            embed = Embed(
                title='ERROR',
                description='You are not registered to the database!\n**TIP:** `!register`',
                colour=Colour.red()
            )
            
            await ctx.send(embed=embed)
            return

        query = f"""
            SELECT
            item_pickaxe,
            item_drill,
            item_jackhammer,
            item_metal_detector,
            item_gold_detector,
            item_diamond_detector,
            item_minecart,
            item_minetransport,
            item_transportplane
            FROM
            inventory
            WHERE
            uid={uid}
        """
        Connection.SQL_Cursor.execute(query)
        result = Connection.SQL_Cursor.fetchone()
        Connection.SQL_Handle.commit()

        tool_name = {
            'pickaxe': result[0],
            'drill': result[1],
            'jackhammer': result[2],
            'metal_detector': result[3],
            'gold_detector': result[4],
            'diamond_detector': result[5]
        }

        work_salary = 100
        default_salary = 100
        tool = 'Shovel'

        if tool_name['pickaxe']:
            tool = 'Pickaxe'
            work_salary = default_salary + settings.WORK_SALARY * 0.05
        if tool_name['drill']:
            tool = 'Drill'
            work_salary = default_salary + settings.WORK_SALARY * 0.10
        if tool_name['jackhammer']:
            tool = 'Jackhammer'
            work_salary = default_salary + settings.WORK_SALARY * 0.25
        if tool_name['metal_detector']:
            tool = 'Metal Detector'
            work_salary = default_salary + settings.WORK_SALARY * 0.35
        if tool_name['gold_detector']:
            tool = 'Gold Detector'
            work_salary = default_salary + settings.WORK_SALARY * 0.50
        if tool_name['diamond_detector']:
            tool = 'Diamond Detector'
            work_salary = default_salary + settings.WORK_SALARY * 0.75

        mining = utils.get(self.bot.emojis, name='mining')
        embed = Embed(
            title=f'{str(mining)}Mining in Progress...',
            description=f'**Current Tool**: {tool}',
            colour=Colour.random()
        )
        progress = await ctx.send(embed=embed)
        await asyncio.sleep(15)
        embed = Embed(
            title='Mining Finished!',
            description=f'**You have worked in the mines and earned \
             ${int(work_salary)} and {settings.WORK_BONUS} exp**',
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
        values = (work_salary, settings.WORK_BONUS)
        Connection.SQL_Prepared_Cursor.execute(query, values)
        Connection.SQL_Handle.commit()

    @work.error
    async def work_error(self, ctx, exc):
        if isinstance(exc, CommandOnCooldown):
            await ctx.send(
                f"Hey <@!{ctx.author.id}> you still have a work in progress," +
                f" why don't you wait for `{exc.retry_after:,.1f}` seconds?"
            )


def setup(bot):
    bot.add_cog(Labor(bot))
