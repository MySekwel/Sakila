"""
Module: ./cogs/user.py
Description: User module, includes everything that has relation to user information.
Module Dependencies:
    > discord.Colour
    > discord.Embed
    > discord.utils
    > discord.exit.commands.BucketType
    > discord.ext.commands.cooldown
    > discord.ext.commands.CommandOnCooldown
"""
import asyncio
import datetime

from discord import Colour, Embed, utils
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown, CommandOnCooldown

from main import Connection


def registered(userid):
    query = f"SELECT * FROM users WHERE user_id={userid}"
    Connection.SQL_Cursor.execute(query)
    result = Connection.SQL_Cursor.fetchone()
    Connection.SQL_Handle.commit()
    return result


def get_uid(user):
    query = f"SELECT uid FROM users WHERE user_id={user.id}"
    Connection.SQL_Cursor.execute(query)
    result = Connection.SQL_Cursor.fetchone()
    Connection.SQL_Handle.commit()
    return result[0]


def get_cash(user):
    query = f"SELECT user_cash FROM users WHERE uid={get_uid(user)}"
    Connection.SQL_Cursor.execute(query)
    result = Connection.SQL_Cursor.fetchone()
    Connection.SQL_Handle.commit()
    return result[0]


def get_bank(user):
    query = f"SELECT user_bank FROM users WHERE uid={get_uid(user)}"
    Connection.SQL_Cursor.execute(query)
    result = Connection.SQL_Cursor.fetchone()
    Connection.SQL_Handle.commit()
    return result[0]


def get_exp(user):
    query = f"SELECT user_exp FROM users WHERE uid={get_uid(user)}"
    Connection.SQL_Cursor.execute(query)
    result = Connection.SQL_Cursor.fetchone()
    Connection.SQL_Handle.commit()
    return result[0]


def get_reputation(user):
    query = f"SELECT user_reputation FROM users WHERE uid={get_uid(user)}"
    Connection.SQL_Cursor.execute(query)
    result = Connection.SQL_Cursor.fetchone()
    Connection.SQL_Handle.commit()
    return result[0]


def get_vip(user):
    query = f"SELECT user_vip FROM users WHERE uid={get_uid(user)}"
    Connection.SQL_Cursor.execute(query)
    result = Connection.SQL_Cursor.fetchone()
    Connection.SQL_Handle.commit()
    return result[0]


def get_love(user):
    query = f"SELECT user_love FROM users WHERE uid={get_uid(user)}"
    Connection.SQL_Cursor.execute(query)
    result = Connection.SQL_Cursor.fetchone()
    Connection.SQL_Handle.commit()
    return result[0]


def has_pickaxe(user):
    query = f"SELECT tool_pickaxe FROM equipment WHERE uid={get_uid(user)}"
    Connection.SQL_Cursor.execute(query)
    result = Connection.SQL_Cursor.fetchone()
    Connection.SQL_Handle.commit()
    return result[0]


def has_drill(user):
    query = f"SELECT tool_drill FROM equipment WHERE uid={get_uid(user)}"
    Connection.SQL_Cursor.execute(query)
    result = Connection.SQL_Cursor.fetchone()
    Connection.SQL_Handle.commit()
    return result[0]


def has_jackhammer(user):
    query = f"SELECT tool_jackhammer FROM equipment WHERE uid={get_uid(user)}"
    Connection.SQL_Cursor.execute(query)
    result = Connection.SQL_Cursor.fetchone()
    Connection.SQL_Handle.commit()
    return result[0]


def has_metaldetector(user):
    query = f"SELECT tool_metal_detector FROM equipment WHERE uid={get_uid(user)}"
    Connection.SQL_Cursor.execute(query)
    result = Connection.SQL_Cursor.fetchone()
    Connection.SQL_Handle.commit()
    return result[0]


def has_golddetector(user):
    query = f"SELECT tool_gold_detector FROM equipment WHERE uid={get_uid(user)}"
    Connection.SQL_Cursor.execute(query)
    result = Connection.SQL_Cursor.fetchone()
    Connection.SQL_Handle.commit()
    return result[0]


def has_diamonddetector(user):
    query = f"SELECT tool_diamond_detector FROM equipment WHERE uid={get_uid(user)}"
    Connection.SQL_Cursor.execute(query)
    result = Connection.SQL_Cursor.fetchone()
    Connection.SQL_Handle.commit()
    return result[0]


