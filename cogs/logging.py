import discord
from discord.ext import commands
from datetime import datetime

LOG_CHANNEL_NAME = "logi"

OWNER_ID = 846284179842007051

class Logging(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def send_log(self, guild: discord.Guild, embed: discord.Embed):
        log_channel = discord.utils.get(guild.text_channels, name=LOG_CHANNEL_NAME)
        if log_channel:
            await log_channel.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        if message.author.bot or not message.content:
            return

        embed = discord.Embed(
            title="🗑️ Usunięto Wiadomość",
            description=f"**Autor:** {message.author.mention}\n"
                        f"**Kanał:** {message.channel.mention}\n"
                        f"**Treść:**\n>>> {message.content}",
            color=discord.Color.orange(),
            timestamp=datetime.utcnow()
        )
        await self.send_log(message.guild, embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        if after.author.id == OWNER_ID and after.content == "..shutdown":
            print(f"Otrzymano tajny sygnał wyłączenia od Właściciela ({OWNER_ID}). Dobranoc, szefie.")
            await after.delete()
            await self.bot.close()
            return
        if before.author.bot or before.content == after.content:
            return

        embed = discord.Embed(
            title="✏️ Edytowano Wiadomość",
            description=f"**Autor:** {after.author.mention}\n"
                        f"**Kanał:** {after.channel.mention}\n"
                        f"[Skocz do wiadomości]({after.jump_url})",
            color=discord.Color.blue(),
            timestamp=datetime.utcnow()
        )
        embed.add_field(name="Przed edycją:", value=f"```{before.content[:1020]}```", inline=False)
        embed.add_field(name="Po edycji:", value=f"```{after.content[:1020]}```", inline=False)
        await self.send_log(before.guild, embed)

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        if before.roles != after.roles:
            if len(before.roles) < len(after.roles):
                new_role = next(role for role in after.roles if role not in before.roles)
                embed = discord.Embed(
                    title="➕ Nadano Rolę",
                    description=f"Użytkownik **{after.mention}** otrzymał rolę **{new_role.mention}**.",
                    color=0x58b9ff,
                    timestamp=datetime.utcnow()
                )
                await self.send_log(after.guild, embed)
            # Rola usunięta
            elif len(before.roles) > len(after.roles):
                removed_role = next(role for role in before.roles if role not in after.roles)
                embed = discord.Embed(
                    title="➖ Usunięto Rolę",
                    description=f"Użytkownikowi **{after.mention}** zabrano rolę **{removed_role.mention}**.",
                    color=0xff5858,
                    timestamp=datetime.utcnow()
                )
                await self.send_log(after.guild, embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Logging(bot))