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

PRICE_PICKAXE           = 100
PRICE_DRILL             = 500
PRICE_JACKHAMMER        = 2500
PRICE_METALDETECTOR     = 3500
PRICE_GOLDDETECTOR      = 7500
PRICE_DIAMONDDETECTOR   = 15000
PRICE_MINECART          = 15000
PRICE_MINETRANSPORT     = 25000
PRICE_TRANSPORTPLANE    = 50000
