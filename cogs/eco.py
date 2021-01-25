"""
Module: ./cogs/eco.py
Description: Economy module, includes everything that has relation to the economy system.
Module Dependencies:
    > discord.Embed
    > discord.Colour
    > discord.utils
    > discord.ext.commands.BucketType
    > discord.ext.commands.cooldown
    > discord.ext.commands.CommandOnCooldown
    > utils.settings
"""

from discord import Embed, Colour, utils
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown, CommandOnCooldown

from main import Connection
from utils import settings


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Command: Buy
    # Description: Buy command for user shop
    # Cooldown: 10 Seconds
    @commands.command()
    @cooldown(1, 10, BucketType.user)
    async def buy(self, ctx, item=0):
        query = f"""
            SELECT
            *
            FROM
            users
            WHERE
            user_id={ctx.author.id}
        """
        Connection.SQL_Cursor.execute(query)
        result = Connection.SQL_Cursor.fetchone()
        Connection.SQL_Handle.commit()
        cash = result[4]
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
        # - Item Variable Declaration
        # Store fetched data from the query
        item_name = {
            'pickaxe': result[0],
            'drill': result[1],
            'jackhammer': result[2],
            'metal_detector': result[3],
            'gold_detector': result[4],
            'diamond_detector': result[5],
            'minecart': result[6],
            'minetransport': result[7],
            'transportplane': result[8]
        }

        # Item: Pickaxe
        # Price: 2500
        # Description: %50 Work Salary Bonus
        if int(item) == 1:
            if item_name['pickaxe'] >= 1:
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
            Connection.SQL_Prepared_Cursor.execute(query, (1,))
            Connection.SQL_Handle.commit()

            query = f"""
                UPDATE
                users
                SET
                user_cash=user_cash-?
                WHERE
                user_id={ctx.author.id}
            """
            Connection.SQL_Prepared_Cursor.execute(query, (settings.PRICE_PICKAXE,))
            Connection.SQL_Handle.commit()

            await ctx.send(f"You have bought a `pickaxe` for ${settings.PRICE_PICKAXE}!")
        # Item: Drill
        # Price: 5000
        # Description: %75 Work Salary Bonus
        elif int(item) == 2:
            if item_name['drill'] >= 1:
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
            Connection.SQL_Prepared_Cursor.execute(query, (1,))
            Connection.SQL_Handle.commit()

            query = f"""
                UPDATE
                users
                SET
                user_cash=user_cash-?
                WHERE
                user_id={ctx.author.id}
            """
            Connection.SQL_Prepared_Cursor.execute(query, (settings.PRICE_DRILL,))
            Connection.SQL_Handle.commit()

            await ctx.send(f"You have bought a `drill` for ${settings.PRICE_DRILL}!")
        # Item: Jackhammer
        # Price: 15000
        # Description: %100 Work Salary Bonus
        elif int(item) == 3:
            if item_name['jackhammer'] >= 1:
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
            Connection.SQL_Prepared_Cursor.execute(query, (1,))
            Connection.SQL_Handle.commit()

            query = f"""
                UPDATE
                users
                SET
                user_cash=user_cash-?
                WHERE
                user_id={ctx.author.id}
            """
            Connection.SQL_Prepared_Cursor.execute(query, (settings.PRICE_JACKHAMMER,))
            Connection.SQL_Handle.commit()

            await ctx.send(f"You have bought a `jackhammer` for ${settings.PRICE_JACKHAMMER}!")
        # Item: Metal Detector
        # Price: 7500
        # Description: %10 Chance of getting valuable metals
        elif int(item) == 4:
            if item_name['metal_detector'] >= 1:
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
            Connection.SQL_Prepared_Cursor.execute(query, (1,))
            Connection.SQL_Handle.commit()

            query = f"""
                UPDATE
                users
                SET
                user_cash=user_cash-?
                WHERE
                user_id={ctx.author.id}
            """
            Connection.SQL_Prepared_Cursor.execute(query, (settings.PRICE_METALDETECTOR,))
            Connection.SQL_Handle.commit()

            await ctx.send(f"You have bought a `metal detector` for ${settings.PRICE_METALDETECTOR}!")
        # Item: Gold Detector
        # Price: 15000
        # Description: %20 Chance of getting valuable metals
        elif int(item) == 5:
            if item_name['gold_detector'] >= 1:
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
            Connection.SQL_Prepared_Cursor.execute(query, (1,))
            Connection.SQL_Handle.commit()

            query = f"""
                UPDATE
                users
                SET
                user_cash=user_cash-?
                WHERE
                user_id={ctx.author.id}
            """
            Connection.SQL_Prepared_Cursor.execute(query, (settings.PRICE_GOLDDETECTOR,))
            Connection.SQL_Handle.commit()

            await ctx.send(f"You have bought a `gold detector` for ${settings.PRICE_GOLDDETECTOR}!")
        # Item: Diamond Detector
        # Price: 25000
        # Description: %35 Chance of getting valuable metals / diamonds
        elif int(item) == 6:
            if item_name['diamond_detector'] >= 1:
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
            Connection.SQL_Prepared_Cursor.execute(query, (1,))
            Connection.SQL_Handle.commit()

            query = f"""
                UPDATE
                users
                SET
                user_cash=user_cash-?
                WHERE
                user_id={ctx.author.id}
            """
            Connection.SQL_Prepared_Cursor.execute(query, (settings.PRICE_DIAMONDDETECTOR,))
            Connection.SQL_Handle.commit()

            await ctx.send(f"You have bought a `diamond detector` for ${settings.PRICE_DIAMONDDETECTOR}!")
        # Item: Mine Cart
        # Price: 35000
        # Description: -%10 Work Cooldown
        elif int(item) == 7:
            if item_name['minecart'] >= 1:
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
            Connection.SQL_Prepared_Cursor.execute(query, (1,))
            Connection.SQL_Handle.commit()

            query = f"""
                UPDATE
                users
                SET
                user_cash=user_cash-?
                WHERE
                user_id={ctx.author.id}
            """
            Connection.SQL_Prepared_Cursor.execute(query, (settings.PRICE_MINECART,))
            Connection.SQL_Handle.commit()

            await ctx.send(f"You have bought a `minecart` for ${settings.PRICE_MINECART}!")
        # Item: Mine Transport
        # Price: 55000
        # Description: -%25 Work Cooldown
        elif int(item) == 8:
            if item_name['minetransport'] >= 1:
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
            Connection.SQL_Prepared_Cursor.execute(query, (1,))
            Connection.SQL_Handle.commit()

            query = f"""
                UPDATE
                users
                SET
                user_cash=user_cash-?
                WHERE
                user_id={ctx.author.id}
            """
            Connection.SQL_Prepared_Cursor.execute(query, (settings.PRICE_MINETRANSPORT,))
            Connection.SQL_Handle.commit()

            await ctx.send(f"You have bought a `mine transport` for ${settings.PRICE_MINETRANSPORT}!")
        # Item: Transport Plane
        # Price: 150000
        # Description: -%50 Work Cooldown
        elif int(item) == 9:
            if item_name['transportplane'] >= 1:
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
            Connection.SQL_Prepared_Cursor.execute(query, (1,))
            Connection.SQL_Handle.commit()

            query = f"""
                UPDATE
                users
                SET
                user_cash=user_cash-?
                WHERE
                user_id={ctx.author.id}
            """
            Connection.SQL_Prepared_Cursor.execute(query, (settings.PRICE_TRANSPORTPLANE,))
            Connection.SQL_Handle.commit()

            await ctx.send(f"You have bought a `transport plane` for ${settings.PRICE_TRANSPORTPLANE}!")
        else:
            await ctx.send("USAGE: !buy [item id]")

    @commands.command()
    @cooldown(1, 10, BucketType.user)
    async def sell(self, ctx, item=0):
        query = f"""
            SELECT
            *
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

        item_name = {
            'pickaxe': result[0],
            'drill': result[1],
            'jackhammer': result[2],
            'metal_detector': result[3],
            'gold_detector': result[4],
            'diamond_detector': result[5],
            'minecart': result[6],
            'minetransport': result[7],
            'transportplane': result[8]
        }
        if int(item) == 1:
            if item_name['pickaxe']:
                query = f"""
                    UPDATE
                    users
                    SET
                    user_cash=user_cash+?
                    WHERE
                    uid={userid}
                """
                Connection.SQL_Prepared_Cursor.execute(query, (settings.PRICE_PICKAXE * 0.5,))
                Connection.SQL_Handle.commit()
                query = f"""
                    UPDATE
                    inventory
                    SET
                    item_pickaxe=item_pickaxe-?
                    WHERE
                    uid={userid}
                """
                Connection.SQL_Prepared_Cursor.execute(query, (1,))
                Connection.SQL_Handle.commit()
                embed = Embed(
                    title='Item Sold!',
                    description=f'You have sold your `Pickaxe` for `${settings.PRICE_PICKAXE * 0.5}`\
                     50% of the original price.',
                    colour=Colour.dark_gold()
                )
                await ctx.send(embed=embed)
            else:
                await ctx.send("You do not have a Pickaxe!")

        elif int(item) == 2:
            if item_name['drill']:
                query = f"""
                    UPDATE
                    users
                    SET
                    user_cash=user_cash+?
                    WHERE
                    uid={userid}
                """
                Connection.SQL_Prepared_Cursor.execute(query, (settings.PRICE_DRILL * 0.5,))
                Connection.SQL_Handle.commit()
                query = f"""
                    UPDATE
                    inventory
                    SET
                    item_drill=item_drill-?
                    WHERE
                    uid={userid}
                """
                Connection.SQL_Prepared_Cursor.execute(query, (1,))
                Connection.SQL_Handle.commit()
                embed = Embed(
                    title='Item Sold!',
                    description=f'You have sold your `Drill` for `${settings.PRICE_DRILL * 0.5}`\
                     50% of the original price.',
                    colour=Colour.dark_gold()
                )
                await ctx.send(embed=embed)
            else:
                await ctx.send("You do not have a Drill!")

        elif int(item) == 3:
            if item_name['jackhammer']:
                query = f"""
                    UPDATE
                    users
                    SET
                    user_cash=user_cash+?
                    WHERE
                    uid={userid}
                """
                Connection.SQL_Prepared_Cursor.execute(query, (settings.PRICE_JACKHAMMER * 0.5,))
                Connection.SQL_Handle.commit()
                query = f"""
                    UPDATE
                    inventory
                    SET
                    item_jackhammer=item_jackhammer-?
                    WHERE
                    uid={userid}
                """
                Connection.SQL_Prepared_Cursor.execute(query, (1,))
                Connection.SQL_Handle.commit()
                embed = Embed(
                    title='Item Sold!',
                    description=f'You have sold your `Jackhammer` for `${settings.PRICE_JACKHAMMER * 0.5}`\
                     50% of the original price.',
                    colour=Colour.dark_gold()
                )
                await ctx.send(embed=embed)
            else:
                await ctx.send("You do not have a Jackhammer!")

        elif int(item) == 4:
            if item_name['metal_detector']:
                query = f"""
                    UPDATE
                    users
                    SET
                    user_cash=user_cash+?
                    WHERE
                    uid={userid}
                """
                Connection.SQL_Prepared_Cursor.execute(query, (settings.PRICE_METALDETECTOR * 0.5,))
                Connection.SQL_Handle.commit()
                query = f"""
                    UPDATE
                    inventory
                    SET
                    item_metal_detector=item_metal_detector-?
                    WHERE
                    uid={userid}
                """
                Connection.SQL_Prepared_Cursor.execute(query, (1,))
                Connection.SQL_Handle.commit()
                embed = Embed(
                    title='Item Sold!',
                    description=f'You have sold your `Metal Detector` for `${settings.PRICE_METALDETECTOR * 0.5}`\
                     50% of the original price.',
                    colour=Colour.dark_gold()
                )
                await ctx.send(embed=embed)
            else:
                await ctx.send("You do not have a Metal Detector!")

        elif int(item) == 5:
            if item_name['gold_detector']:
                query = f"""
                    UPDATE
                    users
                    SET
                    user_cash=user_cash+?
                    WHERE
                    uid={userid}
                """
                Connection.SQL_Prepared_Cursor.execute(query, (settings.PRICE_GOLDDETECTOR * 0.5,))
                Connection.SQL_Handle.commit()
                query = f"""
                    UPDATE
                    inventory
                    SET
                    item_gold_detector=item_gold_detector-?
                    WHERE
                    uid={userid}
                """
                Connection.SQL_Prepared_Cursor.execute(query, (1,))
                Connection.SQL_Handle.commit()
                embed = Embed(
                    title='Item Sold!',
                    description=f'You have sold your `Gold Detector` for `${settings.PRICE_GOLDDETECTOR * 0.5}`\
                     50% of the original price.',
                    colour=Colour.dark_gold()
                )
                await ctx.send(embed=embed)
            else:
                await ctx.send("You do not have a Gold Detector!")

        elif int(item) == 6:
            if item_name['diamond_detector']:
                query = f"""
                    UPDATE
                    users
                    SET
                    user_cash=user_cash+?
                    WHERE
                    uid={userid}
                """
                Connection.SQL_Prepared_Cursor.execute(query, (settings.PRICE_DIAMONDDETECTOR * 0.5,))
                Connection.SQL_Handle.commit()
                query = f"""
                    UPDATE
                    inventory
                    SET
                    item_diamond_detector=item_diamond_detector-?
                    WHERE
                    uid={userid}
                """
                Connection.SQL_Prepared_Cursor.execute(query, (1,))
                Connection.SQL_Handle.commit()
                embed = Embed(
                    title='Item Sold!',
                    description=f'You have sold your `Diamond Detector` for `${settings.PRICE_DIAMONDDETECTOR * 0.5}`\
                     50% of the original price.',
                    colour=Colour.dark_gold()
                )
                await ctx.send(embed=embed)
            else:
                await ctx.send("You do not have a Diamond Detector!")

        elif int(item) == 7:
            if item_name['minecart']:
                query = f"""
                    UPDATE
                    users
                    SET
                    user_cash=user_cash+?
                    WHERE
                    uid={userid}
                """
                Connection.SQL_Prepared_Cursor.execute(query, (settings.PRICE_MINECART * 0.5,))
                Connection.SQL_Handle.commit()
                query = f"""
                    UPDATE
                    inventory
                    SET
                    item_minecart=item_minecart-?
                    WHERE
                    uid={userid}
                """
                Connection.SQL_Prepared_Cursor.execute(query, (1,))
                Connection.SQL_Handle.commit()
                embed = Embed(
                    title='Item Sold!',
                    description=f'You have sold your `Mine Cart` for `${settings.PRICE_MINECART * 0.5}`\
                     50% of the original price.',
                    colour=Colour.dark_gold()
                )
                await ctx.send(embed=embed)
            else:
                await ctx.send("You do not have a Mine Cart!")

        elif int(item) == 8:
            if item_name['minetransport']:
                query = f"""
                    UPDATE
                    users
                    SET
                    user_cash=user_cash+?
                    WHERE
                    uid={userid}
                """
                Connection.SQL_Prepared_Cursor.execute(query, (settings.PRICE_MINETRANSPORT * 0.5,))
                Connection.SQL_Handle.commit()
                query = f"""
                    UPDATE
                    inventory
                    SET
                    item_mine_transport=item_mine_transport-?
                    WHERE
                    uid={userid}
                """
                Connection.SQL_Prepared_Cursor.execute(query, (1,))
                Connection.SQL_Handle.commit()
                embed = Embed(
                    title='Item Sold!',
                    description=f'You have sold your `Mine Transport` for `${settings.PRICE_MINETRANSPORT * 0.5}`\
                     50% of the original price.',
                    colour=Colour.dark_gold()
                )
                await ctx.send(embed=embed)
            else:
                await ctx.send("You do not have a Mine Transport!")

        elif int(item) == 9:
            if item_name['transportplane']:
                query = f"""
                    UPDATE
                    users
                    SET
                    user_cash=user_cash+?
                    WHERE
                    uid={userid}
                """
                Connection.SQL_Prepared_Cursor.execute(query, (settings.PRICE_TRANSPORTPLANE * 0.5,))
                Connection.SQL_Handle.commit()
                query = f"""
                    UPDATE
                    inventory
                    SET
                    item_transportplane=item_transportplane-?
                    WHERE
                    uid={userid}
                """
                Connection.SQL_Cursor.execute(query, (1,))
                Connection.SQL_Handle.commit()
                embed = Embed(
                    title='Item Sold!',
                    description=f'You have sold your `Transport Plane` for `${settings.PRICE_TRANSPORTPLANE * 0.5}`\
                     50% of the original price.',
                    colour=Colour.dark_gold()
                )
                await ctx.send(embed=embed)
            else:
                await ctx.send("You do not have a Transport Plane!")
        else:
            embed = Embed(
                title='USAGE:',
                description='!sell [item id]',
                colour=Colour.dark_gold()
            )
            await ctx.send(embed=embed)

    # Command: Shop
    # Description: Show user shop
    # Cooldown: 10 Seconds
    @commands.command()
    @cooldown(1, 10, BucketType.user)
    async def shop(self, ctx):
        query = f"""
            SELECT
            *
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

        embed = Embed(
            title='User Shop',
            description='Buy useful items and boosters!',
            colour=Colour.dark_gold()
        )
        embed.set_thumbnail(url='https://i.pinimg.com/originals/77/c3/66/77c366436d8bd35fe8b3ce5b8c66992e.png')
        embed.add_field(
            name='1. Pickaxe :pick:',
            value=f'`Price: ${settings.PRICE_PICKAXE}` | `Bonus: 50% Work Salary`',
            inline=True
        )
        drill = utils.get(self.bot.emojis, name='drill')
        embed.add_field(
            name=f'2. Drill {str(drill)}',
            value=f'`Price: ${settings.PRICE_DRILL}` | `Bonus: 75% Work Salary`',
            inline=True
        )
        jackhammer = utils.get(self.bot.emojis, name='jackhammer')
        embed.add_field(
            name=f'3. Jackhammer {str(jackhammer)}',
            value=f'`Price: ${settings.PRICE_JACKHAMMER}` | `Bonus: 100% Work Salary`',
            inline=True
        )
        metal_detector = utils.get(self.bot.emojis, name='metal_detector')
        embed.add_field(
            name=f'4. Metal Detector {str(metal_detector)}',
            value=f'`Price: ${settings.PRICE_METALDETECTOR}` | `Metal Chance: {settings.MD_VALUABLE_CHANCE}%`',
            inline=True
        )
        gold_detector = utils.get(self.bot.emojis, name='metal_detector')
        embed.add_field(
            name=f'5. Gold Detector {str(gold_detector)}',
            value=f'`Price: ${settings.PRICE_GOLDDETECTOR}` | `Gold Chance: {settings.GD_VALUABLE_CHANCE}%`',
            inline=True
        )
        diamond_detector = utils.get(self.bot.emojis, name='metal_detector')
        embed.add_field(
            name=f'6. Diamond Detector {str(diamond_detector)}',
            value=f'`Price: ${settings.PRICE_DIAMONDDETECTOR}` | `Diamond Chance: {settings.DD_VALUABLE_CHANCE}%`',
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
            await ctx.reply(
                f"Hey be chill on buying stuffs bro," +
                f" why don't you wait for `{exc.retry_after:,.1f}` seconds?"
            )

    @shop.error
    async def shop_error(self, ctx, exc):
        if isinstance(exc, CommandOnCooldown):
            await ctx.reply(
                f"Whoa whoa, didn't you already see the menu?" +
                f" why don't you wait for `{exc.retry_after:,.1f}` seconds?"
            )


def setup(bot):
    bot.add_cog(Economy(bot))
