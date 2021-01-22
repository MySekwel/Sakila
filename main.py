import asyncio
import mysql.connector
import discord
from discord import utils, Colour
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown, CommandOnCooldown
import settings

# Discord Bot Token variable
TOKEN = settings.TOKEN
# Setting up the bot and it's prefix for commands
bot = commands.Bot(command_prefix='!')

# Connect us to the database with the following information
SQL_Handle = mysql.connector.connect(
    host=settings.SQL_HOST,
    user=settings.SQL_USER,
    password=settings.SQL_PASSWORD
)
# Setup the connection cursor
SQL_Cursor = SQL_Handle.cursor()

# Setup the database and tables
SQL_Query = """
    CREATE DATABASE
    IF NOT EXISTS
    mysekwel
"""
SQL_Cursor.execute(SQL_Query)
SQL_Handle.commit()
# Connect with new database
SQL_Handle = mysql.connector.connect(
    host=settings.SQL_HOST,
    database=settings.SQL_DATABASE,
    user=settings.SQL_USER,
    password=settings.SQL_PASSWORD
)
SQL_Cursor = SQL_Handle.cursor()
SQL_Prepared_Cursor = SQL_Handle.cursor(prepared=True)
# Setup users table
SQL_Query = """
    CREATE TABLE
    IF NOT EXISTS
    users(
        uid INT NOT NULL AUTO_INCREMENT,
        user_id varchar(20),
        user_name varchar(24),
        user_tag INT(4),
        user_cash INT,
        user_diamonds INT,
        user_exp INT,
        user_reputation INT,
        user_love INT,
        user_vip varchar(16),
        PRIMARY KEY (uid),
        UNIQUE KEY (user_id)
    )
"""
SQL_Cursor.execute(SQL_Query)
SQL_Handle.commit()
# Setup inventory table
SQL_Query = """
    CREATE TABLE
    IF NOT EXISTS
    inventory(
        uid INT NOT NULL,
        item_pickaxe INT(1),
        item_drill INT(1),
        item_jackhammer INT(1),
        item_metal_detector INT(1),
        item_gold_detector INT(1),
        item_diamond_detector INT(1),
        item_minecart INT(1),
        item_minetransport INT(1),
        item_transportplane INT(1),
        PRIMARY KEY (uid),
        FOREIGN KEY (uid)
        REFERENCES
        users (uid)
        ON DELETE CASCADE
        ON UPDATE RESTRICT
    )
"""
SQL_Cursor.execute(SQL_Query)
SQL_Handle.commit()


# Just a simple command for testing
@bot.command()
async def debug(ctx):
    await ctx.send('Debugging complete!')


# Register to the database command
@bot.command()
async def register(ctx):
    query = """
        SELECT
        MAX(uid)
        FROM
        users
    """
    SQL_Cursor.execute(query)
    result = SQL_Cursor.fetchone()
    SQL_Handle.commit()
    lastid = result[0]
    if lastid:
        lastid = lastid + 1

    try:
        query = """
            INSERT INTO
            users(
                user_id,
                user_name,
                user_tag,
                user_cash,
                user_diamonds,
                user_exp,
                user_reputation,
                user_love,
                user_vip
            )
            VALUES(
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?
            )
        """
        stats_values = (
            ctx.author.id,
            ctx.author.name,
            ctx.author.discriminator,
            100,
            0,
            0,
            0,
            0,
            'None'
        )
        SQL_Prepared_Cursor.execute(query, stats_values)
        SQL_Handle.commit()
        query = f"""
            SELECT
            uid
            FROM
            users
            WHERE
            user_id={ctx.author.id}
        """
        SQL_Cursor.execute(query)
        result = SQL_Cursor.fetchone()
        SQL_Handle.commit()
        uid = result[0]
        query = """
            INSERT INTO
            inventory(
                uid,
                item_pickaxe,
                item_drill,
                item_jackhammer,
                item_metal_detector,
                item_gold_detector,
                item_diamond_detector,
                item_minecart,
                item_minetransport,
                item_transportplane
            )
            VALUES(
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?
            )
        """
        inventory_values = (
            uid,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
        )
        SQL_Prepared_Cursor.execute(query, inventory_values)
        SQL_Handle.commit()
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        await ctx.send("**You are already registered to the database!**")
        return

    await ctx.send(
        f"""
        You are now registered to the database with the following information:
        **UID:** `{lastid}`
        **UserID:** `{ctx.author.id}`
        **UserName:** `{ctx.author.name}`
        **UserTag:** `{ctx.author.discriminator}`
    """
    )


