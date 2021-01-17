import mysql.connector
from discord.ext import commands
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

# Setup the tables
SQL_Query = """
    CREATE TABLE
    IF NOT EXISTS
    accounts(
        uid int NOT NULL AUTO_INCREMENT,
        userid varchar(20),
        username varchar(24),
        usertag int(4),
        PRIMARY KEY (uid),
        UNIQUE KEY (userid)
    )
"""
SQL_Cursor.execute(SQL_Query)

# Just a simple reminder on fetching and storing data from the database
SQL_Cursor.execute(
    "SELECT * FROM accounts"
)
# Fetch all the rows from the SELECT query
SQL_Result = SQL_Cursor.fetchall()
# SQL_Count - For iterators, returns the number of rows
SQL_Count = SQL_Cursor.rowcount
# Store all the data in a temporary iterator (Just for debugging)
# Don't mind this block of code
for i in range(SQL_Count):
    SQL_UID = SQL_Result[i][0]
    SQL_UserID = SQL_Result[i][1]
    SLQ_UserName = SQL_Result[i][2]
    SQL_UserTag = SQL_Result[i][3]


# Just a simple command for testing
@bot.command()
async def debug(ctx):
    await ctx.send('Debugging complete!')


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
    lastid = result[0] + 1
    try:
        query = """
            INSERT
            INTO
            accounts(
                userid,
                username,
                usertag
            )
            VALUES(
                %s,
                %s,
                %d
            )
        """
        SQL_Cursor.execute(query, (ctx.author.id, ctx.author.name, ctx.author.discriminator))
        SQL_Handle.commit()
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        await ctx.send("**You are already registered to the database!**")
        return

    message = f"""
        You are now registered to the database with the following information:
        **UID:** `{lastid}`
        **UserID:** `{ctx.author.id}`,
        **UserName:** `{ctx.author.name}`,
        **UserTag:** `{ctx.author.discriminator}`
    """
    await ctx.send(message)


@bot.event
async def on_message(message):
    if message.content == 'hi':
        await message.channel.send('Hello!')
    await bot.process_commands(message)


@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == settings.GUILD:
            break
        print(f'{bot.user} is connected to the following guild: {guild.name}')

bot.run(TOKEN)
