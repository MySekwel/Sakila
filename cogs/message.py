"""
Module: ./cogs/message.py
Description: Message module, includes everything that has relation to message processing.
Module Dependencies:
    > discord.ext.commands
"""
import asyncio
import datetime

from discord import Embed, Colour
from discord.ext import commands

from utils import emoji_dictionary as emojii

guild_hashmap = {}


class Message(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        # Check if the user who sent the message is not the bot itself
        if message.author.id == self.bot.user.id:
            return
        if message.content.endswith("!!!"):
            await message.channel.trigger_typing()
            await asyncio.sleep(2)
            await message.reply("qiqil?")
        if message.content.casefold() == "hi":
            await message.add_reaction(emojii.hand["wave"])
            await message.channel.trigger_typing()
            await asyncio.sleep(2)
            await message.reply(f"Hello there {message.author.mention}")
        elif message.content.casefold() == "hello":
            await message.channel.trigger_typing()
            await message.add_reaction(emojii.hand["wave"])
            await asyncio.sleep(2)
            await message.reply(f"Hi there {message.author.mention}")
        elif message.content.casefold() == "pls snipe":
            if message.guild.id == guild_hashmap[f"{message.guild}_guild_id"]:
                embed = Embed(
                    title="Boom Headshot!",
                    description=f"**Message:** `{guild_hashmap[f'{message.guild}_message']}`",
                    colour=Colour.green()
                )
                embed.set_author(icon_url=guild_hashmap[f"{message.guild}_author_avatar"],
                                 name=guild_hashmap[f"{message.guild}_author_name"] + "#" + guild_hashmap[
                                     f"{message.guild}_author_tag"])
                embed.set_thumbnail(
                    url="https://cdn.discordapp.com/attachments/799655646722523166/803568246045147156/d9atvs2-6c8bcc70-1cf4-412f-9ac3-f9538e443c7a.png")
                time = datetime.datetime.now()
                embed.set_footer(text=time.strftime("%B %d, %Y | %I:%M %p"))
                await message.channel.send(embed=embed)
            else:
                embed = Embed(
                    title="You missed!",
                    description=f"You failed to snipe the message, better luck next time!",
                    colour=Colour.red()
                )
                await message.channel.send(embed=embed)

    @commands.command()
    async def snipe(self, ctx):
        if ctx.guild.id == guild_hashmap[f"{ctx.guild}_guild_id"]:
            embed = Embed(
                title="Boom Headshot!",
                description=f"**Message:** `{guild_hashmap[f'{ctx.guild}_message']}`",
                colour=Colour.green()
            )
            embed.set_author(icon_url=guild_hashmap[f"{ctx.guild}_author_avatar"],
                             name=guild_hashmap[f"{ctx.guild}_author_name"] + "#" + guild_hashmap[
                                 f"{ctx.guild}_author_tag"])
            embed.set_thumbnail(
                url="https://cdn.discordapp.com/attachments/799655646722523166/803568246045147156/d9atvs2-6c8bcc70-1cf4-412f-9ac3-f9538e443c7a.png")
            time = datetime.datetime.now()
            embed.set_footer(text=time.strftime("%B %d, %Y | %I:%M %p"))
            await ctx.send(embed=embed)
        else:
            embed = Embed(
                title="You missed!",
                description=f"You failed to snipe the message, better luck next time!",
                colour=Colour.red()
            )
            await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        guild_hashmap[f"{message.guild}_message"] = message.content
        guild_hashmap[f"{message.guild}_author_name"] = message.author.name
        guild_hashmap[f"{message.guild}_author_tag"] = message.author.discriminator
        guild_hashmap[f"{message.guild}_author_avatar"] = message.author.avatar_url
        guild_hashmap[f"{message.guild}_guild_id"] = message.guild.id


def setup(bot):
    bot.add_cog(Message(bot))
