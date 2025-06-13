import asyncio
import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import View, Button

class TicketLauncherView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="✉️ Stwórz Ticket", style=discord.ButtonStyle.secondary, custom_id="create_ticket_button")
    async def create_ticket(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer(ephemeral=True)

        category_name = "TICKETS"
        category = discord.utils.get(interaction.guild.categories, name=category_name)
        if not category:
            return await interaction.followup.send(f"Nie mogę znaleźć kategorii o nazwie `{category_name}`! Stwórz ją, proszę.", ephemeral=True)

        staff_role_name = "Staff"
        staff_role = discord.utils.get(interaction.guild.roles, name=staff_role_name)
        if not staff_role:
            return await interaction.followup.send(f"Nie mogę znaleźć roli o nazwie `{staff_role_name}`! Stwórz ją, misiu.", ephemeral=True)

        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True, attach_files=True),
            interaction.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            staff_role: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }

        channel_name = f"ticket-{interaction.user.name}"
        ticket_channel = await interaction.guild.create_text_channel(
            name=channel_name,
            category=category,
            overwrites=overwrites,
            topic=f"Ticket otwarty przez: {interaction.user.id}"
        )

        welcome_embed = discord.Embed(
            title=f"Witaj, {interaction.user.name}!",
            description=f"Dziękujemy za otwarcie ticketu. Opisz swój problem, a ktoś z ekipy `{staff_role.name}` wkrótce się tobą zajmie. \n\nAby zamknąć ten ticket, kliknij przycisk poniżej.",
            color=discord.Color.green()
        )
        await ticket_channel.send(embed=welcome_embed, view=TicketCloseView())

        await interaction.followup.send(f"Twój ticket został otwarty! Przejdź do kanału {ticket_channel.mention}", ephemeral=True)


class TicketCloseView(View):
    def __init__(self):
        super().__init__(timeout=None) 

    @discord.ui.button(label="🔒 Zamknij Ticket", style=discord.ButtonStyle.danger, custom_id="close_ticket_button")
    async def close_ticket(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message("Zamykanie ticketu za 5 sekund...", ephemeral=True)
        await asyncio.sleep(5)
        await interaction.channel.delete(reason=f"Ticket zamknięty przez {interaction.user.name}")


class Tickets(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.bot.add_view(TicketLauncherView())

    @app_commands.command(name="panel-ticketow", description="Tworzy panel do otwierania ticketów.")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def ticket_panel(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Centrum Wsparcia",
            description="Masz problem, pytanie lub sugestię? Kliknij przycisk poniżej, aby otworzyć prywatny kanał rozmowy z naszą ekipą!",
            color=discord.Color.blurple()
        )
        await interaction.channel.send(embed=embed, view=TicketLauncherView())
        await interaction.response.send_message("Panel ticketów został stworzony!", ephemeral=True)

async def setup(bot: commands.Bot):
    import asyncio
    await bot.add_cog(Tickets(bot))