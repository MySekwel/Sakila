import os
import mysql.connector
from discord import Colour, Embed
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown, CommandOnCooldown
import settings

# Discord Bot Token variable
TOKEN = settings.TOKEN
# Setting up the bot and it's prefix for commands
bot = commands.Bot(command_prefix='!', help_command=None, case_insensitive=True)


class Connection:
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


@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == settings.GUILD:
            break
        print(f"{bot.user} is connected to the following guild: {guild.name}")


bot.run(TOKEN)
