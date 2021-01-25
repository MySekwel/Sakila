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

from discord import Colour, Embed, utils
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown, CommandOnCooldown

from main import Connection

slot_item = {
    'pickaxe': 0,
    'drill': 0,
    'jackhammer': 0,
    'metal_detector': 0,
    'gold_detector': 0,
    'diamond_detector': 0,
    'minecart': 0,
    'minetransport': 0,
    'transportplane': 0,
    'metal': 0,
    'gold': 0,
    'diamond': 0,
}


class User(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Command: Stats
    # Description: Show user stats
    # Cooldown: 10 Seconds
    @commands.command()
    @cooldown(1, 10, BucketType.user)
    async def stats(self, ctx):
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
            user_id={ctx.author.id}
        """
        Connection.SQL_Cursor.execute(query)
        result = Connection.SQL_Cursor.fetchone()
        Connection.SQL_Handle.commit()
        if not result:
            embed = Embed(
                title='ERROR',
                description='You are not registered to the database!\n**TIP:** `!register`',
                colour=Colour.red()
            )
            
            await ctx.send(embed=embed)
            return

        await ctx.send(f"**{ctx.author.name}'s stats.**")
        cash = result[0]
        diamonds = result[1]
        exp = result[2]
        reputation = result[3]
        love = result[4]
        vip = result[5]

        embed = Embed(
            title='User Stats',
            description=f"**{ctx.author.name}'s Stats**",
            colour=Colour.green()
        )
        embed.set_thumbnail(
            url='https://webstockreview.net/images/statistics-clipart-transparent-2.png'
        )
        embed.add_field(
            name='Balance',
            value=f':moneybag: `{cash}`',
            inline=True
        )
        embed.add_field(
            name='Bank',
            value=f':bank: `{diamonds}`',
            inline=True
        )
        embed.add_field(
            name='Exp',
            value=f':military_medal: `{exp}`',
            inline=True
        )
        embed.add_field(
            name='Reputation',
            value=f':rosette: `{reputation}`',
            inline=True
        )
        embed.add_field(
            name='Love',
            value=f':heart: `{love}`',
            inline=True
        )
        embed.add_field(
            name='VIP Package',
            value=f':crown: `{vip}`',
            inline=True
        )
        await ctx.send(embed=embed)

    # Command: Inventory
    # Description: Show user inventory
    # Cooldown: 10 Seconds
    @commands.command()
    @cooldown(1, 10, BucketType.user)
    async def inventory(self, ctx):
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
        userid = result[0]

        if not result:
            embed = Embed(
                title='ERROR',
                description='You are not registered to the database!\n**TIP:** `!register`',
                colour=Colour.red()
            )
            
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
            uid={userid}
        """
        Connection.SQL_Cursor.execute(query)
        result = Connection.SQL_Cursor.fetchone()
        Connection.SQL_Handle.commit()

        item_name = {
            'pickaxe': result[0],
            'drill': result[1],
            'jackhammer': result[2],
            'metal_detector': result[3],
            'gold_detector': result[4],
            'diamond_detector': result[5],
            'minecart': result[6],
            'minetransport': result[7],
            'transportplane': result[8],
            'metal': result[9],
            'gold': result[10],
            'diamond': result[11]
        }

        embed = Embed(
            title='User Stats',
            description=f"**{ctx.author.name}'s Inventory**",
            colour=Colour.green()
        )
        embed.set_thumbnail(
            url='https://images.emojiterra.com/mozilla/512px/1f392.png'
        )
        slot = 1
        if item_name['pickaxe']:
            embed.add_field(
                name=f'{slot}. Pickaxe',
                value=f":pick: `{item_name['pickaxe']}`",
                inline=False
            )
            slot += 1
            slot_item['pickaxe'] = slot
        if item_name['drill']:
            emoji_drill = utils.get(self.bot.emojis, name='drill')
            embed.add_field(
                name=f'{slot}. Drill',
                value=f"{str(emoji_drill)} `{item_name['drill']}`",
                inline=False
            )
            slot += 1
            slot_item['drill'] = slot
        if item_name['jackhammer']:
            emoji_jackhammer = utils.get(self.bot.emojis, name='jackhammer')
            embed.add_field(
                name=f'{slot}. Jackhammer',
                value=f"{str(emoji_jackhammer)} `{item_name['jackhammer']}`",
                inline=False
            )
            slot += 1
            slot_item['jackhammer'] = slot
        if item_name['metal_detector']:
            emoji_jackhammer = utils.get(self.bot.emojis, name='metal_detector')
            embed.add_field(
                name=f'{slot}. Metal Detector',
                value=f"{str(emoji_jackhammer)} `{item_name['metal_detector']}`",
                inline=False
            )
            slot += 1
            slot_item['metal_detector'] = slot
        if item_name['gold_detector']:
            emoji_jackhammer = utils.get(self.bot.emojis, name='metal_detector')
            embed.add_field(
                name=f'{slot}. Gold Detector',
                value=f"{str(emoji_jackhammer)} `{item_name['gold_detector']}`",
                inline=False
            )
            slot += 1
            slot_item['gold_detector'] = slot
        if item_name['diamond_detector']:
            emoji_jackhammer = utils.get(self.bot.emojis, name='metal_detector')
            embed.add_field(
                name=f'{slot}. Diamond Detector',
                value=f"{str(emoji_jackhammer)} `{item_name['diamond_detector']}`",
                inline=False
            )
            slot += 1
            slot_item['diamond_detector'] = slot
        if item_name['minecart']:
            emoji_jackhammer = utils.get(self.bot.emojis, name='minecart')
            embed.add_field(
                name=f'{slot}. Mine Cart',
                value=f"{str(emoji_jackhammer)} `{item_name['minecart']}`",
                inline=False
            )
            slot += 1
            slot_item['minecart'] = slot
        if item_name['minetransport']:
            emoji_jackhammer = utils.get(self.bot.emojis, name='minetransport')
            embed.add_field(
                name=f'{slot}. Mine Transport',
                value=f"{str(emoji_jackhammer)} `{item_name['minetransport']}`",
                inline=False
            )
            slot += 1
            slot_item['minetransport'] = slot
        if item_name['transportplane']:
            emoji_jackhammer = utils.get(self.bot.emojis, name='transportplane')
            embed.add_field(
                name=f'{slot}. Transport Plane',
                value=f"{str(emoji_jackhammer)} `{item_name['transportplane']}`",
                inline=False
            )
            slot += 1
            slot_item['transportplane'] = slot
        if item_name['metal']:
            embed.add_field(
                name=f'{slot}. Metal',
                value=f":gear: `{item_name['metal']}`",
                inline=False
            )
            slot += 1
            slot_item['metal'] = slot
        if item_name['gold']:
            embed.add_field(
                name=f'{slot}. Gold',
                value=f":coin: `{item_name['gold']}`",
                inline=False
            )
            slot += 1
            slot_item['gold'] = slot
        if item_name['diamond']:
            embed.add_field(
                name=f'{slot}. Diamond',
                value=f":large_blue_diamond: `{item_name['diamond']}`",
                inline=False
            )
            slot += 1
            slot_item['diamond'] = slot
        await ctx.send(f"**{ctx.author.name}'s inventory.**")
        await ctx.send(embed=embed)

    @stats.error
    async def stats_error(self, ctx, exc):
        if isinstance(exc, CommandOnCooldown):
            await ctx.reply(
                f"Hey, you've already seen your stats, " +
                f"why don't you wait for `{exc.retry_after:,.1f}` seconds?"
            )

    @inventory.error
    async def inventory_error(self, ctx, exc):
        if isinstance(exc, CommandOnCooldown):
            await ctx.reply(
                f"Hey, you've already seen your inventory no one will rob you, " +
                f"why don't you wait for `{exc.retry_after:,.1f}` seconds?")


def setup(bot):
    bot.add_cog(User(bot))
