"""
Module: ./cogs/message.py
Description: Message module, includes everything that has relation to message processing.
Module Dependencies:
    > discord.ext.commands
"""
import asyncio

from discord.ext import commands

from utils import emoji_dictionary


class Message(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
            await message.reply(f'Hello there <@!{message.author.id}>')
        elif message.content in ('hello', 'Hello'):
            await message.channel.trigger_typing()
            await message.add_reaction(emoji_dictionary.hand['wave'])
            await asyncio.sleep(2)
            await message.reply(f'Hi there <@!{message.author.id}>')


def setup(bot):
    bot.add_cog(Message(bot))
