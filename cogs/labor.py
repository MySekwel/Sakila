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

from cogs import user
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
        if not user.registered(ctx.author.id):
            await user.send_notregistered_msg(ctx)
            return
        work_salary = 100
        default_salary = 100
        tool = "Shovel"
        metal, gold, diamond = 0, 0, 0

        if user.has_jackhammer(ctx.author):
            tool = "Jackhammer"
            work_salary = default_salary + settings.WORK_SALARY * 1.00
            if user.has_diamonddetector(ctx.author):
                tool += " & Diamond Detector"
                if random.randint(0, 100) < settings.DD_VALUABLE_CHANCE:
                    metal = random.randint(1, 5)
                if random.randint(0, 100) < settings.DD_VALUABLE_CHANCE:
                    gold = random.randint(1, 3)
                if random.randint(0, 100) < settings.DD_VALUABLE_CHANCE:
                    diamond = random.randint(1, 2)
            elif user.has_golddetector(ctx.author):
                tool += " & Gold Detector"
                if random.randint(0, 100) < settings.GD_VALUABLE_CHANCE:
                    metal = random.randint(1, 5)
                if random.randint(0, 100) < settings.GD_VALUABLE_CHANCE:
                    gold = random.randint(1, 3)
            elif user.has_metaldetector(ctx.author):
                tool += " & Metal Detector"
                if random.randint(0, 100) < settings.MD_VALUABLE_CHANCE:
                    metal = random.randint(1, 5)
        elif user.has_drill(ctx.author):
            tool = "Drill"
            work_salary = default_salary + settings.WORK_SALARY * 0.75
            if user.has_diamonddetector(ctx.author):
                tool += " & Diamond Detector"
                if random.randint(0, 100) < settings.DD_VALUABLE_CHANCE:
                    metal = random.randint(1, 5)
                if random.randint(0, 100) < settings.DD_VALUABLE_CHANCE:
                    gold = random.randint(1, 3)
                if random.randint(0, 100) < settings.DD_VALUABLE_CHANCE:
                    diamond = random.randint(1, 2)
            elif user.has_golddetector(ctx.author):
                tool += " & Gold Detector"
                if random.randint(0, 100) < settings.GD_VALUABLE_CHANCE:
                    metal = random.randint(1, 5)
                if random.randint(0, 100) < settings.GD_VALUABLE_CHANCE:
                    gold = random.randint(1, 3)
            elif user.has_metaldetector(ctx.author):
                tool += " & Metal Detector"
                if random.randint(0, 100) < settings.MD_VALUABLE_CHANCE:
                    metal = random.randint(1, 5)
        elif user.has_pickaxe(ctx.author):
            tool = "Pickaxe"
            work_salary = default_salary + settings.WORK_SALARY * 0.50
            if user.has_diamonddetector(ctx.author):
                tool += " & Diamond Detector"
                if random.randint(0, 100) < settings.DD_VALUABLE_CHANCE:
                    metal = random.randint(1, 5)
                if random.randint(0, 100) < settings.DD_VALUABLE_CHANCE:
                    gold = random.randint(1, 3)
                if random.randint(0, 100) < settings.DD_VALUABLE_CHANCE:
                    diamond = random.randint(1, 2)
            elif user.has_golddetector(ctx.author):
                tool += " & Gold Detector"
                if random.randint(0, 100) < settings.GD_VALUABLE_CHANCE:
                    metal = random.randint(1, 5)
                if random.randint(0, 100) < settings.GD_VALUABLE_CHANCE:
                    gold = random.randint(1, 3)
            elif user.has_metaldetector(ctx.author):
                tool += " & Metal Detector"
                if random.randint(0, 100) < settings.MD_VALUABLE_CHANCE:
                    metal = random.randint(1, 5)
        else:
            if user.has_diamonddetector(ctx.author):
                tool += " & Diamond Detector"
                if random.randint(0, 100) < settings.DD_VALUABLE_CHANCE:
                    metal = random.randint(1, 5)
                if random.randint(0, 100) < settings.DD_VALUABLE_CHANCE:
                    gold = random.randint(1, 3)
                if random.randint(0, 100) < settings.DD_VALUABLE_CHANCE:
                    diamond = random.randint(1, 2)
            elif user.has_golddetector(ctx.author):
                tool += " & Gold Detector"
                if random.randint(0, 100) < settings.GD_VALUABLE_CHANCE:
                    metal = random.randint(1, 5)
                if random.randint(0, 100) < settings.GD_VALUABLE_CHANCE:
                    gold = random.randint(1, 3)
            elif user.has_metaldetector(ctx.author):
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
        await progress.edit(embed=embed)

        user.update_cash(ctx.author, work_salary)
        user.update_exp(ctx.author, settings.WORK_BONUS)

        query = """
            UPDATE
            inventory
            SET
            metal_metal=metal_metal+?,
            metal_gold=metal_gold+?,
            metal_diamond=metal_diamond+?
            WHERE
            uid=?
        """
        values = (metal, gold, diamond, user.get_uid(ctx.author))
        Connection.SQL_Cursor.execute(query, values)
        Connection.SQL_Handle.commit()

        query = """
            SELECT
            record_metal_mined,
            record_gold_mined,
            record_diamond_mined
            FROM
            record
            WHERE
            uid=?
        """
        Connection.SQL_Cursor.execute(query, (user.get_uid(ctx.author),))
        result = Connection.SQL_Cursor.fetchone()
        Connection.SQL_Handle.commit()
        fetched_metal, fetched_gold, fetched_diamonds = int(result[0]), int(result[1]), int(result[2])
        if fetched_metal < metal:
            query = f"UPDATE record SET record_metal_mined={metal} WHERE uid=?"
            Connection.SQL_Cursor.execute(query, (user.get_uid(ctx.author),))
            Connection.SQL_Handle.commit()
        if fetched_gold < gold:
            query = f"UPDATE record SET record_gold_mined={gold} WHERE uid=?"
            Connection.SQL_Cursor.execute(query, (user.get_uid(ctx.author),))
            Connection.SQL_Handle.commit()
        if fetched_diamonds < diamond:
            query = f"UPDATE record SET record_diamond_mined={diamond} WHERE uid=?"
            Connection.SQL_Cursor.execute(query, (user.get_uid(ctx.author),))
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
