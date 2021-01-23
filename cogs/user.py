from discord import Colour, Embed, utils
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType, CommandOnCooldown
from main import Connection


class User(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Command: Stats
    # Description: Show user stats
    # Cooldown: 5 Seconds
    @commands.command()
    @cooldown(1, 5, BucketType.user)
    async def stats(self, ctx):
        query = f"""
                SELECT
                user_cash,
                user_diamonds,
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
            await ctx.send("**You are not registered to the database!**")
            await ctx.send("TIP: `!register`")
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
            name='Diamonds',
            value=f':large_blue_diamond: `{diamonds}`',
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
            name='VIP Package',
            value=f':crown: `{vip}`',
            inline=True
        )
        embed.add_field(
            name='Love',
            value=f':heart: `{love}`',
            inline=True
        )
        await ctx.send(embed=embed)

    # Command: Inventory
    # Description: Show user inventory
    # Cooldown: 5 Seconds
    @commands.command()
    @cooldown(1, 5, BucketType.user)
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
            await ctx.send("**You are not registered to the database!**")
            await ctx.send("TIP: `!register`")
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
                item_transportplane
                FROM
                inventory
                WHERE
                uid={userid}
            """
        Connection.SQL_Cursor.execute(query)
        result = Connection.SQL_Cursor.fetchone()
        Connection.SQL_Handle.commit()
        if not result:
            await ctx.send("**You are not registered to the database!**")
            await ctx.send("TIP: `!register`")
            return
        await ctx.send(f"**{ctx.author.name}'s stats.**")
        pickaxe = result[0]
        drill = result[1]
        jackhammer = result[2]
        metal_detector = result[3]
        gold_detector = result[4]
        diamond_detector = result[5]
        minecart = result[6]
        minetransport = result[7]
        transportplane = result[8]

        embed = Embed(
            title='User Stats',
            description=f"**{ctx.author.name}'s Stats**",
            colour=Colour.green()
        )
        embed.set_thumbnail(
            url='https://images.emojiterra.com/mozilla/512px/1f392.png'
        )
        embed.add_field(
            name='Pickaxe',
            value=f':pick: `{pickaxe}`',
            inline=True
        )
        emoji_drill = utils.get(self.bot.emojis, name='drill')
        embed.add_field(
            name='Drill',
            value=f'{str(emoji_drill)} `{drill}`',
            inline=True
        )
        emoji_jackhammer = utils.get(self.bot.emojis, name='jackhammer')
        embed.add_field(
            name='Jackhammer',
            value=f'{str(emoji_jackhammer)} `{jackhammer}`',
            inline=True
        )
        emoji_metal_detector = utils.get(self.bot.emojis, name='metal_detector')
        embed.add_field(
            name='Metal Detector',
            value=f'{str(emoji_metal_detector)} `{metal_detector}`',
            inline=True
        )
        emoji_gold_detector = utils.get(self.bot.emojis, name='metal_detector')
        embed.add_field(
            name='Gold Detector',
            value=f'{str(emoji_gold_detector)} `{gold_detector}`',
            inline=True
        )
        emoji_diamond_detector = utils.get(self.bot.emojis, name='metal_detector')
        embed.add_field(
            name='Diamond Detector',
            value=f'{str(emoji_diamond_detector)} `{diamond_detector}`',
            inline=True
        )
        emoji_minecart = utils.get(self.bot.emojis, name='minecart')
        embed.add_field(
            name='Mine Cart',
            value=f'{str(emoji_minecart)} `{minecart}`',
            inline=True
        )
        emoji_minetransport = utils.get(self.bot.emojis, name='minetransport')
        embed.add_field(
            name='Mine Transport',
            value=f'{str(emoji_minetransport)} `{minetransport}`',
            inline=True
        )
        embed.add_field(
            name='Transport Plane',
            value=f':airplane: `{transportplane}`',
            inline=True
        )
        await ctx.send(embed=embed)

    @stats.error
    async def stats_error(self, ctx, exc):
        if isinstance(exc, CommandOnCooldown):
            await ctx.send(
                f"Hey <@!{ctx.author.id}> you've already seen your stats," +
                f"why don't you wait for `{exc.retry_after:,.1f}` seconds?"
            )

    @inventory.error
    async def inventory_error(self, ctx, exc):
        if isinstance(exc, CommandOnCooldown):
            await ctx.send(
                f"Hey <@!{ctx.author.id}> you've already seen your inventory no one will rob you," +
                f"why don't you wait for `{exc.retry_after:,.1f}` seconds?")


def setup(bot):
    bot.add_cog(User(bot))
