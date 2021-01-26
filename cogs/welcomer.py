from discord import Embed, Colour
from discord.ext import commands


class Welcomer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.join = None
        self.leave = None

    @commands.command()
    async def set(self, ctx, set_type=None):
        if set_type in ('join', 'Join'):
            for channel in ctx.guild.channels:
                if channel.name == ctx.channel.name:
                    self.join = channel
                    embed = Embed(
                        title='Channel Set',
                        description='This channel will now be the welcomer channel for joining members.',
                        colour=Colour.green()
                    )
                    await ctx.send(embed=embed)
        elif set_type in ('leave', 'Leave'):
            for channel in ctx.guild.channels:
                if channel.name == ctx.channel.name:
                    self.leave = channel
                    embed = Embed(
                        title='Channel Set',
                        description='This channel will now be the welcomer channel for leaving members.',
                        colour=Colour.green()
                    )
                    await ctx.send(embed=embed)
        else:
            embed = Embed(
                title='Usage:',
                description='`!set [join, leave]`\n**Example:** `!set join`',
                colour=Colour.red()
            )
            await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if self.join is not None:
            embed = Embed(
                title='Welcome',
                description=f'{member.mention}',
                colour=Colour.green()
            )
            embed.set_thumbnail(url=member.avatar_url)
            await self.bot.join.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if self.leave is not None:
            embed = Embed(
                title='Goodbye',
                description=f'{member.name + member.discriminator}',
                colour=Colour.green()
            )
            await self.bot.join.send(embed=embed)
            embed.set_thumbnail(url=member.avatar_url)


def setup(bot):
    bot.add_cog(Welcomer(bot))
