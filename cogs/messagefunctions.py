import asyncio
import discord
from discord.ext import commands
from database.database import getanswer, getgreeting, getily, getcompliment
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
            if substring == "winnie":  # Trigger word
                msg.remove(substring)
                msg = " ".join(msg)
                answer = await getanswer(msg)
                response = await getgreeting(msg)
                ily = await getily(msg)
                compliment = await getcompliment(msg)
                if answer:
                    await message.reply(f"{answer}!")
                if response:
                    await message.reply(f"{response} {message.author.name}!")
                elif ily:
                    await message.reply(f"{ily} {message.author.name}!")
                elif compliment:
                    await message.reply(f"{compliment} {message.author.name}!")
                await asyncio.sleep(3)


async def setup(bot):
    await bot.add_cog(messagefunctions(bot))