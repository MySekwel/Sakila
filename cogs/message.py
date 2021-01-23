from discord.ext import commands


class Message(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        # Check if the user who sent the message is not the bot itself
        if message.author.id == self.bot.user.id:
            return

        if message.content == 'hi':
            await message.channel.send(f'Hello there <@!{message.author.id}>')
        elif message.content == 'hello':
            await message.channel.send(f'Hi there <@!{message.author.id}>')


def setup(bot):
    bot.add_cog(Message(bot))