# Command: Work
# Description: Mine to earn money
# Cooldown: 15 seconds
@bot.command()
@cooldown(1, 15, BucketType.user)
async def work(ctx):
    query = f"""
        SELECT
        *
        FROM
        users
        WHERE
        user_id={ctx.author.id}
    """
    SQL_Cursor.execute(query)
    result = SQL_Cursor.fetchone()
    SQL_Handle.commit()
    if not result:
        await ctx.send("**You are not registered to the database!**")
        await ctx.send("TIP: `!register`")
        return

    mining = utils.get(bot.emojis, name='mining')
    embed = discord.Embed(
        title=f'{str(mining)}Mining in Progress...',
        description='**Current Tool**: Pickaxe',
        colour=Colour.random()
    )
    progress = await ctx.send(embed=embed)
    await asyncio.sleep(15)
    embed = discord.Embed(
        title='Mining Finished!',
        description=f'**You have worked in the mines and earned \
         ${settings.WORK_SALARY} and {settings.WORK_BONUS} exp**',
        colour=Colour.green()
    )
    await progress.edit(
        embed=embed
    )
    query = f"""
        UPDATE
        users
        SET
        user_cash=user_cash+?,
        user_exp=user_exp+?
        WHERE
        user_id={ctx.author.id}
    """
    values = (settings.WORK_SALARY, settings.WORK_BONUS)
    SQL_Prepared_Cursor.execute(query, values)
    SQL_Handle.commit()


