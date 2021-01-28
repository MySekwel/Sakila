import asyncio
import random

from discord import Embed, Colour
from discord.ext import commands

from cogs.user import registered
from main import Connection


class Casino(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def dice(self, ctx, bet, rolls=2):
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
            user_cash
            FROM
            users
            WHERE
            user_id={ctx.author.id}
        """
        Connection.SQL_Cursor.execute(query)
        result = Connection.SQL_Cursor.fetchone()
        Connection.SQL_Handle.commit()
        cash = result[0]
        if cash >= int(bet):
            embed = Embed(
                title="Rolling Dice...",
                description=f"${bet} bet has been placed, {rolls} dice will roll, goodluck!",
                colour=Colour.random()
            )
            embed.set_thumbnail(url="https://thumbs.gfycat.com/ElatedImpartialArmadillo-max-1mb.gif")
            message = await ctx.send(embed=embed)
            await asyncio.sleep(5)
            user_result = random.randint(1, 6 * int(rolls))
            dealer_result = random.randint(1, 6 * int(rolls))
            if user_result > dealer_result:
                query = f"""
                    UPDATE
                    users
                    SET
                    user_cash=?
                    WHERE
                    user_id={ctx.author.id}
                """
                win = cash + int(bet)
                Connection.SQL_Prepared_Cursor.execute(query, (win,))
                Connection.SQL_Handle.commit()

                embed = Embed(
                    title="You won!",
                    description=f"Congratulations, {ctx.author.name}! You've won ${bet}.\n**Summary**\nYour roll: {user_result}\nDealer's Roll: {dealer_result}",
                    colour=Colour.green()
                )
                embed.set_thumbnail(url="https://media.tenor.com/images/99cff34bdcb675975b2b0cc661f2e4ce/tenor.gif")
                await message.edit(embed=embed)
            elif user_result == dealer_result:
                embed = Embed(
                    title="Draw!",
                    description=f"It's a draw!\n**Summary**\nYour roll: {user_result}\nDealer's Roll: {dealer_result}",
                    colour=Colour.gold()
                )
                embed.set_thumbnail(url="https://media.tenor.com/images/99cff34bdcb675975b2b0cc661f2e4ce/tenor.gif")
                await message.edit(embed=embed)
            else:
                query = f"""
                    UPDATE
                    users
                    SET
                    user_cash=?
                    WHERE
                    user_id={ctx.author.id}
                """
                lost = cash - int(bet)
                Connection.SQL_Prepared_Cursor.execute(query, (lost,))
                Connection.SQL_Handle.commit()
                embed = Embed(
                    title="You lost!",
                    description=f"Better luck next Timer, {ctx.author.name}! You've lost ${bet}.\n**Summary**\nYour roll: {user_result}\nDealer's Roll: {dealer_result}",
                    colour=Colour.orange()
                )
                embed.set_thumbnail(url="https://media.tenor.com/images/2b454269146fcddfdae60d3013484f0f/tenor.gif")
                await message.edit(embed=embed)
        else:
            embed = Embed(
                title="Error",
                description=f"You don't have that amount of cash! `!work` to earn more.",
                colour=Colour.red()
            )
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Casino(bot))
