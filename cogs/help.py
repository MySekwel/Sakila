"""
Module: ./cogs/help.py
Description: Help module includes everything needed for the !help command.
Module Dependencies:
    > discord.Embed
    > discord.Colour
    > discord.ext.commands
    > discord.ext.commands.BucketType
    > discord.ext.commands.cooldown,
    > discord.ext.commands.CommandOnCooldown
    > disputils.BotEmbedPaginator
"""
import asyncio
import datetime

from discord import Embed, Colour
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown, CommandOnCooldown

from utils import emoji_dictionary as emoji_dictionary


def empty_field(embed):
    embed.add_field(
        name=emoji_dictionary.special["empty"],
        value=emoji_dictionary.special["empty"],
        inline=True
    )


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Command: Help
    # Description: Shows the list of available commands.
    # Cooldown: 10 Seconds
    @commands.command()
    @cooldown(1, 10, BucketType.user)
    async def help(self, ctx, category=None):
        if category is None:
            await ctx.channel.trigger_typing()
            await asyncio.sleep(2)
            description = ""
            embed = Embed(
                title="Help",
                description=description,
                colour=Colour.random()
            )
            embed.set_thumbnail(url="https://i.imgur.com/bObV3r5.png")
            time = datetime.datetime.now()
            embed.set_footer(text=time.strftime("**Page** 1 | %B %d, %Y | %I:%M %p"))
            embed.add_field(
                name="Category: General",
                value="**Usage:** Show bot commands"
            )
            ctx.send(embed=embed)

            return
        if category.casefold() == "general":
            pass
        elif category.casefold() == "casino":
            pass
        elif category.casefold() == "labor":
            pass
        elif category.casefold() == "economy":
            pass

    @help.error
    async def help_error(self, ctx, exc):
        if isinstance(exc, CommandOnCooldown):
            await ctx.reply(
                f"You really need help huh?" +
                f" Why don't you wait for `{exc.retry_after:,.1f}` seconds?"
            )


def setup(bot):
    bot.add_cog(Help(bot))
