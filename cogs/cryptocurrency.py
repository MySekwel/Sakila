import asyncio
import datetime
import os
import random
import string

import numpy as np
from discord import Embed, Colour, utils, File
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType, CommandOnCooldown
from cogs import user
from cogs.help import empty_field
from main import Connection
from utils import emoji_dictionary as emojii

import matplotlib.pyplot as plt


def miner(_user):
    query = f"SELECT * FROM crypto WHERE uid={user.get_uid(_user)}"
    Connection.SQL_Cursor.execute(query)
    result = Connection.SQL_Cursor.fetchone()
    Connection.SQL_Handle.commit()
    return result


def has_rig(_user):
    query = f"SELECT crypto_rig FROM crypto WHERE uid={user.get_uid(_user)}"
    Connection.SQL_Cursor.execute(query)
    result = Connection.SQL_Cursor.fetchone()
    Connection.SQL_Handle.commit()
    return int(result[0])


def bitcoins(_user):
    query = f"SELECT crypto_currency FROM crypto WHERE uid={user.get_uid(_user)}"
    Connection.SQL_Cursor.execute(query)
    result = Connection.SQL_Cursor.fetchone()
    Connection.SQL_Handle.commit()
    return float(result[0])


def has_wallet(_user):
    query = f"SELECT crypto_wallet FROM crypto WHERE uid={user.get_uid(_user)}"
    Connection.SQL_Cursor.execute(query)
    result = Connection.SQL_Cursor.fetchone()
    Connection.SQL_Handle.commit()
    return int(result[0])


async def send_notminer_msg(message):
    embed = Embed(
        title="ERROR",
        description="You don't have a mining rig yet!\n**TIP:** `!crypto market buy rig`",
        colour=Colour.red()
    )
    await message.channel.trigger_typing()
    await asyncio.sleep(2)
    await message.send(embed=embed)


