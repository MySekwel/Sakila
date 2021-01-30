import asyncio
import random

from discord import Embed, Colour
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType

from cogs import user
from main import Connection


class Casino(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @cooldown(1, 5, BucketType.user)
    async def dice(self, ctx, bet, rolls=2):
        if not user.registered(ctx.author.id):
            embed = Embed(
                title="ERROR",
                description="You are not registered to the database!\n**TIP:** `!register`",
                colour=Colour.red()
            )
            await ctx.channel.trigger_typing()
            await asyncio.sleep(2)
            await ctx.send(embed=embed)
            return
        if user.get_cash(ctx.author) >= int(bet):
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
                    uid={user.get_uid(ctx.author)}
                """
                win = user.get_cash(ctx.author) + int(bet)
                Connection.SQL_Prepared_Cursor.execute(query, (win,))
                Connection.SQL_Handle.commit()

                embed = Embed(
                    title="You won!",
                    description=f"Congratulations, {ctx.author.name}! You've won ${bet}.\n\n**Summary:**\nYour roll: {user_result}\nDealer's Roll: {dealer_result}",
                    colour=Colour.green()
                )
                embed.set_thumbnail(url="https://media.tenor.com/images/99cff34bdcb675975b2b0cc661f2e4ce/tenor.gif")
                await message.edit(embed=embed)
            elif user_result == dealer_result:
                embed = Embed(
                    title="Draw!",
                    description=f"It's a draw!\n\n**Summary:**\nYour roll: {user_result}\nDealer's Roll: {dealer_result}",
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
                    uid={user.get_uid(ctx.author)}
                """
                lost = user.get_cash(ctx.author) - int(bet)
                Connection.SQL_Prepared_Cursor.execute(query, (lost,))
                Connection.SQL_Handle.commit()
                embed = Embed(
                    title="You lost!",
                    description=f"Better luck next Timer, {ctx.author.name}! You've lost ${bet}.\n\n**Summary:**\nYour roll: {user_result}\nDealer's Roll: {dealer_result}",
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
