from discord import Embed, Colour
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown, CommandOnCooldown


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Command: Help
    # Description: Shows the list of available commands.
    # Cooldown: 5 seconds
    @commands.command()
    @cooldown(1, 5, BucketType.user)
    async def help(self, ctx):
        embed = Embed(
            title='Help',
            description='List of commands:',
            colour=Colour.dark_orange()
        )
        embed.set_thumbnail(url='https://i.imgur.com/bObV3r5.png')
        embed.add_field(
            name='Command: !Help',
            value='**Description:** Shows the list of available commands.',
            inline=False
        )
        embed.add_field(
            name='Command: !Register',
            value='**Description:** Register to the database to use the other commands.',
            inline=False
        )
        embed.add_field(
            name='Command: !Ping',
            value='**Description:** Shows user latency.',
            inline=False
        )
        embed.add_field(
            name='Command: !Work',
            value='**Description:** Mine to earn money.',
            inline=False
        )
        embed.add_field(
            name='Command: !Stats',
            value='**Description:** Show user stats.',
            inline=False
        )
        embed.add_field(
            name='Command: !Shop',
            value='**Description:** Show user shop.',
            inline=False
        )
        embed.add_field(
            name='Command: !Buy',
            value='**Description:** Buy command for user shop.',
            inline=False
        )
        await ctx.send(embed=embed)

    @help.error
    async def help_error(self, ctx, exc):
        if isinstance(exc, CommandOnCooldown):
            await ctx.send(
                f"Hey <@!{ctx.author.id}> you really need help huh?" +
                f" Why don't you wait for `{exc.retry_after:,.1f}` seconds?"
            )


def setup(bot):
    bot.add_cog(Help(bot))