def has_minecart(user):
    query = f"SELECT tool_minecart FROM equipment WHERE uid={get_uid(user)}"
    Connection.SQL_Cursor.execute(query)
    result = Connection.SQL_Cursor.fetchone()
    Connection.SQL_Handle.commit()
    return result[0]


def has_minetransport(user):
    query = f"SELECT tool_minetransport FROM equipment WHERE uid={get_uid(user)}"
    Connection.SQL_Cursor.execute(query)
    result = Connection.SQL_Cursor.fetchone()
    Connection.SQL_Handle.commit()
    return result[0]


def has_transportplane(user):
    query = f"SELECT tool_transportplane FROM equipment WHERE uid={get_uid(user)}"
    Connection.SQL_Cursor.execute(query)
    result = Connection.SQL_Cursor.fetchone()
    Connection.SQL_Handle.commit()
    return result[0]


def metal(user):
    query = f"SELECT item_metal FROM inventory WHERE uid={get_uid(user)}"
    Connection.SQL_Cursor.execute(query)
    result = Connection.SQL_Cursor.fetchone()
    Connection.SQL_Handle.commit()
    return result[0]


def gold(user):
    query = f"SELECT item_gold FROM inventory WHERE uid={get_uid(user)}"
    Connection.SQL_Cursor.execute(query)
    result = Connection.SQL_Cursor.fetchone()
    Connection.SQL_Handle.commit()
    return result[0]


def diamond(user):
    query = f"SELECT item_diamond FROM inventory WHERE uid={get_uid(user)}"
    Connection.SQL_Cursor.execute(query)
    result = Connection.SQL_Cursor.fetchone()
    Connection.SQL_Handle.commit()
    return result[0]


