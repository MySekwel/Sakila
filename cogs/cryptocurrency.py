import asyncio

from discord import Embed, Colour
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType, CommandOnCooldown

from cogs import user
from main import Connection
from utils import emoji_dictionary as emojii


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
    return int(result[0])


def has_wallet(_user):
    query = f"SELECT crypto_wallet FROM crypto WHERE uid={user.get_uid(_user)}"
    Connection.SQL_Cursor.execute(query)
    result = Connection.SQL_Cursor.fetchone()
    Connection.SQL_Handle.commit()
    return int(result[0])


async def send_notminer_msg(message):
    embed = Embed(
        title="ERROR",
        description="You are not a miner!\n**TIP:** `!crypto market buy rig`",
        colour=Colour.red()
    )
    await message.channel.trigger_typing()
    await asyncio.sleep(2)
    await message.send(embed=embed)


class Miner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @cooldown(1, 5, BucketType.user)
    async def crypto(self, ctx, action, action2="None", action3="None"):
        if not user.registered(ctx.author.id):
            await user.send_notregistered_msg(ctx)
            return
        if action == "market":
            if not user.registered(ctx.author.id):
                await user.send_notregistered_msg(ctx)
                return
            if action2 == "buy":
                if action3 == "rig":
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
        if action == "download":
            print("Test")
            if action2 == "wallet":
                print("Test")
                print(user.get_uid(ctx.author))
                if has_wallet(ctx.author):
                    embed = Embed(
                        title="ERROR",
                        description="You already have a crypto wallet!",
                        colour=Colour.red()
                    )
                    await ctx.send(embed=embed)
                    return
                print("Test")
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
                print("Test")
                await ctx.channel.trigger_typing()
                await asyncio.sleep(2)
                embed = Embed(
                    title="Downloading Crypto Wallet",
                    description="**Progress:**\n" + ":white_large_square:" * 10,
                    colour=Colour.magenta()
                )
                progress = await ctx.send(embed=embed)
                ii = 11
                for i in range(10):
                    ii -= 1
                    await asyncio.sleep(1)
                    embed = Embed(
                        title="Downloading Crypto Wallet",
                        description=("**Progress:**\n" + ":green_square:" * i) + ":white_large_square:" * ii,
                        colour=Colour.magenta()
                    )
                    await progress.edit(embed=embed)
                await asyncio.sleep(1)
                embed = Embed(
                    title="Success!",
                    description="Crypto Wallet has been downloaded to your rig.\n\n**Progress:**\n" + "" + ":green_square:" * 10,
                    colour=Colour.magenta()
                )
                await progress.edit(embed=embed)

            if action2 == "sell":
                pass
        if action == "mine":
            if not miner(ctx.author):
                await send_notminer_msg(ctx)
                return
        if action == "stats":
            if not miner(ctx.author):
                await send_notminer_msg(ctx)
                return
        if action == "upgrade":
            if not miner(ctx.author):
                await send_notminer_msg(ctx)
                return
        if action == "company":
            if not miner(ctx.author):
                await send_notminer_msg(ctx)
                return

    @crypto.error
    async def crypto_error(self, ctx, exc):
        if isinstance(exc, CommandOnCooldown):
            await ctx.reply(
                f"Hey, you've already seen your stats, " +
                f"why don't you wait for `{exc.retry_after:,.1f}` seconds?"
            )


def setup(bot):
    bot.add_cog(Miner(bot))
