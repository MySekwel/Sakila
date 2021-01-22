import asyncio
import mysql.connector
import discord
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
    database=settings.SQL_DATABASE,
    user=settings.SQL_USER,
    password=settings.SQL_PASSWORD
)
# Setup the connection cursor
SQL_Cursor = SQL_Handle.cursor()
SQL_Prepared_Cursor = SQL_Handle.cursor(prepared=True)

# Setup the tables
SQL_Query = """
    CREATE TABLE
    IF NOT EXISTS
    accounts(
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
        UNIQUE KEY (userid)
    )
"""
SQL_Cursor.execute(SQL_Query)


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
        accounts
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
            accounts(
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
            VALUES (
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
        values = (
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
        SQL_Prepared_Cursor.execute(query, values)
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


# Show user statistics command
@bot.command()
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
        accounts
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
        colour=discord.Colour.green()
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


@bot.command()
@cooldown(1, 5, BucketType.user)
async def work(ctx):
    mining = discord.utils.get(bot.emojis, name='mining')
    embed = discord.Embed(
        title=f'{str(mining)}Mining in Progress...',
        description='Current Tool: Pickaxe',
        colour=discord.Colour.random()
    )
    progress = await ctx.send(embed=embed)
    await asyncio.sleep(5)
    embed = discord.Embed(
        title='Mining Finished!',
        description=f'**You have worked in the mines and earned ${settings.WORK_SALARY} and {settings.WORK_BONUS} exp**',
        colour=discord.Colour.green()
    )
    await progress.edit(
        embed=embed
    )
    query = f"""
        UPDATE
        accounts
        SET
        user_cash=user_cash+?,
        user_exp=user_exp+?
        WHERE
        user_id={ctx.author.id}
    """
    values = (settings.WORK_SALARY, settings.WORK_BONUS)
    SQL_Prepared_Cursor.execute(query, values)

    query = f"""
        SELECT
        *
        FROM
        accounts
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
    SQL_Handle.commit()


@bot.command()
async def shop(ctx):
    await ctx.send(f"**{ctx.author.name}'s shop.**")
    embed = discord.Embed(
        title='User Shop',
        description='Buy useful items and boosters!',
        colour=discord.Colour.dark_gold()
    )
    embed.set_thumbnail(url='https://i.pinimg.com/originals/77/c3/66/77c366436d8bd35fe8b3ce5b8c66992e.png')
    embed.add_field(
        name='1. Pickaxe :pick:',
        value=f'`Price: ${settings.PRICE_DRILL}` | `Bonus: 5% Work Salary`',
        inline=True
    )
    drill = discord.utils.get(bot.emojis, name='drill')
    embed.add_field(
        name=f'2. Drill {str(drill)}',
        value=f'`Price: ${settings.PRICE_JACKHAMMER}` | `Bonus: 10% Work Salary`',
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


@bot.command()
async def buy(ctx, item):
    if int(item) == 1:
        await ctx.send(f"You have bought a `pickaxe` for ${settings.PRICE_PICKAXE}!")
    elif int(item) == 2:
        await ctx.send(f"You have bought a `drill` for ${settings.PRICE_DRILL}!")
    elif int(item) == 3:
        await ctx.send(f"You have bought a `jackhammer` for ${settings.PRICE_JACKHAMMER}!")
    elif int(item) == 4:
        await ctx.send(f"You have bought a `metal detector` for ${settings.PRICE_METALDETECTOR}!")
    elif int(item) == 5:
        await ctx.send(f"You have bought a `gold detector` for ${settings.PRICE_GOLDDETECTOR}!")
    elif int(item) == 6:
        await ctx.send(f"You have bought a `diamond detector` for ${settings.PRICE_DIAMONDDETECTOR}!")
    elif int(item) == 7:
        await ctx.send(f"You have bought a `minecart` for ${settings.PRICE_MINECART}!")
    elif int(item) == 8:
        await ctx.send(f"You have bought a `mine transport` for ${settings.PRICE_MINETRANSPORT}!")
    elif int(item) == 9:
        await ctx.send(f"You have bought a `transport plane` for ${settings.PRICE_TRANSPORTPLANE}!")


@bot.event
async def on_message(message):
    # Check if the user who sent the message is not the bot itself
    if message.author == bot.user:
        return

    if message.content == 'hi':
        await message.channel.send('Hello!')
    await bot.process_commands(message)


@bot.event
async def on_command_error(ctx, exc):
    if isinstance(exc, CommandOnCooldown):
        await ctx.send(f"Hey {ctx.author.name} why don't you take a rest for about {exc.retry_after:,.1f} seconds?")


@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == settings.GUILD:
            break
        print(f'{bot.user} is connected to the following guild: {guild.name}')

bot.run(TOKEN)