class Miner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    @cooldown(1, 5, BucketType.user)
    async def crypto(self, ctx):
        if not user.registered(ctx.author.id):
            await user.send_notregistered_msg(ctx)
            return

    @crypto.group(invoke_without_command=True)
    async def market(self, ctx):
        pass

    @market.command()
    async def buy(self, ctx, item):
        if item.casefold() == "rig":
            uid = user.get_uid(ctx.author)
            query = f"""
                INSERT
                INTO
                crypto(
                    uid,
                    crypto_rig,
                    crypto_wallet,
                    crypto_currency
                )
                VALUES(?, ?, ?, ?)
            """
            Connection.SQL_Prepared_Cursor.execute(query, (uid, 1, 0, 0))
            Connection.SQL_Handle.commit()
            embed = Embed(
                title="Success",
                description="You have bought a rig! You can now start mining for crypto currencies.",
                colour=Colour.green()
            )
            embed.add_field(
                name=emojii.special["empty"],
                value="**TIP:** You can now use `!crypto download wallet` to download your crypto wallet.",
                inline=True
            )
            await ctx.send(embed=embed)

    @crypto.group(invoke_without_command=True)
    async def download(self, ctx):
        await send_notminer_msg(ctx)
        return

    @download.command()
    async def wallet(self, ctx):
        if has_wallet(ctx.author):
            embed = Embed(
                title="ERROR",
                description="You already have a crypto wallet!",
                colour=Colour.red()
            )
            await ctx.send(embed=embed)
            return
        query = f"""
                UPDATE
                crypto
                SET
                crypto_wallet=1
                WHERE
                uid={user.get_uid(ctx.author)}
            """
        Connection.SQL_Cursor.execute(query)
        Connection.SQL_Handle.commit()
        await ctx.channel.trigger_typing()
        await asyncio.sleep(2)
        embed = Embed(
            title="Downloading Crypto Wallet",
            description="**Progress:**\n" + ":white_large_square:" * 10,
            colour=Colour.magenta()
        )
        time = datetime.datetime.now()
        embed.set_footer(text=time.strftime(f"Date: %B %d, %Y | %I:%M %p"))
        progress = await ctx.send(embed=embed)
        ii = 10
        for i in range(1, 10):
            ii -= 1
            await asyncio.sleep(1)
            embed = Embed(
                title="Downloading Crypto Wallet",
                description=("**Progress:**\n" + ":green_square:" * i) + ":white_large_square:" * ii,
                colour=Colour.magenta()
            )
            time = datetime.datetime.now()
            embed.set_footer(text=time.strftime(f"Date: %B %d, %Y | %I:%M %p"))
            await progress.edit(embed=embed)
        await asyncio.sleep(1)
        embed = Embed(
            title="Success!",
            description="Crypto Wallet has been downloaded to your rig.\n\n**Progress:**\n" + "" + ":green_square:" * 10,
            colour=Colour.magenta()
        )
        time = datetime.datetime.now()
        embed.set_footer(text=time.strftime(f"Date: %B %d, %Y | %I:%M %p"))
        await progress.edit(embed=embed)

    @crypto.command()
    async def mine(self, ctx):
        if not miner(ctx.author):
            await send_notminer_msg(ctx)
            return
        if not has_wallet(ctx.author):
            embed = Embed(
                title="ERROR",
                description="You don't have a crypto wallet!\n**TIP:** `!crypto download wallet`",
                colour=Colour.red()
            )
            await ctx.send(embed=embed)
            return
        alphabet = string.ascii_letters
        rand_letter_1 = random.choices(population=alphabet, k=10)
        rand_letter_2 = random.choices(population=alphabet, k=5)
        rand_letter_3 = random.choices(population=alphabet, k=15)
        joined_ouput = ("".join(rand_letter_1), "".join(rand_letter_2), "".join(rand_letter_3))
        formatted_output = "-".join(joined_ouput)
        embed = Embed(
            title="Decoding hashed equation...",
            description=f"Hash: `{formatted_output.casefold()}`\n\n" + f"**Progress:**\n" + ":white_large_square:" * 10,
            colour=Colour.purple()
        )
        time = datetime.datetime.now()
        embed.set_footer(text=time.strftime(f"Date: %B %d, %Y | %I:%M %p"))
        progress = await ctx.send(embed=embed)
        ii = 10
        for i in range(1, 10):
            rand_letter_1 = random.choices(population=alphabet, k=10)
            rand_letter_2 = random.choices(population=alphabet, k=5)
            rand_letter_3 = random.choices(population=alphabet, k=15)
            joined_ouput = ("".join(rand_letter_1), "".join(rand_letter_2), "".join(rand_letter_3))
            formatted_output = "-".join(joined_ouput)
            ii -= 1
            await asyncio.sleep(2)
            embed = Embed(
                title="Decoding hashed equation...",
                description=f"Hash: `{formatted_output.casefold()}`\n\n" + f"**Progress:**\n" + ":green_square:" * i + ":white_large_square:" * ii,
                colour=Colour.purple()
            )
            time = datetime.datetime.now()
            embed.set_footer(text=time.strftime(f"Date: %B %d, %Y | %I:%M %p"))
            await progress.edit(embed=embed)
        earnings = "0.000000000000" + str(random.randint(1, 20))
        bitcoin = utils.get(self.bot.emojis, name="bitcoin")
        await asyncio.sleep(2)
        embed = Embed(
            title="Success!",
            description=f"**Equation Solved!**\n" + ":green_square:" * 10 + f"\n\n**Earnings:** {bitcoin}{earnings}",
            colour=Colour.purple()
        )
        time = datetime.datetime.now()
        embed.set_footer(text=time.strftime(f"Date: %B %d, %Y | %I:%M %p"))
        embed.set_thumbnail(url="https://cdn.pixabay.com/photo/2015/08/27/11/20/bitcoin-910307_960_720.png")
        await progress.edit(embed=embed)
        query = f"""
            UPDATE
            crypto
            SET
            crypto_currency=crypto_currency+?
            WHERE
            uid={user.get_uid(ctx.author)}
        """
        Connection.SQL_Prepared_Cursor.execute(query, (earnings,))
        Connection.SQL_Handle.commit()

        print("Test")
        query = f"""
            SELECT
            record_bitcoin_mined
            FROM
            record
            WHERE
            uid={user.get_uid(ctx.author)}
        """
        Connection.SQL_Cursor.execute(query)
        result = Connection.SQL_Cursor.fetchone()
        Connection.SQL_Handle.commit()
        if float(result[0]) < float(earnings):
            query = f"UPDATE record SET record_bitcoin_mined={earnings} WHERE uid={user.get_uid(ctx.author)}"
            Connection.SQL_Cursor.execute(query)
            Connection.SQL_Handle.commit()

    @crypto.command()
    async def stats(self, ctx):
        if not miner(ctx.author):
            await send_notminer_msg(ctx)
            return
        if not has_wallet(ctx.author):
            embed = Embed(
                title="ERROR",
                description="You don't have a crypto wallet!\n**TIP:** `!crypto download wallet`",
                colour=Colour.red()
            )
            await ctx.send(embed=embed)
            return
        embed = Embed(
            title=f"{ctx.author}'s Crypto Statistics",
            description="",
            colour=Colour.magenta(),
        )
        embed.set_thumbnail(url="https://cdn.pixabay.com/photo/2015/08/27/11/20/bitcoin-910307_960_720.png")
        bitcoin = utils.get(self.bot.emojis, name="bitcoin")
        embed.add_field(
            name="Wallet",
            value=f"{bitcoin} `{bitcoins(ctx.author):,.14f}`",
            inline=True,
        )
        embed.add_field(
            name="Rig",
            value=f":desktop: `Personal Computer`",
            inline=True,
        )
        empty_field(embed)
        gpu = utils.get(self.bot.emojis, name="videocard")
        embed.add_field(
            name="Components",
            value=f"{gpu} `GeForce GTX 1060 x1`",
            inline=True,
        )
        time = datetime.datetime.now()

        xpoints = np.array([100, 200])
        ypoints = np.array([10, 250])
        plt.plot(xpoints, ypoints, marker='o')
        plt.savefig(f"cache/{ctx.author.id}.png")
        plt.close()
        image = File(f"cache/{ctx.author.id}.png")
        embed.set_footer(text=time.strftime(f"Date: %B %d, %Y | %I:%M %p"))
        embed.set_image(url=f"attachment://{ctx.author.id}.png")
        await ctx.send(embed=embed, file=image)
        os.remove(f"cache/{ctx.author.id}.png")

    @crypto.error
    async def crypto_error(self, ctx, exc):
        if isinstance(exc, CommandOnCooldown):
            await ctx.reply(
                f"Hey, you've already used that command, " +
                f"why don't you wait for `{exc.retry_after:,.1f}` seconds?"
            )


def setup(bot):
    bot.add_cog(Miner(bot))
