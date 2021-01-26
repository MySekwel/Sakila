"""
Module: ./cogs/labor.py
Description: Labor module, includes everything for user work and money earning system.
Module Dependencies:
    > asyncio
    > discord.ext.commands
    > discord.ext.commands.BucketType
    > discord.ext.commands.cooldown
    > discord.ext.commands.CommandOnCooldown
    > main.Connection
    > utils.settings
    > random
"""
import asyncio
import random

from discord import utils, Embed, Colour
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown, CommandOnCooldown

from cogs.user import registered
from main import Connection
from utils import settings


class Labor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Command: Work
    # Description: Mine to earn money
    # Cooldown: 15 - Default
    @commands.command(aliases=["mine"])
    @cooldown(1, 15, BucketType.user)
    async def work(self, ctx):
        if not registered(ctx.author.id):
            embed = Embed(
                title="ERROR",
                description="You are not registered to the database!\n**TIP:** `!register`",
                colour=Colour.red()
            )
            await ctx.channel.trigger_typing()
            await asyncio.sleep(2)
            await ctx.send(embed=embed)
            return

        query = f"""
            SELECT
            uid
            FROM
            users
            WHERE
            user_id={ctx.author.id}
        """
        Connection.SQL_Cursor.execute(query)
        result = Connection.SQL_Cursor.fetchone()
        Connection.SQL_Handle.commit()
        uid = result[0]

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
            "pickaxe": result[0],
            "drill": result[1],
            "jackhammer": result[2],
            "metal_detector": result[3],
            "gold_detector": result[4],
            "diamond_detector": result[5]
        }

        work_salary = 100
        default_salary = 100
        tool = "Shovel"
        metal, gold, diamond = 0, 0, 0

        if tool_name["jackhammer"]:
            tool = "Jackhammer"
            work_salary = default_salary + settings.WORK_SALARY * 1.00
            if tool_name["diamond_detector"]:
                tool += " & Diamond Detector"
                if random.randint(0, 100) < settings.DD_VALUABLE_CHANCE:
                    metal = random.randint(1, 5)
                if random.randint(0, 100) < settings.DD_VALUABLE_CHANCE:
                    gold = random.randint(1, 3)
                if random.randint(0, 100) < settings.DD_VALUABLE_CHANCE:
                    diamond = random.randint(1, 2)
            elif tool_name["gold_detector"]:
                tool += " & Gold Detector"
                if random.randint(0, 100) < settings.GD_VALUABLE_CHANCE:
                    metal = random.randint(1, 5)
                if random.randint(0, 100) < settings.GD_VALUABLE_CHANCE:
                    gold = random.randint(1, 3)
            elif tool_name["metal_detector"]:
                tool += " & Metal Detector"
                if random.randint(0, 100) < settings.MD_VALUABLE_CHANCE:
                    metal = random.randint(1, 5)
        elif tool_name["drill"]:
            tool = "Drill"
            work_salary = default_salary + settings.WORK_SALARY * 0.75
            if tool_name["diamond_detector"]:
                tool += " & Diamond Detector"
                if random.randint(0, 100) < settings.DD_VALUABLE_CHANCE:
                    metal = random.randint(1, 5)
                if random.randint(0, 100) < settings.DD_VALUABLE_CHANCE:
                    gold = random.randint(1, 3)
                if random.randint(0, 100) < settings.DD_VALUABLE_CHANCE:
                    diamond = random.randint(1, 2)
            elif tool_name["gold_detector"]:
                tool += " & Gold Detector"
                if random.randint(0, 100) < settings.GD_VALUABLE_CHANCE:
                    metal = random.randint(1, 5)
                if random.randint(0, 100) < settings.GD_VALUABLE_CHANCE:
                    gold = random.randint(1, 3)
            elif tool_name["metal_detector"]:
                tool += " & Metal Detector"
                if random.randint(0, 100) < settings.MD_VALUABLE_CHANCE:
                    metal = random.randint(1, 5)
        elif tool_name["pickaxe"]:
            tool = "Pickaxe"
            work_salary = default_salary + settings.WORK_SALARY * 0.50
            if tool_name["diamond_detector"]:
                tool += " & Diamond Detector"
                if random.randint(0, 100) < settings.DD_VALUABLE_CHANCE:
                    metal = random.randint(1, 5)
                if random.randint(0, 100) < settings.DD_VALUABLE_CHANCE:
                    gold = random.randint(1, 3)
                if random.randint(0, 100) < settings.DD_VALUABLE_CHANCE:
                    diamond = random.randint(1, 2)
            elif tool_name["gold_detector"]:
                tool += " & Gold Detector"
                if random.randint(0, 100) < settings.GD_VALUABLE_CHANCE:
                    metal = random.randint(1, 5)
                if random.randint(0, 100) < settings.GD_VALUABLE_CHANCE:
                    gold = random.randint(1, 3)
            elif tool_name["metal_detector"]:
                tool += " & Metal Detector"
                if random.randint(0, 100) < settings.MD_VALUABLE_CHANCE:
                    metal = random.randint(1, 5)
        else:
            if tool_name["diamond_detector"]:
                tool += " & Diamond Detector"
                if random.randint(0, 100) < settings.DD_VALUABLE_CHANCE:
                    metal = random.randint(1, 5)
                if random.randint(0, 100) < settings.DD_VALUABLE_CHANCE:
                    gold = random.randint(1, 3)
                if random.randint(0, 100) < settings.DD_VALUABLE_CHANCE:
                    diamond = random.randint(1, 2)
            elif tool_name["gold_detector"]:
                tool += " & Gold Detector"
                if random.randint(0, 100) < settings.GD_VALUABLE_CHANCE:
                    metal = random.randint(1, 5)
                if random.randint(0, 100) < settings.GD_VALUABLE_CHANCE:
                    gold = random.randint(1, 3)
            elif tool_name["metal_detector"]:
                tool += " & Metal Detector"
                if random.randint(0, 100) < settings.MD_VALUABLE_CHANCE:
                    metal = random.randint(1, 5)

        mining = utils.get(self.bot.emojis, name="mining")
        embed = Embed(
            title=f"{str(mining)}Mining in Progress...",
            description=f"**Current Tool**: {tool}",
            colour=Colour.random()
        )
        progress = await ctx.send(embed=embed)
        await asyncio.sleep(15)
        embed = Embed(
            title="Mining Finished!",
            description=f"**You have worked in the mines and earned**\n\
                **Salary:** `${int(work_salary)}`\n\
                **EXP:** `{settings.WORK_BONUS}`\n\
                **Metal:** `{metal}`\n\
                **Gold:** `{gold}`\n\
                **Diamond:** `{diamond}`",
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

        query = f"""
            UPDATE
            inventory
            SET
            metal_metal=metal_metal+?,
            metal_gold=metal_gold+?,
            metal_diamond=metal_diamond+?
            WHERE
            uid={uid}
        """
        values = (metal, gold, diamond)
        Connection.SQL_Prepared_Cursor.execute(query, values)
        Connection.SQL_Handle.commit()

    @work.error
    async def work_error(self, ctx, exc):
        if isinstance(exc, CommandOnCooldown):
            await ctx.reply(
                f"Hey, you still have a work in progress," +
                f" why don't you wait for `{exc.retry_after:,.1f}` seconds?"
            )


def setup(bot):
    bot.add_cog(Labor(bot))
