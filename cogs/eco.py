from discord import Embed, Colour, utils
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown, CommandOnCooldown
import main
import settings


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Command: Buy
    # Description: Buy command for user shop
    # Cooldown: 5 Seconds
    @commands.command()
    @cooldown(1, 5, BucketType.user)
    async def buy(self, ctx, item=0):
        query = f"""
            SELECT
            *
            FROM
            users
            WHERE
            user_id={ctx.author.id}
        """
        main.SQL_Cursor.execute(query)
        result = main.SQL_Cursor.fetchone()
        main.SQL_Handle.commit()
        cash = result[4]
        if not result:
            await ctx.send("**You are not registered to the database!**")
            await ctx.send("TIP: `!register`")
            return
        query = f"""
            SELECT
            uid
            FROM
            users
            WHERE
            user_id={ctx.author.id}
        """
        main.SQL_Cursor.execute(query)
        result = main.SQL_Cursor.fetchone()
        main.SQL_Handle.commit()
        userid = result[0]
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
        main.SQL_Cursor.execute(query)
        result = main.SQL_Cursor.fetchone()
        main.SQL_Handle.commit()
        # - Item Variable Declaration
        # Store fetched data from the query
        item_pickaxe = result[0]
        item_drill = result[1]
        item_jackhammer = result[2]
        item_metal_detector = result[3]
        item_gold_detector = result[4]
        item_diamond_detector = result[5]
        item_minecart = result[6]
        item_minetransport = result[7]
        item_transportplane = result[8]
        # - Item checks
        # No input
        if int(item) == 0:
            await ctx.send("USAGE: !buy [item id]")
        # Item: Pickaxe
        # Price: 500
        # Description: %5 Work Salary Bonus
        if int(item) == 1:
            if item_pickaxe >= 1:
                await ctx.send("ERROR: You already have this item!")
                return
            if int(cash) < settings.PRICE_PICKAXE:
                await ctx.send("ERROR: You don't have any money bud, try working in the mines [!work]")
                return
            query = f"""
                UPDATE
                inventory
                SET
                item_pickaxe=?
                WHERE
                uid={userid}
            """
            main.SQL_Prepared_Cursor.execute(query, (1,))
            main.SQL_Handle.commit()

            query = f"""
                UPDATE
                users
                SET
                user_cash=user_cash-?
                WHERE
                user_id={ctx.author.id}
            """
            main.SQL_Prepared_Cursor.execute(query, (settings.PRICE_PICKAXE,))
            main.SQL_Handle.commit()

            await ctx.send(f"You have bought a `pickaxe` for ${settings.PRICE_PICKAXE}!")
        # Item: Drill
        # Price: 2500
        # Description: %10 Work Salary Bonus
        elif int(item) == 2:
            if item_drill >= 1:
                await ctx.send("ERROR: You already have this item!")
                return
            if int(cash) < settings.PRICE_DRILL:
                await ctx.send("ERROR: You don't have any money bud, try working in the mines [!work]")
                return
            query = f"""
                UPDATE
                inventory
                SET
                item_drill=?
                WHERE
                uid={userid}
            """
            main.SQL_Prepared_Cursor.execute(query, (1,))
            main.SQL_Handle.commit()

            query = f"""
                UPDATE
                users
                SET
                user_cash=user_cash-?
                WHERE
                user_id={ctx.author.id}
            """
            main.SQL_Prepared_Cursor.execute(query, (settings.PRICE_DRILL,))
            main.SQL_Handle.commit()

            await ctx.send(f"You have bought a `drill` for ${settings.PRICE_DRILL}!")
        # Item: Jackhammer
        # Price: 5000
        # Description: %25 Work Salary Bonus
        elif int(item) == 3:
            if item_jackhammer >= 1:
                await ctx.send("ERROR: You already have this item!")
                return
            if int(cash) < settings.PRICE_JACKHAMMER:
                await ctx.send("ERROR: You don't have any money bud, try working in the mines [!work]")
                return
            query = f"""
                UPDATE
                inventory
                SET
                item_jackhammer=?
                WHERE
                uid={userid}
            """
            main.SQL_Prepared_Cursor.execute(query, (1,))
            main.SQL_Handle.commit()

            query = f"""
                UPDATE
                users
                SET
                user_cash=user_cash-?
                WHERE
                user_id={ctx.author.id}
            """
            main.SQL_Prepared_Cursor.execute(query, (settings.PRICE_JACKHAMMER,))
            main.SQL_Handle.commit()

            await ctx.send(f"You have bought a `jackhammer` for ${settings.PRICE_JACKHAMMER}!")
        # Item: Metal Detector
        # Price: 7500
        # Description: %35 Work Salary Bonus
        elif int(item) == 4:
            if item_metal_detector >= 1:
                await ctx.send("ERROR: You already have this item!")
                return
            if int(cash) < settings.PRICE_METALDETECTOR:
                await ctx.send("ERROR: You don't have any money bud, try working in the mines [!work]")
                return
            query = f"""
                UPDATE
                inventory
                SET
                item_metal_detector=?
                WHERE
                uid={userid}
            """
            main.SQL_Prepared_Cursor.execute(query, (1,))
            main.SQL_Handle.commit()

            query = f"""
                UPDATE
                users
                SET
                user_cash=user_cash-?
                WHERE
                user_id={ctx.author.id}
            """
            main.SQL_Prepared_Cursor.execute(query, (settings.PRICE_METALDETECTOR,))
            main.SQL_Handle.commit()

            await ctx.send(f"You have bought a `metal detector` for ${settings.PRICE_METALDETECTOR}!")
        # Item: Gold Detector
        # Price: 15000
        # Description: %50 Work Salary Bonus
        elif int(item) == 5:
            if item_gold_detector >= 1:
                await ctx.send("ERROR: You already have this item!")
                return
            if int(cash) < settings.PRICE_GOLDDETECTOR:
                await ctx.send("ERROR: You don't have any money bud, try working in the mines [!work]")
                return
            query = f"""
                UPDATE
                inventory
                SET
                item_gold_detector=?
                WHERE
                uid={userid}
            """
            main.SQL_Prepared_Cursor.execute(query, (1,))
            main.SQL_Handle.commit()

            query = f"""
                UPDATE
                users
                SET
                user_cash=user_cash-?
                WHERE
                user_id={ctx.author.id}
            """
            main.SQL_Prepared_Cursor.execute(query, (settings.PRICE_GOLDDETECTOR,))
            main.SQL_Handle.commit()

            await ctx.send(f"You have bought a `gold detector` for ${settings.PRICE_GOLDDETECTOR}!")
        # Item: Diamond Detector
        # Price: 25000
        # Description: %75 Work Salary Bonus
        elif int(item) == 6:
            if item_diamond_detector >= 1:
                await ctx.send("ERROR: You already have this item!")
                return
            if int(cash) < settings.PRICE_DIAMONDDETECTOR:
                await ctx.send("ERROR: You don't have any money bud, try working in the mines [!work]")
                return
            query = f"""
                UPDATE
                inventory
                SET
                item_diamond_detector=?
                WHERE
                uid={userid}
            """
            main.SQL_Prepared_Cursor.execute(query, (1,))
            main.SQL_Handle.commit()

            query = f"""
                UPDATE
                users
                SET
                user_cash=user_cash-?
                WHERE
                user_id={ctx.author.id}
            """
            main.SQL_Prepared_Cursor.execute(query, (settings.PRICE_DIAMONDDETECTOR,))
            main.SQL_Handle.commit()

            await ctx.send(f"You have bought a `diamond detector` for ${settings.PRICE_DIAMONDDETECTOR}!")
        # Item: Mine Cart
        # Price: 35000
        # Description: -%10 Work Cooldown
        elif int(item) == 7:
            if item_minecart >= 1:
                await ctx.send("ERROR: You already have this item!")
                return
            if int(cash) < settings.PRICE_MINECART:
                await ctx.send("ERROR: You don't have any money bud, try working in the mines [!work]")
                return
            query = f"""
                UPDATE
                inventory
                SET
                item_minecart=?
                WHERE
                uid={userid}
            """
            main.SQL_Prepared_Cursor.execute(query, (1,))
            main.SQL_Handle.commit()

            query = f"""
                UPDATE
                users
                SET
                user_cash=user_cash-?
                WHERE
                user_id={ctx.author.id}
            """
            main.SQL_Prepared_Cursor.execute(query, (settings.PRICE_MINECART,))
            main.SQL_Handle.commit()

            await ctx.send(f"You have bought a `minecart` for ${settings.PRICE_MINECART}!")
        # Item: Mine Transport
        # Price: 55000
        # Description: -%25 Work Cooldown
        elif int(item) == 8:
            if item_minetransport >= 1:
                await ctx.send("ERROR: You already have this item!")
                return
            if int(cash) < settings.PRICE_MINETRANSPORT:
                await ctx.send("ERROR: You don't have any money bud, try working in the mines [!work]")
                return
            query = f"""
                UPDATE
                inventory
                SET
                item_minetransport=?
                WHERE
                uid={userid}
            """
            main.SQL_Prepared_Cursor.execute(query, (1,))
            main.SQL_Handle.commit()

            query = f"""
                UPDATE
                users
                SET
                user_cash=user_cash-?
                WHERE
                user_id={ctx.author.id}
            """
            main.SQL_Prepared_Cursor.execute(query, (settings.PRICE_MINETRANSPORT,))
            main.SQL_Handle.commit()

            await ctx.send(f"You have bought a `mine transport` for ${settings.PRICE_MINETRANSPORT}!")
        # Item: Transport Plane
        # Price: 150000
        # Description: -%50 Work Cooldown
        elif int(item) == 9:
            if item_transportplane >= 1:
                await ctx.send("ERROR: You already have this item!")
                return
            if int(cash) < settings.PRICE_TRANSPORTPLANE:
                await ctx.send("ERROR: You don't have any money bud, try working in the mines [!work]")
                return
            query = f"""
                UPDATE
                inventory
                SET
                item_transportplane=?
                WHERE
                uid={userid}
            """
            main.SQL_Prepared_Cursor.execute(query, (1,))
            main.SQL_Handle.commit()

            query = f"""
                UPDATE
                users
                SET
                user_cash=user_cash-?
                WHERE
                user_id={ctx.author.id}
            """
            main.SQL_Prepared_Cursor.execute(query, (settings.PRICE_TRANSPORTPLANE,))
            main.SQL_Handle.commit()

            await ctx.send(f"You have bought a `transport plane` for ${settings.PRICE_TRANSPORTPLANE}!")

    # Command: Shop
    # Description: Show user shop
    # Cooldown: 5 Seconds
    @commands.command()
    @cooldown(1, 5, BucketType.user)
    async def shop(self, ctx):
        query = f"""
            SELECT
            *
            FROM
            users
            WHERE
            user_id={ctx.author.id}
        """
        main.SQL_Cursor.execute(query)
        result = main.SQL_Cursor.fetchone()
        main.SQL_Handle.commit()
        if not result:
            await ctx.send("**You are not registered to the database!**")
            await ctx.send("TIP: `!register`")
            return

        embed = Embed(
            title='User Shop',
            description='Buy useful items and boosters!',
            colour=Colour.dark_gold()
        )
        embed.set_thumbnail(url='https://i.pinimg.com/originals/77/c3/66/77c366436d8bd35fe8b3ce5b8c66992e.png')
        embed.add_field(
            name='1. Pickaxe :pick:',
            value=f'`Price: ${settings.PRICE_PICKAXE}` | `Bonus: 5% Work Salary`',
            inline=True
        )
        drill = utils.get(self.bot.emojis, name='drill')
        embed.add_field(
            name=f'2. Drill {str(drill)}',
            value=f'`Price: ${settings.PRICE_DRILL}` | `Bonus: 10% Work Salary`',
            inline=True
        )
        jackhammer = utils.get(self.bot.emojis, name='jackhammer')
        embed.add_field(
            name=f'3. Jackhammer {str(jackhammer)}',
            value=f'`Price: ${settings.PRICE_JACKHAMMER}` | `Bonus: 25% Work Salary`',
            inline=True
        )
        metal_detector = utils.get(self.bot.emojis, name='metal_detector')
        embed.add_field(
            name=f'4. Metal Detector {str(metal_detector)}',
            value=f'`Price: ${settings.PRICE_METALDETECTOR}` | `Bonus: 35% Work Salary`',
            inline=True
        )
        gold_detector = utils.get(self.bot.emojis, name='metal_detector')
        embed.add_field(
            name=f'5. Gold Detector {str(gold_detector)}',
            value=f'`Price: ${settings.PRICE_GOLDDETECTOR}` | `Bonus: 50% Work Salary`',
            inline=True
        )
        diamond_detector = utils.get(self.bot.emojis, name='metal_detector')
        embed.add_field(
            name=f'6. Diamond Detector {str(diamond_detector)}',
            value=f'`Price: ${settings.PRICE_DIAMONDDETECTOR}` | `Bonus: 75% Work Salary`',
            inline=True
        )
        minecart = utils.get(self.bot.emojis, name='minecart')
        embed.add_field(
            name=f'7. Minecart {str(minecart)}',
            value=f'`Price: ${settings.PRICE_MINECART}` | `Bonus: -10% Work Cooldown`',
            inline=True
        )
        minetransport = utils.get(self.bot.emojis, name='minetransport')
        embed.add_field(
            name=f'8. Mine Transport {str(minetransport)}',
            value=f'`Price: ${settings.PRICE_MINETRANSPORT}` | `Bonus: -25% Work Cooldown`',
            inline=True
        )
        embed.add_field(
            name='9. Transport Plane :airplane:',
            value=f'`Price: ${settings.PRICE_TRANSPORTPLANE}` | `Bonus: -50% Work Cooldown`',
            inline=True
        )
        embed.add_field(
            name='How to Buy?',
            value='To buy, use the command `!buy [item number]`.',
            inline=False
        )
        await ctx.send(embed=embed)

    @buy.error
    async def buy_error(self, ctx, exc):
        if isinstance(exc, CommandOnCooldown):
            await ctx.send(
                f"Hey <@!{ctx.author.id}> be chill on buying stuffs bro," +
                f" why don't you wait for `{exc.retry_after:,.1f}` seconds?"
            )


def setup(bot):
    bot.add_cog(Economy(bot))
