from discord import SyncWebhook
from discord.ext import commands, tasks
from database.database import geteeyoremsg


# Needs manage messages permission

class eeyoretask(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.wait_until_ready()
        if not self.eeyore_message.is_running():
            self.eeyore_message.start()

    @tasks.loop(minutes=1440)
    async def eeyore_message(self):
        try:
            msg = await geteeyoremsg()
            webhook = SyncWebhook.from_url(url="https://discord.com/api/webhooks/1085769797561761822/IIUn2KzqoOiyqJCEHT9ndznOK_UsK7UHjwVUx1RF9twIUTK0poz2Ji5NSCqrIu40kYVn")
            webhook.send(msg)

        except Exception as e:
            print(e)


async def setup(bot):
    await bot.add_cog(eeyoretask(bot))
