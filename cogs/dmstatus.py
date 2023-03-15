import discord
from discord import app_commands
from discord.ext import commands


# Needs "manage role" perms

class dmcmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="dmstatus", description="Command used to assign someone to a role for their dm status.")
    @app_commands.choices(statuses=[
        app_commands.Choice(name='Open DM', value=1),
        app_commands.Choice(name='Ask to DM', value=2),
        app_commands.Choice(name='Closed DM', value=3),
    ])
    async def dmstatus(self, interaction: discord.Interaction, statuses: app_commands.Choice[int]) -> None:
        try:
            role = discord.utils.get(interaction.guild.roles, name=statuses.name)
            if not role:
                role = await interaction.guild.create_role(name=statuses.name)
            # Checks for previous role and removes you from it if you're in it.
            openrole = discord.utils.get(interaction.guild.roles, name="Open DM")
            askrole = discord.utils.get(interaction.guild.roles, name="Ask to DM")
            closedrole = discord.utils.get(interaction.guild.roles, name="Closed DM")
            if openrole.name == role.name:
                if openrole in interaction.user.roles:
                    await interaction.response.send_message(f"You have been removed from the {statuses.name} role.",
                                                            ephemeral=True)
                    await interaction.user.remove_roles(openrole)
                else:
                    await interaction.user.add_roles(role)
                    await interaction.response.send_message(f"You have been added to the {statuses.name} role.",
                                                            ephemeral=True)
            elif askrole.name == role.name:
                if askrole in interaction.user.roles:
                    await interaction.response.send_message(f"You have been removed from the {statuses.name} role.",
                                                            ephemeral=True)
                    await interaction.user.remove_roles(askrole)
                else:
                    await interaction.user.add_roles(role)
                    await interaction.response.send_message(f"You have been added to the {statuses.name} role.",
                                                            ephemeral=True)
            elif closedrole.name == role.name:
                if closedrole in interaction.user.roles:
                    await interaction.response.send_message(f"You have been removed from the {statuses.name} role.",
                                                            ephemeral=True)
                    await interaction.user.remove_roles(closedrole)
                else:
                    await interaction.user.add_roles(role)
                    await interaction.response.send_message(f"You have been added to the {statuses.name} role.",
                                                            ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message(
                content=f"""Unable to set your role, make sure my role is higher than the role you're trying to add!""",
                ephemeral=True)


async def setup(bot):
    await bot.add_cog(dmcmd(bot))
