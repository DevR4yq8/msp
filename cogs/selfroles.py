import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import View, Button

class RoleButtonView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Gracz", style=discord.ButtonStyle.primary, custom_id="role_button:Gracz")
    async def gamer_role_button(self, interaction: discord.Interaction, button: Button):
        user = interaction.user
        role = discord.utils.get(interaction.guild.roles, name="Gracz")

        if role is None:
            return await interaction.response.send_message("Nie znaleziono roli 'Gracz'. Stwórz ją, misiu.", ephemeral=True)

        if role in user.roles:
            await user.remove_roles(role)
            await interaction.response.send_message(f"Usunięto rolę **{role.name}**.", ephemeral=True)
        else:
            await user.add_roles(role)
            await interaction.response.send_message(f"Nadano rolę **{role.name}**! Slay!", ephemeral=True)

    @discord.ui.button(label="Programista", style=discord.ButtonStyle.green, custom_id="role_button:Programista")
    async def programmer_role_button(self, interaction: discord.Interaction, button: Button):
        user = interaction.user
        role = discord.utils.get(interaction.guild.roles, name="Programista")

        if role is None:
            return await interaction.response.send_message("Nie znaleziono roli 'Programista'. Dodaj ją, wymiataczu.", ephemeral=True)

        if role in user.roles:
            await user.remove_roles(role)
            await interaction.response.send_message(f"Usunięto rolę **{role.name}**.", ephemeral=True)
        else:
            await user.add_roles(role)
            await interaction.response.send_message(f"Nadano rolę **{role.name}**! Jesteś pro!", ephemeral=True)


class SelfRoles(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.bot.add_view(RoleButtonView())

    @app_commands.command(name="panel-rol", description="Tworzy panel do samodzielnego wybierania ról.")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def role_panel(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="✨ Wybierz swoje role!",
            description="Kliknij w przycisk poniżej, aby nadać lub usunąć rolę. Pokaż wszystkim, kim jesteś!",
            color=discord.Color.blurple()
        )
        
        await interaction.channel.send(embed=embed, view=RoleButtonView())
        await interaction.response.send_message("Panel ról został stworzony!", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(SelfRoles(bot))