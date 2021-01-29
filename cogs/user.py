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


def registered(user):
    query = f"""
        SELECT
        *
        FROM
        users
        WHERE
        uid={user.get_user_uid(user)}
    """
    Connection.SQL_Cursor.execute(query)
    result = Connection.SQL_Cursor.fetchone()
    Connection.SQL_Handle.commit()
    return result


def get_user_uid(user):
    query = f"""
        SELECT
        uid
        FROM
        users
        WHERE
        user_id={user.id}
    """
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
            user_cash,
            user_bank,
            user_exp,
            user_reputation,
            user_love,
            user_vip
            FROM
            users
            WHERE
            uid={get_user_uid(ctx.author)}
        """
        Connection.SQL_Cursor.execute(query)
        result = Connection.SQL_Cursor.fetchone()
        Connection.SQL_Handle.commit()
        stat = {
            "cash": result[0],
            "bank": result[1],
            "exp": result[2],
            "reputation": result[3],
            "love": result[4],
            "vip": result[5],
        }

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
            value=f":moneybag: `{stat['cash']}`",
            inline=True
        )
        embed.add_field(
            name="Bank",
            value=f":bank: `{stat['bank']}`",
            inline=True
        )
        embed.add_field(
            name="Exp",
            value=f":military_medal: `{stat['exp']}`",
            inline=True
        )
        embed.add_field(
            name="Reputation",
            value=f":rosette: `{stat['reputation']}`",
            inline=True
        )
        embed.add_field(
            name="Love",
            value=f":heart: `{stat['love']}`",
            inline=True
        )
        embed.add_field(
            name="VIP Package",
            value=f":crown: `{stat['vip']}`",
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
        query = f"""
            SELECT
            user_cash,
            user_bank
            FROM
            users
            WHERE
            uid={get_user_uid(ctx.author)}
        """
        Connection.SQL_Cursor.execute(query)
        result = Connection.SQL_Cursor.fetchone()
        Connection.SQL_Handle.commit()
        embed = Embed(
            title=f"{ctx.author}'s Balance:",
            description=f"**Cash:** :moneybag:`${result[0]}`\n**Bank:** :bank:`${result[1]}`",
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
            item_transportplane,
            metal_metal,
            metal_gold,
            metal_diamond
            FROM
            inventory
            WHERE
            uid={get_user_uid(ctx.author)}
        """
        Connection.SQL_Cursor.execute(query)
        result = Connection.SQL_Cursor.fetchone()
        Connection.SQL_Handle.commit()

        item_name = {
            "pickaxe": result[0],
            "drill": result[1],
            "jackhammer": result[2],
            "metal_detector": result[3],
            "gold_detector": result[4],
            "diamond_detector": result[5],
            "minecart": result[6],
            "minetransport": result[7],
            "transportplane": result[8],
            "metal": result[9],
            "gold": result[10],
            "diamond": result[11]
        }

        embed = Embed(
            title="User Stats",
            description=f"**{ctx.author.name}'s Inventory**",
            colour=Colour.green()
        )
        embed.set_thumbnail(
            url="https://images.emojiterra.com/mozilla/512px/1f392.png"
        )
        slot = 1
        if item_name["pickaxe"]:
            embed.add_field(
                name=f"{slot}. Pickaxe",
                value=f":pick: `{item_name['pickaxe']}`",
                inline=False
            )
            slot += 1
        if item_name["drill"]:
            emoji_drill = utils.get(self.bot.emojis, name="drill")
            embed.add_field(
                name=f"{slot}. Drill",
                value=f"{str(emoji_drill)} `{item_name['drill']}`",
                inline=False
            )
            slot += 1
        if item_name["jackhammer"]:
            emoji_jackhammer = utils.get(self.bot.emojis, name="jackhammer")
            embed.add_field(
                name=f"{slot}. Jackhammer",
                value=f"{str(emoji_jackhammer)} `{item_name['jackhammer']}`",
                inline=False
            )
            slot += 1
        if item_name["metal_detector"]:
            emoji_jackhammer = utils.get(self.bot.emojis, name="metal_detector")
            embed.add_field(
                name=f"{slot}. Metal Detector",
                value=f"{str(emoji_jackhammer)} `{item_name['metal_detector']}`",
                inline=False
            )
            slot += 1
        if item_name["gold_detector"]:
            emoji_jackhammer = utils.get(self.bot.emojis, name="metal_detector")
            embed.add_field(
                name=f"{slot}. Gold Detector",
                value=f"{str(emoji_jackhammer)} `{item_name['gold_detector']}`",
                inline=False
            )
            slot += 1
        if item_name["diamond_detector"]:
            emoji_jackhammer = utils.get(self.bot.emojis, name="metal_detector")
            embed.add_field(
                name=f"{slot}. Diamond Detector",
                value=f"{str(emoji_jackhammer)} `{item_name['diamond_detector']}`",
                inline=False
            )
            slot += 1
        if item_name["minecart"]:
            emoji_jackhammer = utils.get(self.bot.emojis, name="minecart")
            embed.add_field(
                name=f"{slot}. Mine Cart",
                value=f"{str(emoji_jackhammer)} `{item_name['minecart']}`",
                inline=False
            )
            slot += 1
        if item_name["minetransport"]:
            emoji_jackhammer = utils.get(self.bot.emojis, name="minetransport")
            embed.add_field(
                name=f"{slot}. Mine Transport",
                value=f"{str(emoji_jackhammer)} `{item_name['minetransport']}`",
                inline=False
            )
            slot += 1
        if item_name["transportplane"]:
            emoji_jackhammer = utils.get(self.bot.emojis, name="transportplane")
            embed.add_field(
                name=f"{slot}. Transport Plane",
                value=f"{str(emoji_jackhammer)} `{item_name['transportplane']}`",
                inline=False
            )
            slot += 1
        if item_name["metal"]:
            embed.add_field(
                name=f"{slot}. Metal",
                value=f":gear: `{item_name['metal']}`",
                inline=False
            )
            slot += 1
        if item_name["gold"]:
            embed.add_field(
                name=f"{slot}. Gold",
                value=f":coin: `{item_name['gold']}`",
                inline=False
            )
            slot += 1
        if item_name["diamond"]:
            embed.add_field(
                name=f"{slot}. Diamond",
                value=f":large_blue_diamond: `{item_name['diamond']}`",
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
