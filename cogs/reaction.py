from discord.ext import commands

from cogs import user
from main import Connection
from utils import emoji_dictionary as emojii


class React(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        emoji = payload.emoji
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        author_id = message.author.id

        if payload.user_id in (self.bot.user.id, author_id) or self.bot.user.id == author_id:
            return
        if emoji.name == emojii.heart["red"] + emojii.special["variant"]:
            if user.get_uid(message.author):
                query = f"""
                    UPDATE
                    users
                    SET
                    user_love=user_love+?
                    WHERE
                    uid={user.get_uid(message.author)}
                """
                Connection.SQL_Prepared_Cursor.execute(query, (1,))
                Connection.SQL_Handle.commit()

        if emoji.name == emojii.flower["rosette"] + emojii.special["variant"]:
            if user.get_uid(message.author):
                query = f"""
                    UPDATE
                    users
                    SET
                    user_reputation=user_reputation+?
                    WHERE
                    uid={user.get_uid(message.author)}
                """
                Connection.SQL_Prepared_Cursor.execute(query, (1,))
                Connection.SQL_Handle.commit()

    async def on_raw_reaction_remove(self, payload):
        pass


def setup(bot):
    bot.add_cog(React(bot))
