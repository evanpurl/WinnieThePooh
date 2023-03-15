import asyncio
import datetime
import discord
from discord import app_commands, ui
from discord.ext import commands

timeout = 300  # seconds


# Needs "manage role" perms
# report-usernamediscriminator

def ticketembed(bot):
    embed = discord.Embed(description=f"When you are finished, click the close report button below. This report will "
                                      f"close in 5 minutes if no message is sent.", color=discord.Color.blue(),
                          timestamp=datetime.datetime.now())
    embed.set_author(name=bot.user.name, icon_url=bot.user.avatar)
    return embed


class ticketbuttonpanel(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Close Report", emoji="🗑️", style=discord.ButtonStyle.red,
                       custom_id="Winnie:close")
    async def close_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.channel.delete()
        except Exception as e:
            print(e)

    @commands.has_permissions(manage_channels=True)
    @discord.ui.button(label="Auto-Close Report", emoji="⏲️", style=discord.ButtonStyle.gray,
                       custom_id="Winnie:autoclose")
    async def auto_close_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            if interaction.user.guild_permissions.manage_channels:
                await interaction.response.send_message(content="Timer started.", ephemeral=True)

                def check(m: discord.Message):  # m = discord.Message.
                    return m.author.id == interaction.user.id and m.channel.id == interaction.channel.id

                try:
                    while True:
                        msg = await interaction.client.wait_for('message', check=check, timeout=timeout)
                except asyncio.TimeoutError:
                    await interaction.channel.delete()
                    return
            else:
                await interaction.response.send_message(content="You don't have permission to do that.", ephemeral=True)
        except Exception as e:
            print(e)


class ticketbutton(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Create Report", emoji="📨", style=discord.ButtonStyle.blurple,
                       custom_id="reportbutton")
    async def gray_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            existticket = discord.utils.get(interaction.guild.channels,
                                            name=f"report-{interaction.user.name.lower()}{interaction.user.discriminator}")
            if existticket:
                await interaction.response.send_message(
                    content=f"You already have an existing report you silly goose. {existticket.mention}",
                    ephemeral=True)
            else:
                overwrites = {
                    interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    interaction.user: discord.PermissionOverwrite(read_messages=True),
                    interaction.guild.me: discord.PermissionOverwrite(read_messages=True)}
                ticketcat = discord.utils.get(interaction.guild.categories, name="Reports")
                if ticketcat:
                    ticketchan = await interaction.guild.create_text_channel(
                        f"report-{interaction.user.name}{interaction.user.discriminator}", category=ticketcat,
                        overwrites=overwrites)
                    await interaction.response.send_message(content=f"Report created in {ticketchan.mention}!",
                                                            ephemeral=True)
                    await ticketchan.send(
                        content=f"{interaction.user.mention} created a report!")
                    await ticketchan.send(
                        embed=ticketembed(interaction.client),
                        view=ticketbuttonpanel())

                    def check(m: discord.Message):  # m = discord.Message.
                        return m.author.id == interaction.user.id and m.channel.id == ticketchan.id

                    try:
                        msg = await interaction.client.wait_for('message', check=check, timeout=timeout)
                    except asyncio.TimeoutError:
                        await ticketchan.delete()

                else:
                    ticketchan = await interaction.guild.create_text_channel(
                        f"report-{interaction.user.name}{interaction.user.discriminator}", overwrites=overwrites)
                    await interaction.response.send_message(content=f"Report created in {ticketchan.mention}!",
                                                            ephemeral=True)
                    await ticketchan.send(
                        content=f"{interaction.user.mention} created a Report!")
                    await ticketchan.send(
                        embed=ticketembed(interaction.client),
                        view=ticketbuttonpanel())

                    def check(m: discord.Message):  # m = discord.Message.
                        return m.author.id == interaction.user.id and m.channel.id == ticketchan.id

                    try:
                        msg = await interaction.client.wait_for('message', check=check, timeout=timeout)
                    except asyncio.TimeoutError:
                        await ticketchan.delete()
        except Exception as e:
            print(e)


def ticketmessageembed(bot):
    embed = discord.Embed(title="**Reports**",
                          description=f"Oh bother! Is someone here breaking a rule? Making you feel unsafe either in public or private? Feel free to create a report!",
                          color=discord.Color.blue(),
                          timestamp=datetime.datetime.now())
    embed.set_author(name=bot.user.name, icon_url=bot.user.avatar)
    return embed


class ticketcmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(manage_roles=True)
    @app_commands.command(name="report", description="Command used by admin to create the report message.")
    async def report(self, interaction: discord.Interaction) -> None:
        try:
            await interaction.response.send_message(embed=ticketmessageembed(self.bot), view=ticketbutton())
        except Exception as e:
            print(e)

    @report.error
    async def onerror(self, interaction: discord.Interaction, error: app_commands.MissingPermissions):
        await interaction.response.send_message(content=error,
                                                ephemeral=True)


async def setup(bot):
    await bot.add_cog(ticketcmd(bot))
    bot.add_view(ticketbutton())  # line that inits persistent view
    bot.add_view(ticketbuttonpanel())
