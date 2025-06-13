import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import random
import re
from datetime import datetime, timedelta

class Giveaway(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    @app_commands.command(name="giveaway", description="Rozpoczyna nowy giveaway!")
    @app_commands.describe(minutes="Na ile minut?", prize="Jaka jest nagroda?", winners="Ilu szczęśliwców wygrywa?")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def giveaway(self, interaction: discord.Interaction, minutes: int, prize: str, winners: int = 1):
        if winners < 1:
            await interaction.response.send_message("Liczba zwycięzców musi być co najmniej 1, słodziaku.", ephemeral=True)
            return

        end_time = datetime.utcnow() + timedelta(minutes=minutes)

        embed = discord.Embed(
            title="🎉 GIVEAWAY 🎉",
            description=f"**Nagroda:** {prize}\n"
                        f"**Wygrywa:** {winners} {'osoba' if winners == 1 else 'osoby'}\n"
                        f"**Aby wziąć udział, kliknij reakcję 🎉 poniżej!**",
            color=discord.Color.gold(),
            timestamp=end_time
        )
        embed.set_footer(text=f"Kończy się")
        embed.set_author(name=f"Sponsoruje: {interaction.user.name}", icon_url=interaction.user.avatar.url)

        giveaway_message = await interaction.channel.send(embed=embed)
        await giveaway_message.add_reaction("🎉")

        await interaction.response.send_message(f"Giveaway na **{prize}** wystartował! Powodzenia!", ephemeral=True)

        await asyncio.sleep(minutes * 60)

        try:
            updated_message = await interaction.channel.fetch_message(giveaway_message.id)
        except discord.NotFound:
            await interaction.channel.send("Wiadomość giveaway'a została usunięta. Konkurs anulowany.")
            return

        reaction = discord.utils.get(updated_message.reactions, emoji="🎉")
        if reaction is None:
             await interaction.channel.send(f"Co jest? Nikt nie wziął udziału w konkursie na **{prize}**?!", embed=None)
             return

        users = [user async for user in reaction.users() if not user.bot]
        
        if not users:
            await interaction.channel.send(f"Nikt nie wziął udziału w konkursie na **{prize}**... no cóż!", embed=None)
            return
        
        if len(users) < winners:
            winner_list = users
        else:
            winner_list = random.sample(users, k=winners)

        winner_mentions = ", ".join([winner.mention for winner in winner_list])

        winner_embed = discord.Embed(
            title="🎉 ZWYCIĘZCY GIVEAWAY'A 🎉",
            description=f"Gratulacje! Zwycięzcy konkursu na **{prize}** to:\n\n{winner_mentions}\n\n"
                        f"[Skocz do giveaway'a]({giveaway_message.jump_url})",
            color=discord.Color.green()
        )
        await interaction.channel.send(content=f"Gratulacje, {winner_mentions}!", embed=winner_embed)

        ended_embed = updated_message.embeds[0]
        ended_embed.description = f"**Nagroda:** {prize}\n**Zakończony!** Wygrali: {winner_mentions}"
        ended_embed.color = discord.Color.dark_grey()
        await updated_message.edit(embed=ended_embed)

    @app_commands.command(name="reroll", description="Losuje nowego zwycięzcę zakończonego giveaway'a.")
    @app_commands.describe(message_id="ID wiadomości z zakończonym giveawayem")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def reroll(self, interaction: discord.Interaction, message_id: str):
        try:
            giveaway_message = await interaction.channel.fetch_message(int(message_id))
        except (discord.NotFound, ValueError):
            return await interaction.response.send_message("Nie mogę znaleźć wiadomości o takim ID. Upewnij się, że ID jest poprawne i że używasz komendy na tym samym kanale co giveaway.", ephemeral=True)

        reaction = discord.utils.get(giveaway_message.reactions, emoji="🎉")
        if reaction is None:
            return await interaction.response.send_message("Ta wiadomość nie wygląda jak giveaway. Brak reakcji 🎉.", ephemeral=True)

        participants = [user async for user in reaction.users() if not user.bot]
        if not participants:
            return await interaction.response.send_message("Nikt nie wziął udziału w tym giveawayu.", ephemeral=True)

        if giveaway_message.embeds:
            embed_desc = giveaway_message.embeds[0].description
            previous_winners_ids = [int(id_str) for id_str in re.findall(r'<@(\d+)>', embed_desc)]
            eligible_participants = [user for user in participants if user.id not in previous_winners_ids]
            if not eligible_participants:
                return await interaction.response.send_message("Wszyscy uczestnicy już wygrali! Nie ma kogo wylosować.", ephemeral=True)
        else:
            eligible_participants = participants

        new_winner = random.choice(eligible_participants)

        reroll_embed = discord.Embed(
            title="🎲 REROLL 🎲",
            description=f"Nowym zwycięzcą jest **{new_winner.mention}**! Gratulacje!\n"
                        f"[Skocz do oryginalnego giveaway'a]({giveaway_message.jump_url})",
            color=discord.Color.blue()
        )
        await interaction.response.send_message(content=f"Nowa runda losowania! Gratulacje, {new_winner.mention}!", embed=reroll_embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Giveaway(bot))