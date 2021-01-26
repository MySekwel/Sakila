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

import mysql.connector
from discord import state, Game, Intents
from discord.ext import commands

from utils import settings

intents = Intents.default()
intents.members = True

# Setting up the bot and it's prefix for commands
bot = commands.Bot(command_prefix='!', help_command=None, case_insensitive=True, intents=intents)


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
            user_tag INT(4),
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


for file in os.listdir('cogs'):
    if file.endswith('.py'):
        bot.load_extension(f'cogs.{file[:-3]}')


# Just a simple command for testing
@bot.command()
async def debug(ctx):
    await ctx.channel.trigger_typing()
    await asyncio.sleep(2)
    await ctx.send('Debugging successful!')


@bot.event
async def on_connect():
    for guild in bot.guilds:
        print(f"{bot.user} is connected to the following guild: {guild.name}")

    await bot.change_presence(activity=Game(name='Console Adventures'), status=state.Status.online)


bot.run(settings.TOKEN)
