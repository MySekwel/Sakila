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
from discord import Embed, Colour
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown, CommandOnCooldown
from disputils import BotEmbedPaginator

from utils import emoji_dictionary as emoji_dictionary


def empty_field(embed):
    embed.add_field(
        name=emoji_dictionary.special['empty'],
        value=emoji_dictionary.special['empty'],
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
    async def help(self, ctx):
        # Page 1
        page_1 = Embed(
            title='Help',
            description='List of commands:',
            colour=Colour.dark_orange()
        )
        page_1.set_thumbnail(url='https://i.imgur.com/bObV3r5.png')
        page_1.add_field(
            name='Command: !Help',
            value='**Description:** Shows the list of available commands, or specify a command.',
            inline=True
        )
        page_1.add_field(
            name='Usage:',
            value='**Example:** `!help [command]`',
            inline=True
        )
        empty_field(page_1)

        page_1.add_field(
            name='Command: !Register',
            value='**Description:** Register to the database to use the other commands.',
            inline=True
        )
        page_1.add_field(
            name='Usage:',
            value='**Example:** `!register`',
            inline=True
        )
        empty_field(page_1)

        page_1.add_field(
            name='Command: !Ping',
            value='**Description:** Shows user latency.',
            inline=True
        )
        page_1.add_field(
            name='Usage:',
            value='**Example:** `!ping [user]`',
            inline=True
        )
        empty_field(page_1)

        page_1.add_field(
            name='Command: !Work',
            value='**Description:** Mine to earn money.',
            inline=True
        )
        page_1.add_field(
            name='Usage:',
            value='**Example:** `!work`',
            inline=True
        )
        empty_field(page_1)

        page_1.add_field(
            name='Command: !Stats',
            value='**Description:** Show user stats.',
            inline=True
        )
        page_1.add_field(
            name='Usage:',
            value='**Example:** `!stats [user]`',
            inline=True
        )
        empty_field(page_1)

        page_1.add_field(
            name='Command: !Shop',
            value='**Description:** Show user shop.',
            inline=True
        )
        page_1.add_field(
            name='Usage:',
            value='**Example:** `!shop`',
            inline=True
        )
        empty_field(page_1)

        page_1.add_field(
            name='Command: !Buy',
            value='**Description:** Buy command for user shop.',
            inline=True
        )
        page_1.add_field(
            name='Usage:',
            value='**Example:** `!buy [item id]`',
            inline=True
        )
        empty_field(page_1)

        page_1.add_field(
            name='Page:',
            value=emoji_dictionary.special['empty'],
            inline=False
        )

        # Page 2
        page_2 = Embed(
            title='Help',
            description='List of commands:',
            colour=Colour.dark_orange()
        )
        page_2.set_thumbnail(url='https://i.imgur.com/bObV3r5.png')
        page_2.add_field(
            name='Command: !Credits',
            value='**Description:** Check the amount of credits you need to pay.',
            inline=True
        )
        page_2.add_field(
            name='Usage:',
            value='**Example:** `!credits`',
            inline=True
        )
        empty_field(page_2)

        page_2.add_field(
            name='Page:',
            value=emoji_dictionary.special['empty'],
            inline=False
        )

        pages = [
            page_1,
            page_2,
        ]

        paginator = BotEmbedPaginator(ctx, pages)
        await paginator.run()

    @help.error
    async def help_error(self, ctx, exc):
        if isinstance(exc, CommandOnCooldown):
            await ctx.reply(
                f"You really need help huh?" +
                f" Why don't you wait for `{exc.retry_after:,.1f}` seconds?"
            )


def setup(bot):
    bot.add_cog(Help(bot))
