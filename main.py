"""
Module: ./main.py
Description: Main module, the main... module.
Module Dependencies:
    > os
    > mysql.connector
    > discord.ext.commands
    > utils.settings
"""
import asyncio
import os
import unicodedata

import mysql.connector
from discord import Intents, Embed, Colour
from discord.ext import commands
from discord.ext.commands import CommandNotFound

from utils import settings

intents = Intents.default()
intents.members = True


# Setting up the bot and it's prefix for commands
def get_pre():
    return ["sakila.", "s."]  # or a list, ["pre1","pre2"]


bot = commands.Bot(command_prefix=get_pre(), help_command=None, case_insensitive=True, intents=intents)


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
        sakila
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
            user_tag varchar(4),
            user_cash INT,
            user_bank INT,
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
    # Setup equipment table
    SQL_Query = """
        CREATE TABLE
        IF NOT EXISTS
        equipment(
            uid INT NOT NULL,
            equipment_pickaxe INT(1),
            equipment_drill INT(1),
            equipment_jackhammer INT(1),
            equipment_metal_detector INT(1),
            equipment_gold_detector INT(1),
            equipment_diamond_detector INT(1),
            equipment_minecart INT(1),
            equipment_minetransport INT(1),
            equipment_transportplane INT(1),
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
    # Setup inventory table
    SQL_Query = """
        CREATE TABLE
        IF NOT EXISTS
        inventory(
            uid INT NOT NULL,
            metal_metal INT(11),
            metal_gold INT(11),
            metal_diamond INT(11),
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
    SQL_Query = """
        CREATE TABLE
        IF NOT EXISTS
        crypto(
            uid INT NOT NULL,
            crypto_rig INT(11),
            crypto_currency INT(11),
            crypto_wallet INT(11),
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


for file in os.listdir("cogs"):
    if file.endswith(".py"):
        bot.load_extension(f"cogs.{file[:-3]}")


# Just a simple command for testing
@bot.command()
async def debug(ctx):
    await ctx.channel.trigger_typing()
    await asyncio.sleep(2)
    await ctx.send("Debugging successful!")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        if ctx.channel.id in (768814110447108096, 768801742992703498, 764843635610353700):
            return
        embed = Embed(
            title="Error",
            description="That command doesn't exist, type `!help` to see the list of available commands.",
            colour=Colour.red()
        )
        await ctx.channel.trigger_typing()
        await asyncio.sleep(2)
        await ctx.reply(embed=embed)


@bot.command()
async def charinfo(ctx, *, characters: str):
    def to_string(c):
        digit = f'{ord(c):x}'
        name = unicodedata.name(c, 'Name not found.')
        return f'`\\U{digit:>08}`: {name} - {c} \N{EM DASH} <http://www.fileformat.info/info/unicode/char/{digit}>'

    msg = '\n'.join(map(to_string, characters))
    if len(msg) > 2000:
        return await ctx.send('Output too long to display.')
    await ctx.send(msg)


@bot.command()
async def sendembed(ctx, title, description, color=Colour.green()):
    embed = Embed(title=title, description=description, color=color)
    await ctx.send(embed=embed)


bot.run(settings.TOKEN)
