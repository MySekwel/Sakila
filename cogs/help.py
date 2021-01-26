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

from discord import Embed, Colour, Color
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
            description = \
                "Use `!help [command]` for more info on a *command*.\n\
                Use `!help [category]` for more info on a *category*.\n\
                For more help, join the official bot support server: https://discord.gg/EpDbtGbDv6"
            embed = Embed(
                title="Help",
                description=description,
                colour=Colour.random()
            )
            embed.set_thumbnail(url="https://i.imgur.com/bObV3r5.png")

            empty_field(embed)
            empty_field(embed)
            empty_field(embed)

            embed.add_field(
                name="Categories:",
                value=emoji_dictionary.special['empty'],
                inline=True
            )
            empty_field(embed)
            empty_field(embed)
            embed.add_field(
                name="Category: General",
                value="**Description:** Shows all available commands that are uncategorized.",
                inline=True
            )
            embed.add_field(
                name="Category: Casino",
                value="**Description:** Casino System, all gambling related commands, for people who loves risks!",
                inline=True
            )
            embed.add_field(
                name="Category: Labor",
                value="**Description:** Labor System, money-earning commands, for industrious people.",
                inline=True
            )
            embed.add_field(
                name="Category: Economy",
                value="**Description:** Economy System, commands related to the economy like buying & selling of "
                      "stuffs.",
                inline=True
            )
            embed.add_field(
                name="Category: Reaction",
                value="**Description:** Reaction System, how to get reaction stats like reputation, love and more.",
                inline=True
            )
            embed.add_field(
                name="Category: Donation",
                value="**Description:** Want to donate? Here's how.",
                inline=True
            )
            empty_field(embed)
            empty_field(embed)
            empty_field(embed)
            embed.add_field(
                name="Commands:",
                value=emoji_dictionary.special['empty'],
                inline=True
            )
            empty_field(embed)
            empty_field(embed)
            embed.add_field(
                name="Command: !help",
                value="**Description:** Show the help menu.\n**Usage:** `!help [command/category]`",
                inline=True
            )
            time = datetime.datetime.now()
            embed.set_footer(text=time.strftime("Page 1 | %B %d, %Y | %I:%M %p"))
            await ctx.send(embed=embed)

            return
        if category.casefold() == "general":
            pass
        elif category.casefold() == "casino":
            pass
        elif category.casefold() == "labor":
            pass
        elif category.casefold() == "economy":
            pass
        elif category.casefold() == 'reaction':
            pass
        elif category.casefold() == 'donate':
            pass
        else:
            embed = Embed(
                title="Error",
                description="That category doesn't exist, type `!help` to see the available categories.",
                colour=Color.red()
            )
            await ctx.channel.trigger_typing()
            await asyncio.sleep(2)
            await ctx.reply(embed=embed)

    @help.error
    async def help_error(self, ctx, exc):
        if isinstance(exc, CommandOnCooldown):
            await ctx.reply(
                f"You really need help huh?" +
                f" Why don't you wait for `{exc.retry_after:,.1f}` seconds?"
            )


def setup(bot):
    bot.add_cog(Help(bot))
