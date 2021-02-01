"""
Module: ./cogs/auth.py
Description: Authentication module, includes everything that a user need to authenticate and be added in the database.
Module Dependencies:
    > mysql.connector
    > discord.ext.commands
"""
import asyncio

import mysql.connector
from discord import Embed, Colour
from discord.ext import commands

from main import Connection


class Authentication(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Command: Register
    # Description: Register to the database command to use other commands
    @commands.command()
    async def register(self, ctx):
        query = """
            SELECT
            MAX(uid)
            FROM
            users
        """
        Connection.SQL_Cursor.execute(query)
        result = Connection.SQL_Cursor.fetchone()
        Connection.SQL_Handle.commit()
        lastid = result[0]
        if lastid:
            lastid = lastid + 1
        try:
            query = """
                INSERT INTO
                users(
                    user_id,
                    user_name,
                    user_tag,
                    user_cash,
                    user_bank,
                    user_exp,
                    user_reputation,
                    user_love,
                    user_vip
                )
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            stats_values = (ctx.author.id, ctx.author.name, ctx.author.discriminator, 100, 0, 0, 0, 0, "None")
            Connection.SQL_Prepared_Cursor.execute(query, stats_values)
            Connection.SQL_Handle.commit()
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
            query = """
                INSERT INTO
                equipment(
                    uid,
                    equipment_pickaxe,
                    equipment_drill,
                    equipment_jackhammer,
                    equipment_metal_detector,
                    equipment_gold_detector,
                    equipment_diamond_detector,
                    equipment_minecart,
                    equipment_minetransport,
                    equipment_transportplane
                )
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            inventory_values = (uid, 0, 0, 0, 0, 0, 0, 0, 0, 0)
            Connection.SQL_Prepared_Cursor.execute(query, inventory_values)
            Connection.SQL_Handle.commit()
            query = """
                INSERT INTO
                inventory(
                    uid,
                    metal_metal,
                    metal_gold,
                    metal_diamond
                )
                VALUES(?, ?, ?, ?)
            """
            inventory_values = (uid, 0, 0, 0)
            Connection.SQL_Prepared_Cursor.execute(query, inventory_values)
            Connection.SQL_Handle.commit()
            query = """
                INSERT INTO
                record(
                    uid,
                    record_metal_mined,
                    record_gold_mined,
                    record_diamond_mined,
                    record_bets_won,
                    record_highest_roll,
                    record_bitcoin_mined
                )
                VALUES(?, ?, ?, ?, ?, ?, ?)
            """
            inventory_values = (uid, 0, 0, 0, 0, 0, 0)
            Connection.SQL_Prepared_Cursor.execute(query, inventory_values)
            Connection.SQL_Handle.commit()
        except mysql.connector.Error as err:
            await ctx.channel.trigger_typing()
            await asyncio.sleep(2)
            await ctx.send("**You are already registered to the database!**")
            raise err

        await ctx.channel.trigger_typing()
        await asyncio.sleep(2)
        embed = Embed(
            title="SUCCESS",
            description="You are now registered to the database with the following information:",
            colour=Colour.green()
        )
        embed.add_field(
            name="User:",
            value=f"`{lastid}`",
            inline=True
        )
        embed.add_field(
            name="User ID:",
            value=f"`{ctx.author.id}`",
            inline=True
        )
        embed.add_field(
            name="User Name:",
            value=f"`{ctx.author.name}`",
            inline=True
        )
        embed.add_field(
            name="User Tag:",
            value=f"`{ctx.author.discriminator}`",
            inline=True
        )
        await ctx.channel.trigger_typing()
        await asyncio.sleep(2)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Authentication(bot))
