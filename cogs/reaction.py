from discord.ext import commands

from main import Connection
from utils import emoji_dictionary


class React(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        emoji = payload.emoji
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        user = payload.user_id
        author_id = message.author.id

        if user in (self.bot.user.id, author_id) or self.bot.user.id == author_id:
            return
        if str(emoji) == emoji_dictionary.heart['red'] + emoji_dictionary.special['variant']:
            query = f"""
                SELECT
                uid
                FROM
                users
                WHERE
                user_id={author_id}
            """
            Connection.SQL_Cursor.execute(query)
            result = Connection.SQL_Cursor.fetchone()
            Connection.SQL_Handle.commit()
            if result:
                query = f"""
                    UPDATE
                    users
                    SET
                    user_love=user_love+?
                    WHERE
                    user_id={author_id}
                """
                Connection.SQL_Prepared_Cursor.execute(query, (1,))
                Connection.SQL_Handle.commit()

        if str(emoji) == emoji_dictionary.flower['rosette'] + emoji_dictionary.special['variant']:
            query = f"""
                SELECT
                uid
                FROM
                users
                WHERE
                user_id={author_id}
            """
            Connection.SQL_Cursor.execute(query)
            result = Connection.SQL_Cursor.fetchone()
            Connection.SQL_Handle.commit()
            if result:
                query = f"""
                    UPDATE
                    users
                    SET
                    user_reputation=user_reputation+?
                    WHERE
                    user_id={author_id}
                """
                Connection.SQL_Prepared_Cursor.execute(query, (1,))
                Connection.SQL_Handle.commit()

    async def on_raw_reaction_remove(self, payload):
        pass


def setup(bot):
    bot.add_cog(React(bot))