class User(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Command: Stats
    # Description: Show user stats
    # Cooldown: 10 Seconds
    @commands.command()
    @cooldown(1, 10, BucketType.user)
    async def stats(self, ctx):
        print("Test")
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
        print("Test")

        embed = Embed(
            title="User Stats",
            description=f"**{ctx.author.name}'s Stats**",
            colour=Colour.green()
        )
        embed.set_thumbnail(
            url=ctx.author.avatar_url
        )
        embed.add_field(
            name="Balance",
            value=f":moneybag: `{get_cash(ctx.author)}`",
            inline=True
        )
        embed.add_field(
            name="Bank",
            value=f":bank: `{get_bank(ctx.author)}`",
            inline=True
        )
        embed.add_field(
            name="Exp",
            value=f":military_medal: `{get_exp(ctx.author)}`",
            inline=True
        )
        embed.add_field(
            name="Reputation",
            value=f":rosette: `{get_reputation(ctx.author)}`",
            inline=True
        )
        embed.add_field(
            name="Love",
            value=f":heart: `{get_love(ctx.author)}`",
            inline=True
        )
        embed.add_field(
            name="VIP Package",
            value=f":crown: `{get_vip(ctx.author)}`",
            inline=True
        )
        await ctx.channel.trigger_typing()
        await asyncio.sleep(2)

        time = datetime.datetime.now()
        embed.set_footer(text=time.strftime(f"As of %B %d, %Y | %I:%M %p"))
        await ctx.send(embed=embed)

    @commands.command()
    @cooldown(1, 10, BucketType.user)
    async def bal(self, ctx):
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
        embed = Embed(
            title=f"{ctx.author}'s Balance:",
            description=f"**Cash:** :moneybag:`${get_cash(ctx.author)}`\n**Bank:** :bank:`${get_bank(ctx.author)}`",
            colour=Colour.gold()
        )
        embed.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.channel.trigger_typing()
        await asyncio.sleep(2)

        time = datetime.datetime.now()
        embed.set_footer(text=time.strftime(f"As of %B %d, %Y | %I:%M %p"))
        await ctx.send(embed=embed)

    # Command: Inventory
    # Description: Show user inventory
    # Cooldown: 10 Seconds
    @commands.command()
    @cooldown(1, 10, BucketType.user)
    async def inventory(self, ctx):
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

        embed = Embed(
            title="User Stats",
            description=f"**{ctx.author.name}'s Inventory**",
            colour=Colour.green()
        )
        embed.set_thumbnail(
            url="https://images.emojiterra.com/mozilla/512px/1f392.png"
        )
        slot = 1
        if has_pickaxe(ctx.author):
            embed.add_field(
                name=f"{slot}. Pickaxe",
                value=f":pick: `{has_pickaxe(ctx.author)}`",
                inline=False
            )
            slot += 1
        if has_drill(ctx.author):
            emoji_drill = utils.get(self.bot.emojis, name="drill")
            embed.add_field(
                name=f"{slot}. Drill",
                value=f"{str(emoji_drill)} `{has_drill(ctx.author)}`",
                inline=False
            )
            slot += 1
        if has_jackhammer(ctx.author):
            emoji_jackhammer = utils.get(self.bot.emojis, name="jackhammer")
            embed.add_field(
                name=f"{slot}. Jackhammer",
                value=f"{str(emoji_jackhammer)} `{has_jackhammer(ctx.author)}`",
                inline=False
            )
            slot += 1
        if has_metaldetector(ctx.author):
            emoji_jackhammer = utils.get(self.bot.emojis, name="metal_detector")
            embed.add_field(
                name=f"{slot}. Metal Detector",
                value=f"{str(emoji_jackhammer)} `{has_metaldetector(ctx.author)}`",
                inline=False
            )
            slot += 1
        if has_golddetector(ctx.author):
            emoji_jackhammer = utils.get(self.bot.emojis, name="metal_detector")
            embed.add_field(
                name=f"{slot}. Gold Detector",
                value=f"{str(emoji_jackhammer)} `{has_golddetector(ctx.author)}`",
                inline=False
            )
            slot += 1
        if has_diamonddetector(ctx.author):
            emoji_jackhammer = utils.get(self.bot.emojis, name="metal_detector")
            embed.add_field(
                name=f"{slot}. Diamond Detector",
                value=f"{str(emoji_jackhammer)} `{has_diamonddetector(ctx.author)}`",
                inline=False
            )
            slot += 1
        if has_minecart(ctx.author):
            emoji_jackhammer = utils.get(self.bot.emojis, name="minecart")
            embed.add_field(
                name=f"{slot}. Mine Cart",
                value=f"{str(emoji_jackhammer)} `{has_minecart(ctx.author)}`",
                inline=False
            )
            slot += 1
        if has_minetransport(ctx.author):
            emoji_jackhammer = utils.get(self.bot.emojis, name="minetransport")
            embed.add_field(
                name=f"{slot}. Mine Transport",
                value=f"{str(emoji_jackhammer)} `{has_minetransport(ctx.author)}`",
                inline=False
            )
            slot += 1
        if has_transportplane(ctx.author):
            emoji_jackhammer = utils.get(self.bot.emojis, name="transportplane")
            embed.add_field(
                name=f"{slot}. Transport Plane",
                value=f"{str(emoji_jackhammer)} `{has_transportplane(ctx.author)}`",
                inline=False
            )
            slot += 1
        if metal(ctx.author):
            embed.add_field(
                name=f"{slot}. Metal",
                value=f":gear: `{metal(ctx.author)}`",
                inline=False
            )
            slot += 1
        if gold(ctx.author):
            embed.add_field(
                name=f"{slot}. Gold",
                value=f":coin: `{gold(ctx.author)}`",
                inline=False
            )
            slot += 1
        if diamond(ctx.author):
            embed.add_field(
                name=f"{slot}. Diamond",
                value=f":large_blue_diamond: `{diamond(ctx.author)}`",
                inline=False
            )
            slot += 1
        await ctx.channel.trigger_typing()
        await asyncio.sleep(2)
        await ctx.send(f"**{ctx.author.name}'s inventory.**")

        time = datetime.datetime.now()
        embed.set_footer(text=time.strftime(f"As of %B %d, %Y | %I:%M %p"))
        await ctx.send(embed=embed)

    @stats.error
    async def stats_error(self, ctx, exc):
        if isinstance(exc, CommandOnCooldown):
            await ctx.reply(
                f"Hey, you've already seen your stats, " +
                f"why don't you wait for `{exc.retry_after:,.1f}` seconds?"
            )

    @bal.error
    async def stats_error(self, ctx, exc):
        if isinstance(exc, CommandOnCooldown):
            await ctx.reply(
                f"Hmm, your money is going nowhere you have to wait you paranoid human, " +
                f"It's just `{exc.retry_after:,.1f}` seconds you know?"
            )

    @inventory.error
    async def inventory_error(self, ctx, exc):
        if isinstance(exc, CommandOnCooldown):
            await ctx.reply(
                f"Hey, you've already seen your inventory no one will rob you, " +
                f"why don't you wait for `{exc.retry_after:,.1f}` seconds?")


def setup(bot):
    bot.add_cog(User(bot))
