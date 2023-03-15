import discord
from discord import app_commands
from discord.ext import commands
from util.dbsetget import dbget, dbset

"Needs pingroleid column in db"


class pingcmd(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Slash command to add people to the Ping role.")
    async def ping(self, interaction: discord.Interaction):
        try:
            prole = await dbget(interaction.guild.id, "Winnie", "pingroleid")
            role = discord.utils.get(interaction.guild.roles, id=prole[0])
            if role:
                if role in interaction.user.roles:

                    await interaction.response.send_message(
                        content=f"""You're already in the role {role.name}.""",
                        ephemeral=True)
                else:
                    await interaction.user.add_roles(role)
                    await interaction.response.send_message(
                        content=f"""You have been added to role {role.name}.""",
                        ephemeral=True)
            else:
                await interaction.response.send_message(content=f"""No ping role exists.""",
                                                        ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message(content=f"""Unable to set your role, make sure my role is higher 
            than the role you're trying to add!""",
                                                    ephemeral=True)

    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.command(name="setpingrole", description="Slash command to set the Ping role.")
    async def setping(self, interaction: discord.Interaction, role: discord.Role):
        try:
            await dbset(interaction.guild.id, "Winnie", "pingroleid", role.id)
            await interaction.response.send_message(content=f"""Ping role has been set to {role.name}""",
                                                    ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.command(name="resetpingrole", description="Slash command to reset the Ping role.")
    async def resetping(self, interaction: discord.Interaction):
        try:
            await dbset(interaction.guild.id, "Winnie", "pingroleid", 0)
            await interaction.response.send_message(f"Ping Role config has been reset.", ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @setping.error
    @ping.error
    @resetping.error
    async def onerror(self, interaction: discord.Interaction, error: app_commands.MissingPermissions):
        await interaction.response.send_message(content=error,
                                                ephemeral=True)


async def setup(bot):
    await bot.add_cog(pingcmd(bot))
