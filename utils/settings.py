"""
Module: ./utils/settings.py
Description: Settings module, holds default settings.
Module Dependencies:
    > os
    > dotenv.load_dotenv
"""

import os

# Dotenv for Discord API Token
from dotenv import load_dotenv

# Load the .env file
load_dotenv()
# Fetch DISCORD_TOKEN
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

SQL_HOST = os.getenv('HOST')
SQL_DATABASE = os.getenv('DATABASE')
SQL_USER = os.getenv('USER')
SQL_PASSWORD = os.getenv('PASSWORD')

WORK_SALARY = 100
WORK_BONUS = 50
MD_VALUABLE_CHANCE = 10
GD_VALUABLE_CHANCE = 20
DD_VALUABLE_CHANCE = 35

PRICE_PICKAXE = 2500
PRICE_DRILL = 5000
PRICE_JACKHAMMER = 15000
PRICE_METALDETECTOR = 7500
PRICE_GOLDDETECTOR = 15000
PRICE_DIAMONDDETECTOR = 25000
PRICE_MINECART = 35000
PRICE_MINETRANSPORT = 55000
PRICE_TRANSPORTPLANE = 150000
PRICE_METAL = 20
PRICE_GOLD = 50
PRICE_DIAMOND = 150
