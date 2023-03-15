import asyncio
import discord
from discord.ext import commands
from database.database import getanswer
import string


class messagefunctions(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:  # If message is from itself, do nothing
            return
        if message.author.bot:  # If message is a bot, do nothing
            return
        msg = message.content.lower().translate(str.maketrans('', '', string.punctuation)).split(" ")
        for substring in msg:
            if substring is "winnie" or "winnie the pooh":  # Trigger word
                msg.remove(substring)
                msg = " ".join(msg)
                answer = await getanswer(msg)
                if answer:
                    await message.reply(f"{answer}!")
                await asyncio.sleep(3)


async def setup(bot):
    await bot.add_cog(messagefunctions(bot))