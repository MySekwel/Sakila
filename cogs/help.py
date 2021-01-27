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


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.page = 1
        self.page_embed = None

    async def show_page(self, ctx, page):
        if page == 1:
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
            embed.set_footer(text=time.strftime(f"Page {self.page} | %B %d, %Y | %I:%M %p"))
            self.page_embed = await ctx.edit(embed=embed)

        elif page == 2:
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
            embed.set_footer(text=time.strftime(f"Page {self.page} | %B %d, %Y | %I:%M %p"))
            self.page_embed = await ctx.edit(embed=embed)
        elif page == 3:
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
            embed.set_footer(text=time.strftime(f"Page {self.page} | %B %d, %Y | %I:%M %p"))
            self.page_embed = await ctx.edit(embed=embed)
        elif page == 4:
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
            embed.set_footer(text=time.strftime(f"Page {self.page} | %B %d, %Y | %I:%M %p"))
            self.page_embed = await ctx.edit(embed=embed)
        elif page == 5:
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
            embed.set_footer(text=time.strftime(f"Page {self.page} | %B %d, %Y | %I:%M %p"))
            self.page_embed = await ctx.edit(embed=embed)
        elif page == 6:
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
            embed.set_footer(text=time.strftime(f"Page {self.page} | %B %d, %Y | %I:%M %p"))
            self.page_embed = await ctx.edit(embed=embed)
        elif page == 7:
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
            embed.set_footer(text=time.strftime(f"Page {self.page} | %B %d, %Y | %I:%M %p"))
            self.page_embed = await ctx.edit(embed=embed)

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
            embed.set_footer(text=time.strftime(f"Page {self.page} | %B %d, %Y | %I:%M %p"))
            self.page_embed = await ctx.send(embed=embed)

            await self.page_embed.add_reaction(emojii.arrow["double_left"])
            await self.page_embed.add_reaction(emojii.arrow["small_left"] + emojii.special["variant"])
            await self.page_embed.add_reaction(emojii.number["1234"])
            await self.page_embed.add_reaction(emojii.arrow["small_right"] + emojii.special["variant"])
            await self.page_embed.add_reaction(emojii.arrow["double_right"])
            await self.page_embed.add_reaction(emojii.buttons["stop"] + emojii.special["variant"])

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

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        emoji = payload.emoji
        user = payload.user_id

        if self.bot.user.id == user:
            return

        if str(emoji) == emojii.arrow["double_left"]:
            await message.remove_reaction(emoji=emojii.arrow["double_left"], member=self.bot.get_user(user))
            self.page = 1
            await self.show_page(message, self.page)

        elif str(emoji) == emojii.arrow["small_left"] + emojii.special["variant"]:
            await message.remove_reaction(emoji=emojii.arrow["small_left"] + emojii.special["variant"],
                                          member=self.bot.get_user(user))
            self.page -= 1
            if self.page <= 1:
                self.page = 1
            await self.show_page(message, self.page)

        elif str(emoji) == emojii.number["1234"]:
            pass

        elif str(emoji) == emojii.arrow["small_right"] + emojii.special["variant"]:
            await message.remove_reaction(emoji=emojii.arrow["small_right"] + emojii.special["variant"],
                                          member=self.bot.get_user(user))
            self.page += 1
            if self.page >= 7:
                self.page = 7
            await self.show_page(message, self.page)

        elif str(emoji) == emojii.arrow["double_right"]:
            await message.remove_reaction(emoji=emojii.arrow["double_right"], member=self.bot.get_user(user))
            self.page = 7
            await self.show_page(message, self.page)

        elif str(emoji) == emojii.buttons["stop"] + emojii.special["variant"]:
            pass


def setup(bot):
    bot.add_cog(Help(bot))
