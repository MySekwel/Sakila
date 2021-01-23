import mysql.connector
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
                    user_diamonds,
                    user_exp,
                    user_reputation,
                    user_love,
                    user_vip
                )
                VALUES(
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?
                )
            """
            stats_values = (
                ctx.author.id,
                ctx.author.name,
                ctx.author.discriminator,
                100,
                0,
                0,
                0,
                0,
                'None'
            )
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
                inventory(
                    uid,
                    item_pickaxe,
                    item_drill,
                    item_jackhammer,
                    item_metal_detector,
                    item_gold_detector,
                    item_diamond_detector,
                    item_minecart,
                    item_minetransport,
                    item_transportplane
                )
                VALUES(
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?
                )
            """
            inventory_values = (
                uid,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
            )
            Connection.SQL_Prepared_Cursor.execute(query, inventory_values)
            Connection.SQL_Handle.commit()
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            await ctx.send("**You are already registered to the database!**")
            return

        await ctx.send(
            f"""
            You are now registered to the database with the following information:
            **UID:** `{lastid}`
            **UserID:** `{ctx.author.id}`
            **UserName:** `{ctx.author.name}`
            **UserTag:** `{ctx.author.discriminator}`
        """
        )


def setup(bot):
    bot.add_cog(Authentication(bot))
