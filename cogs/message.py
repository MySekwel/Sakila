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

from utils import emoji_dictionary


class Message(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.deleter_message = None
        self.deleter_name = None
        self.deleter_tag = None

    @commands.Cog.listener()
    async def on_message(self, message):
        # Check if the user who sent the message is not the bot itself
        if message.author.id == self.bot.user.id:
            return
        if message.content.endswith('!!!'):
            await message.channel.trigger_typing()
            await asyncio.sleep(2)
            await message.reply('qiqil?')
        if message.content in ('hi', 'Hi'):
            await message.add_reaction(emoji_dictionary.hand['wave'])
            await message.channel.trigger_typing()
            await asyncio.sleep(2)
            await message.reply(f'Hello there {message.author.mention}')
        elif message.content in ('hello', 'Hello'):
            await message.channel.trigger_typing()
            await message.add_reaction(emoji_dictionary.hand['wave'])
            await asyncio.sleep(2)
            await message.reply(f'Hi there {message.author.mention}')
        elif message.content == 'snoipe':
            embed = Embed(
                title='Boom Headshot!',
                description=f"**Message:** `{self.deleter_message}`",
                colour=Colour.green()
            )
            embed.set_thumbnail(
                url='https://cdn.discordapp.com/attachments/799655646722523166/803568246045147156/d9atvs2-6c8bcc70-1cf4-412f-9ac3-f9538e443c7a.png')
            time = datetime.datetime.now()
            embed.set_footer(text=str(time))
            embed.set_author(name=self.deleter_name + "#" + str(self.deleter_tag))
            await message.channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        self.deleter_message = message.content
        self.deleter_name = message.author.name
        self.deleter_tag = message.author.discriminator


def setup(bot):
    bot.add_cog(Message(bot))
