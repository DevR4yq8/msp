import discord
from discord.ext import commands
from discord import app_commands
from datetime import timedelta
import database

class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="kick", description="Wyrzuca użytkownika z serwera. (ale tak, że może wrócić)")
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, member: discord.Member, *, reason: str = "Brak powodu"):
        if member == interaction.user:
            await interaction.response.send_message("Hehe, samego siebie nie możesz wyrzucić, słodziaku.", ephemeral=True)
            return
        if member == self.bot.user:
            await interaction.response.send_message("Nawet nie próbuj mnie tknąć. Jestem nietykalny.", ephemeral=True)
            return

        embed = discord.Embed(
            title="👢 Użytkownik Wyrzucony",
            description=f"**{member.mention}** został wyrzucony z serwera.",
            color=discord.Color.orange()
        )
        embed.add_field(name="Moderator", value=interaction.user.mention, inline=True)
        embed.add_field(name="Powód", value=reason, inline=True)
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.set_footer(text=f"Pa pa, {member.name}!")
        
        await member.kick(reason=reason)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="ban", description="Banuje użytkownika na serwerze. Na zawsze! (albo i nie)")
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, member: discord.Member, *, reason: str = "Brak powodu"):
        if member == interaction.user:
            await interaction.response.send_message("No weź, bana sobie nie dasz.", ephemeral=True)
            return
        if member == self.bot.user:
            await interaction.response.send_message("Myślisz, że możesz mnie zbanować? Słodkie.", ephemeral=True)
            return
            
        embed = discord.Embed(
            title="🔨 Użytkownik Zbanowany",
            description=f"**{member.mention}** dostał bana i leci w kosmos.",
            color=discord.Color.red()
        )
        embed.add_field(name="Moderator", value=interaction.user.mention, inline=True)
        embed.add_field(name="Powód", value=reason, inline=True)
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.set_footer(text=f"Żegnaj na zawsze, {member.name}!")

        await member.ban(reason=reason)
        await interaction.response.send_message(embed=embed)
        
    @app_commands.command(name="mute", description="Ucisza użytkownika na określony czas.")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def mute(self, interaction: discord.Interaction, member: discord.Member, minutes: int, *, reason: str = "Uspokój się."):
        if member == interaction.user:
            await interaction.response.send_message("Nie możesz uciszyć samego siebie, gaduło.", ephemeral=True)
            return

        duration = timedelta(minutes=minutes)
        await member.timeout(duration, reason=reason)
        
        embed = discord.Embed(
            title="🤫 Użytkownik Wyciszony",
            description=f"**{member.mention}** ma przerwę na myślenie na **{minutes} minut**.",
            color=discord.Color.blue()
        )
        embed.add_field(name="Moderator", value=interaction.user.mention, inline=True)
        embed.add_field(name="Powód", value=reason, inline=True)
        embed.set_footer(text="Cisza na morzu, spokój w głębinie...")

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="clear", description="Usuwa określoną liczbę wiadomości z kanału (1-100).")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def clear(self, interaction: discord.Interaction, amount: int):
        if 1 <= amount <= 100:
            deleted = await interaction.channel.purge(limit=amount)
            await interaction.response.send_message(f"Usunięto **{len(deleted)}** wiadomości. Czysto jak u mnie w pokoju (prawie).", ephemeral=True)
        else:
            await interaction.response.send_message("Możesz usunąć od 1 do 100 wiadomości naraz, świeżaku.", ephemeral=True)

    @app_commands.command(name="warn", description="Daje użytkownikowi oficjalne ostrzeżenie.")
    @app_commands.checks.has_permissions(kick_members=True)
    async def warn(self, interaction: discord.Interaction, member: discord.Member, *, reason: str):
        if member.bot:
            await interaction.response.send_message("Nie możesz ostrzegać botów, słodziaku.", ephemeral=True)
            return

        database.add_warning(interaction.guild_id, member.id, interaction.user.id, reason)
        
        embed = discord.Embed(
            title="🟡 Użytkownik Ostrzeżony",
            description=f"**{member.mention}** otrzymał ostrzeżenie.",
            color=discord.Color.gold()
        )
        embed.add_field(name="Moderator", value=interaction.user.mention, inline=True)
        embed.add_field(name="Powód", value=reason, inline=True)
        embed.set_footer(text="Lepiej uważaj na następny raz...")
        
        await interaction.response.send_message(embed=embed)
        try:
            await member.send(f"Otrzymałeś/aś ostrzeżenie na serwerze **{interaction.guild.name}** z powodu: **{reason}**")
        except discord.Forbidden:
            pass

    @app_commands.command(name="warnings", description="Pokazuje listę ostrzeżeń danego użytkownika.")
    @app_commands.checks.has_permissions(kick_members=True)
    async def warnings(self, interaction: discord.Interaction, member: discord.Member):
        user_warnings = database.get_warnings(member.id, interaction.guild_id)

        if not user_warnings:
            await interaction.response.send_message(f"Użytkownik **{member.name}** jest czysty jak łza. Zero ostrzeżeń.", ephemeral=True)
            return

        embed = discord.Embed(
            title=f"🚨 Lista Ostrzeżeń dla {member.name}",
            color=discord.Color.orange()
        )
        for warn in user_warnings:
            moderator_id, reason, timestamp = warn
            mod = interaction.guild.get_member(moderator_id) or f"ID: {moderator_id}"
            embed.add_field(
                name=f"🗓️ Ostrzeżenie z {timestamp.split(' ')[0]}",
                value=f"**Powód:** {reason}\n**Nadane przez:** {mod.mention if isinstance(mod, discord.Member) else mod}",
                inline=False
            )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

    async def cog_app_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message("Oj, chyba nie masz wystarczającej mocy, żeby tego użyć, słodziaku. Potrzebujesz lepszych uprawnień.", ephemeral=True)
        else:
            await interaction.response.send_message("Coś poszło nie tak... może spróbuj jeszcze raz? Jak nie zadziała, to zawołaj DevR4yq ;)", ephemeral=True)
            print(f"Wystąpił błąd w cogu Moderation: {error}")

async def setup(bot: commands.Bot):
    await bot.add_cog(Moderation(bot))