# Command: Stats
# Description: Show user stats
# Cooldown: 2 Seconds
@bot.command()
@cooldown(1, 2, BucketType.user)
async def stats(ctx):
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
    SQL_Cursor.execute(query)
    result = SQL_Cursor.fetchone()
    SQL_Handle.commit()
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

    embed = discord.Embed(
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
# Cooldown: 2 Seconds
@bot.command()
@cooldown(1, 2, BucketType.user)
async def inventory(ctx):
    query = f"""
        SELECT
        uid
        FROM
        users
        WHERE
        user_id={ctx.author.id}
    """
    SQL_Cursor.execute(query)
    result = SQL_Cursor.fetchone()
    SQL_Handle.commit()
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
    SQL_Cursor.execute(query)
    result = SQL_Cursor.fetchone()
    SQL_Handle.commit()
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

    embed = discord.Embed(
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
    emoji_drill = discord.utils.get(bot.emojis, name='drill')
    embed.add_field(
        name='Drill',
        value=f'{str(emoji_drill)} `{drill}`',
        inline=True
    )
    emoji_jackhammer = discord.utils.get(bot.emojis, name='jackhammer')
    embed.add_field(
        name='Jackhammer',
        value=f'{str(emoji_jackhammer)} `{jackhammer}`',
        inline=True
    )
    emoji_metal_detector = discord.utils.get(bot.emojis, name='metal_detector')
    embed.add_field(
        name='Metal Detector',
        value=f'{str(emoji_metal_detector)} `{metal_detector}`',
        inline=True
    )
    emoji_gold_detector = discord.utils.get(bot.emojis, name='metal_detector')
    embed.add_field(
        name='Gold Detector',
        value=f'{str(emoji_gold_detector)} `{gold_detector}`',
        inline=True
    )
    emoji_diamond_detector = discord.utils.get(bot.emojis, name='metal_detector')
    embed.add_field(
        name='Diamond Detector',
        value=f'{str(emoji_diamond_detector)} `{diamond_detector}`',
        inline=True
    )
    emoji_minecart = discord.utils.get(bot.emojis, name='minecart')
    embed.add_field(
        name='Mine Cart',
        value=f'{str(emoji_minecart)} `{minecart}`',
        inline=True
    )
    emoji_minetransport = discord.utils.get(bot.emojis, name='minetransport')
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


# Command: Shop
# Description: Show user shop
# Cooldown: 2 Seconds
@bot.command()
@cooldown(1, 2, BucketType.user)
async def shop(ctx):
    query = f"""
        SELECT
        *
        FROM
        users
        WHERE
        user_id={ctx.author.id}
    """
    SQL_Cursor.execute(query)
    result = SQL_Cursor.fetchone()
    SQL_Handle.commit()
    if not result:
        await ctx.send("**You are not registered to the database!**")
        await ctx.send("TIP: `!register`")
        return

    embed = discord.Embed(
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
    drill = discord.utils.get(bot.emojis, name='drill')
    embed.add_field(
        name=f'2. Drill {str(drill)}',
        value=f'`Price: ${settings.PRICE_DRILL}` | `Bonus: 10% Work Salary`',
        inline=True
    )
    jackhammer = discord.utils.get(bot.emojis, name='jackhammer')
    embed.add_field(
        name=f'3. Jackhammer {str(jackhammer)}',
        value=f'`Price: ${settings.PRICE_JACKHAMMER}` | `Bonus: 25% Work Salary`',
        inline=True
    )
    metal_detector = discord.utils.get(bot.emojis, name='metal_detector')
    embed.add_field(
        name=f'4. Metal Detector {str(metal_detector)}',
        value=f'`Price: ${settings.PRICE_METALDETECTOR}` | `Bonus: 35% Work Salary`',
        inline=True
    )
    gold_detector = discord.utils.get(bot.emojis, name='metal_detector')
    embed.add_field(
        name=f'5. Gold Detector {str(gold_detector)}',
        value=f'`Price: ${settings.PRICE_GOLDDETECTOR}` | `Bonus: 50% Work Salary`',
        inline=True
    )
    diamond_detector = discord.utils.get(bot.emojis, name='metal_detector')
    embed.add_field(
        name=f'6. Diamond Detector {str(diamond_detector)}',
        value=f'`Price: ${settings.PRICE_DIAMONDDETECTOR}` | `Bonus: 75% Work Salary`',
        inline=True
    )
    minecart = discord.utils.get(bot.emojis, name='minecart')
    embed.add_field(
        name=f'7. Minecart {str(minecart)}',
        value=f'`Price: ${settings.PRICE_MINECART}` | `Bonus: -10% Work Cooldown`',
        inline=True
    )
    minetransport = discord.utils.get(bot.emojis, name='minetransport')
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


# Command: Buy
# Description: Buy command for user shop
# Cooldown: 2 Seconds
@bot.command()
@cooldown(1, 2, BucketType.user)
async def buy(ctx, item):
    query = f"""
        SELECT
        *
        FROM
        users
        WHERE
        user_id={ctx.author.id}
    """
    SQL_Cursor.execute(query)
    result = SQL_Cursor.fetchone()
    SQL_Handle.commit()
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
    SQL_Cursor.execute(query)
    result = SQL_Cursor.fetchone()
    SQL_Handle.commit()
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
    SQL_Cursor.execute(query)
    result = SQL_Cursor.fetchone()
    SQL_Handle.commit()

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
    if len(item) == 0:
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
        SQL_Prepared_Cursor.execute(query, (1,))
        SQL_Handle.commit()

        query = f"""
            UPDATE
            users
            SET
            user_cash=user_cash-?
            WHERE
            user_id={ctx.author.id}
        """
        SQL_Prepared_Cursor.execute(query, (settings.PRICE_PICKAXE,))
        SQL_Handle.commit()

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
        SQL_Prepared_Cursor.execute(query, (1,))
        SQL_Handle.commit()

        query = f"""
            UPDATE
            users
            SET
            user_cash=user_cash-?
            WHERE
            user_id={ctx.author.id}
        """
        SQL_Prepared_Cursor.execute(query, (settings.PRICE_DRILL,))
        SQL_Handle.commit()

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
        SQL_Prepared_Cursor.execute(query, (1,))
        SQL_Handle.commit()

        query = f"""
            UPDATE
            users
            SET
            user_cash=user_cash-?
            WHERE
            user_id={ctx.author.id}
        """
        SQL_Prepared_Cursor.execute(query, (settings.PRICE_JACKHAMMER,))
        SQL_Handle.commit()

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
        SQL_Prepared_Cursor.execute(query, (1,))
        SQL_Handle.commit()

        query = f"""
            UPDATE
            users
            SET
            user_cash=user_cash-?
            WHERE
            user_id={ctx.author.id}
        """
        SQL_Prepared_Cursor.execute(query, (settings.PRICE_METALDETECTOR,))
        SQL_Handle.commit()

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
        SQL_Prepared_Cursor.execute(query, (1,))
        SQL_Handle.commit()

        query = f"""
            UPDATE
            users
            SET
            user_cash=user_cash-?
            WHERE
            user_id={ctx.author.id}
        """
        SQL_Prepared_Cursor.execute(query, (settings.PRICE_GOLDDETECTOR,))
        SQL_Handle.commit()

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
        SQL_Prepared_Cursor.execute(query, (1,))
        SQL_Handle.commit()

        query = f"""
            UPDATE
            users
            SET
            user_cash=user_cash-?
            WHERE
            user_id={ctx.author.id}
        """
        SQL_Prepared_Cursor.execute(query, (settings.PRICE_DIAMONDDETECTOR,))
        SQL_Handle.commit()

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
        SQL_Prepared_Cursor.execute(query, (1,))
        SQL_Handle.commit()

        query = f"""
            UPDATE
            users
            SET
            user_cash=user_cash-?
            WHERE
            user_id={ctx.author.id}
        """
        SQL_Prepared_Cursor.execute(query, (settings.PRICE_MINECART,))
        SQL_Handle.commit()

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
        SQL_Prepared_Cursor.execute(query, (1,))
        SQL_Handle.commit()

        query = f"""
            UPDATE
            users
            SET
            user_cash=user_cash-?
            WHERE
            user_id={ctx.author.id}
        """
        SQL_Prepared_Cursor.execute(query, (settings.PRICE_MINETRANSPORT,))
        SQL_Handle.commit()

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
        SQL_Prepared_Cursor.execute(query, (1,))
        SQL_Handle.commit()

        query = f"""
            UPDATE
            users
            SET
            user_cash=user_cash-?
            WHERE
            user_id={ctx.author.id}
        """
        SQL_Prepared_Cursor.execute(query, (settings.PRICE_TRANSPORTPLANE,))
        SQL_Handle.commit()

        await ctx.send(f"You have bought a `transport plane` for ${settings.PRICE_TRANSPORTPLANE}!")
    else:
        await ctx.send("USAGE: !buy [item id]")


@bot.event
async def on_message(message):
    # Check if the user who sent the message is not the bot itself
    if message.author == bot.user:
        return

    if message.content == 'hi':
        await message.channel.send('Hello!')
    await bot.process_commands(message)


@work.error
async def work_error(ctx, exc):
    if isinstance(exc, CommandOnCooldown):
        await ctx.send(
            f"Hey <@!{ctx.author.id}> you still have a work in progress," +
            f" why don't you wait for `{exc.retry_after:,.1f}` seconds?"
        )


@buy.error
async def buy_error(ctx, exc):
    if isinstance(exc, CommandOnCooldown):
        await ctx.send(
            f"Hey <@!{ctx.author.id}> be chill on buying stuffs bro," +
            f" why don't you wait for `{exc.retry_after:,.1f}` seconds?"
        )


@stats.error
async def stats_error(ctx, exc):
    if isinstance(exc, CommandOnCooldown):
        await ctx.send(
            f"Hey <@!{ctx.author.id}> you've already seen your stats," +
            f"why don't you wait for `{exc.retry_after:,.1f}` seconds?"
        )


@inventory.error
async def inventory_error(ctx, exc):
    if isinstance(exc, CommandOnCooldown):
        await ctx.send(
            f"Hey <@!{ctx.author.id}> you've already seen your inventory no one will rob you," +
            f"why don't you wait for `{exc.retry_after:,.1f}` seconds?")


@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == settings.GUILD:
            break
        print(f"{bot.user} is connected to the following guild: {guild.name}")


bot.run(TOKEN)
