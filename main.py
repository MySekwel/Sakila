import asyncio
import os

import mysql.connector
import discord
from discord import utils, Colour, Embed
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown, CommandOnCooldown
import settings

# Discord Bot Token variable
TOKEN = settings.TOKEN
# Setting up the bot and it's prefix for commands
bot = commands.Bot(command_prefix='!', help_command=None)

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

for file in os.listdir('cogs'):
    if file.endswith('.py'):
        bot.load_extension(f'cogs.{file[:-3]}')


# Just a simple command for testing
@bot.command()
async def debug(ctx):
    await ctx.send('Debugging complete!')


# Command: Help
# Description: Shows the list of available commands.
# Cooldown: 5 seconds
@bot.command()
@cooldown(1, 5, BucketType.user)
async def help(ctx):
    embed = Embed(
        title='Help',
        description='List of commands:',
        colour=Colour.dark_orange()
    )
    embed.set_thumbnail(url='https://i.imgur.com/bObV3r5.png')
    embed.add_field(
        name='Command: !Help',
        value='**Description:** Shows the list of available commands.',
        inline=False
    )
    embed.add_field(
        name='Command: !Register',
        value='**Description:** Register to the database to use the other commands.',
        inline=False
    )
    embed.add_field(
        name='Command: !Ping',
        value='**Description:** Shows user latency.',
        inline=False
    )
    embed.add_field(
        name='Command: !Work',
        value='**Description:** Mine to earn money.',
        inline=False
    )
    embed.add_field(
        name='Command: !Stats',
        value='**Description:** Show user stats.',
        inline=False
    )
    embed.add_field(
        name='Command: !Shop',
        value='**Description:** Show user shop.',
        inline=False
    )
    embed.add_field(
        name='Command: !Buy',
        value='**Description:** Buy command for user shop.',
        inline=False
    )
    await ctx.send(embed=embed)


# Command: Stats
# Description: Show user stats
# Cooldown: 5 Seconds
@bot.command()
@cooldown(1, 5, BucketType.user)
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
@bot.command()
@cooldown(1, 5, BucketType.user)
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


@bot.event
async def on_message(message):
    # Check if the user who sent the message is not the bot itself
    if message.author.id == bot.user.id:
        return

    if message.content == 'hi':
        await message.channel.send('Hello!')
    await bot.process_commands(message)


@help.error
async def help_error(ctx, exc):
    if isinstance(exc, CommandOnCooldown):
        await ctx.send(
            f"Hey <@!{ctx.author.id}> you really need help huh?" +
            f" Why don't you wait for `{exc.retry_after:,.1f}` seconds?"
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
