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

from utils import emoji_dictionary as emojii


def empty_field(embed):
    embed.add_field(
        name=emojii.special["empty"],
        value=emojii.special["empty"],
        inline=True
    )


guild_hashmap = {}


async def show_page(ctx, page):
    if int(page) == 1:
        description = \
            "Use `!help [command]` for more info on a *command*.\n\
            Use `!help [category]` for more info on a *category*.\n\
            For more help, join the official bot support server: https://discord.gg/EpDbtGbDv6"
        embed = Embed(
            title="Help",
            description=description,
            colour=Colour.random()
        )

        embed.add_field(
            name="Categories:",
            value=emojii.special['empty'],
            inline=True
        )
        empty_field(embed)
        empty_field(embed)
        embed.add_field(
            name="Category: [General]",
            value="**Description:** Shows all available commands that are uncategorized.",
            inline=True
        )
        embed.add_field(
            name="Category: [Casino]",
            value="**Description:** Casino System, all gambling related commands, for people who loves risks!",
            inline=True
        )
        embed.add_field(
            name="Category: [Labor]",
            value="**Description:** Labor System, money-earning commands, for industrious people.",
            inline=True
        )
        embed.add_field(
            name="Category: [Economy]",
            value="**Description:** Economy System, commands related to the economy like buying & selling of "
                  "stuffs.",
            inline=True
        )
        embed.add_field(
            name="Category: [Reaction]",
            value="**Description:** Reaction System, how to get reaction stats like reputation, love and more.",
            inline=True
        )
        embed.add_field(
            name="Category: [Donation]",
            value="**Description:** Want to donate? Here's how.",
            inline=True
        )
        time = datetime.datetime.now()
        embed.set_footer(text=time.strftime(f"Page {page} | %B %d, %Y | %I:%M %p"))
        await ctx.edit(embed=embed)

    elif int(page) == 2:
        description = \
            "Use `!help [command]` for more info on a *command*.\n\
            Use `!help [category]` for more info on a *category*.\n\
            For more help, join the official bot support server: https://discord.gg/EpDbtGbDv6"
        embed = Embed(
            title="Help",
            description=description,
            colour=Colour.random()
        )
        embed.add_field(
            name="Category: [General]",
            value="**Description:** Shows all available commands that are uncategorized.",
            inline=True
        )
        time = datetime.datetime.now()
        embed.set_footer(text=time.strftime(f"Page {page} | %B %d, %Y | %I:%M %p"))
        await ctx.edit(embed=embed)
    elif int(page) == 3:
        description = \
            "Use `!help [command]` for more info on a *command*.\n\
            Use `!help [category]` for more info on a *category*.\n\
            For more help, join the official bot support server: https://discord.gg/EpDbtGbDv6"
        embed = Embed(
            title="Help",
            description=description,
            colour=Colour.random()
        )
        embed.add_field(
            name="Category: [Casino]",
            value="**Description:** Casino System, all gambling related commands, for people who loves risks!",
            inline=True
        )
        time = datetime.datetime.now()
        embed.set_footer(text=time.strftime(f"Page {page} | %B %d, %Y | %I:%M %p"))
        await ctx.edit(embed=embed)
    elif int(page) == 4:
        description = \
            "Use `!help [command]` for more info on a *command*.\n\
            Use `!help [category]` for more info on a *category*.\n\
            For more help, join the official bot support server: https://discord.gg/EpDbtGbDv6"
        embed = Embed(
            title="Help",
            description=description,
            colour=Colour.random()
        )
        embed.add_field(
            name="Category: [Labor]",
            value="**Description:** Labor System, money-earning commands, for industrious people.",
            inline=True
        )
        time = datetime.datetime.now()
        embed.set_footer(text=time.strftime(f"Page {page} | %B %d, %Y | %I:%M %p"))
        await ctx.edit(embed=embed)
    elif int(page) == 5:
        description = \
            "Use `!help [command]` for more info on a *command*.\n\
            Use `!help [category]` for more info on a *category*.\n\
            For more help, join the official bot support server: https://discord.gg/EpDbtGbDv6"
        embed = Embed(
            title="Help",
            description=description,
            colour=Colour.random()
        )
        embed.add_field(
            name="Category: [Economy]",
            value="**Description:** Economy System, commands related to the economy like buying & selling of "
                  "stuffs.",
            inline=True
        )
        time = datetime.datetime.now()
        embed.set_footer(text=time.strftime(f"Page {page} | %B %d, %Y | %I:%M %p"))
        await ctx.edit(embed=embed)
    elif int(page) == 6:
        description = \
            "Use `!help [command]` for more info on a *command*.\n\
            Use `!help [category]` for more info on a *category*.\n\
            For more help, join the official bot support server: https://discord.gg/EpDbtGbDv6"
        embed = Embed(
            title="Help",
            description=description,
            colour=Colour.random()
        )
        embed.add_field(
            name="Category: [Reaction]",
            value="**Description:** Reaction System, how to get reaction stats like reputation, love and more.",
            inline=True
        )
        time = datetime.datetime.now()
        embed.set_footer(text=time.strftime(f"Page {page} | %B %d, %Y | %I:%M %p"))
        await ctx.edit(embed=embed)
    elif int(page) == 7:
        description = \
            "Use `!help [command]` for more info on a *command*.\n\
            Use `!help [category]` for more info on a *category*.\n\
            For more help, join the official bot support server: https://discord.gg/EpDbtGbDv6"
        embed = Embed(
            title="Help",
            description=description,
            colour=Colour.random()
        )
        embed.add_field(
            name="Category: [Donation]",
            value="**Description:** Want to donate? Here's how.",
            inline=True
        )
        time = datetime.datetime.now()
        embed.set_footer(text=time.strftime(f"Page {page} | %B %d, %Y | %I:%M %p"))
        await ctx.edit(embed=embed)


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Command: Help
    # Description: Shows the list of available commands.
    # Cooldown: 10 Seconds
    @commands.command()
    @cooldown(1, 10, BucketType.user)
    async def help(self, ctx, category=None):
        guild_hashmap[f"{ctx.guild}_page"] = 1

        if category is None:
            await ctx.channel.trigger_typing()
            await asyncio.sleep(2)

            embed = Embed(
                title="Help",
                description=self.description,
                colour=Colour.random()
            )

            embed.add_field(
                name="Categories:",
                value=emojii.special['empty'],
                inline=True
            )
            empty_field(embed)
            empty_field(embed)
            embed.add_field(
                name="Category: [General]",
                value="**Description:** Shows all available commands that are uncategorized.",
                inline=True
            )
            embed.add_field(
                name="Category: [Casino]",
                value="**Description:** Casino System, all gambling related commands, for people who loves risks!",
                inline=True
            )
            embed.add_field(
                name="Category: [Labor]",
                value="**Description:** Labor System, money-earning commands, for industrious people.",
                inline=True
            )
            embed.add_field(
                name="Category: [Economy]",
                value="**Description:** Economy System, commands related to the economy like buying & selling of "
                      "stuffs.",
                inline=True
            )
            embed.add_field(
                name="Category: [Reaction]",
                value="**Description:** Reaction System, how to get reaction stats like reputation, love and more.",
                inline=True
            )
            embed.add_field(
                name="Category: [Donation]",
                value="**Description:** Want to donate? Here's how.",
                inline=True
            )
            time = datetime.datetime.now()
            embed.set_footer(text=time.strftime(f"Page 1 | %B %d, %Y | %I:%M %p"))
            guild_hashmap[f"{ctx.guild}_message"] = await ctx.send(embed=embed)

            await guild_hashmap[f"{ctx.guild}_message"].add_reaction(emojii.arrow["double_left"])
            await guild_hashmap[f"{ctx.guild}_message"].add_reaction(
                emojii.arrow["small_left"] + emojii.special["variant"])
            await guild_hashmap[f"{ctx.guild}_message"].add_reaction(emojii.number["1234"])
            await guild_hashmap[f"{ctx.guild}_message"].add_reaction(
                emojii.arrow["small_right"] + emojii.special["variant"])
            await guild_hashmap[f"{ctx.guild}_message"].add_reaction(emojii.arrow["double_right"])
            await guild_hashmap[f"{ctx.guild}_message"].add_reaction(emojii.buttons["stop"] + emojii.special["variant"])

            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) in (
                    emojii.arrow["double_left"],
                    emojii.arrow["small_left"] + emojii.special["variant"],
                    emojii.number["1234"],
                    emojii.arrow["small_right"] + emojii.special["variant"],
                    emojii.arrow["double_right"],
                    emojii.buttons["stop"] + emojii.special["variant"]
                )

            while True:
                try:
                    emoji, member = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
                except asyncio.TimeoutError:
                    await guild_hashmap[f"{ctx.guild}_message"].delete()
                    break
                else:
                    if member.guild.id == guild_hashmap[f"{ctx.guild}_message"].guild.id:
                        if str(emoji) == emojii.arrow["double_left"]:
                            await guild_hashmap[f"{ctx.guild}_message"].remove_reaction(
                                emoji=emojii.arrow["double_left"],
                                member=self.bot.get_user(ctx.author.id)
                            )
                            guild_hashmap[f"{ctx.guild}_page"] = 1
                            await show_page(guild_hashmap[f"{ctx.guild}_message"], guild_hashmap[f"{ctx.guild}_page"])
                        elif str(emoji) == emojii.arrow["small_left"] + emojii.special["variant"]:
                            await guild_hashmap[f"{ctx.guild}_message"].remove_reaction(
                                emoji=emojii.arrow["small_left"] + emojii.special["variant"],
                                member=self.bot.get_user(ctx.author.id)
                            )
                            guild_hashmap[f"{ctx.guild}_page"] -= 1
                            if guild_hashmap[f"{ctx.guild}_page"] <= 1:
                                guild_hashmap[f"{ctx.guild}_page"] = 1
                            await show_page(guild_hashmap[f"{ctx.guild}_message"], guild_hashmap[f"{ctx.guild}_page"])
                        elif str(emoji) == emojii.number["1234"]:
                            await guild_hashmap[f"{ctx.guild}_message"].remove_reaction(
                                emoji=emojii.number["1234"],
                                member=self.bot.get_user(ctx.author.id)
                            )
                        elif str(emoji) == emojii.arrow["small_right"] + emojii.special["variant"]:
                            await guild_hashmap[f"{ctx.guild}_message"].remove_reaction(
                                emoji=emojii.arrow["small_right"] + emojii.special["variant"],
                                member=self.bot.get_user(ctx.author.id)
                            )
                            guild_hashmap[f"{ctx.guild}_page"] += 1
                            if guild_hashmap[f"{ctx.guild}_page"] >= 7:
                                guild_hashmap[f"{ctx.guild}_page"] = 7
                            await show_page(guild_hashmap[f"{ctx.guild}_message"], guild_hashmap[f"{ctx.guild}_page"])
                        elif str(emoji) == emojii.arrow["double_right"]:
                            await guild_hashmap[f"{ctx.guild}_message"].remove_reaction(
                                emoji=emojii.arrow["double_right"],
                                member=self.bot.get_user(ctx.author.id)
                            )
                            guild_hashmap[f"{ctx.guild}_page"] = 7
                            await show_page(ctx=guild_hashmap[f"{ctx.guild}_message"],
                                            page=guild_hashmap[f"{ctx.guild}_page"])
                        elif str(emoji) == emojii.buttons["stop"] + emojii.special["variant"]:
                            await guild_hashmap[f"{ctx.guild}_message"].remove_reaction(
                                emoji=emojii.buttons["stop"] + emojii.special["variant"],
                                member=self.bot.get_user(ctx.author.id)
                            )
                            await guild_hashmap[f"{ctx.guild}_message"].delete()
                            break

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
