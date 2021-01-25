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
WORK_SALARY_BONUS = 0
WORK_BONUS = 50

PRICE_PICKAXE = 500
PRICE_DRILL = 2500
PRICE_JACKHAMMER = 5000
PRICE_METALDETECTOR = 7500
PRICE_GOLDDETECTOR = 15000
PRICE_DIAMONDDETECTOR = 25000
PRICE_MINECART = 35000
PRICE_MINETRANSPORT = 55000
PRICE_TRANSPORTPLANE = 150000