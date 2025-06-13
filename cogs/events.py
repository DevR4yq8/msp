import discord
from discord.ext import commands

class Events(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.welcome_channel_name = "witamy" 
        self.goodbye_channel_name = "żegnamy"

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        channel = discord.utils.get(member.guild.text_channels, name=self.welcome_channel_name)
        
        if channel:
            embed = discord.Embed(
                title="👋 Nowy świeżak na pokładzie!",
                description=f"Siemanko, **{member.mention}**! Wpadaj i czuj się jak u siebie. Ogarnij zasady i baw się dobrze!",
                color=discord.Color.green()
            )
            embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
            embed.set_footer(text=f"Jesteś naszym {member.guild.member_count}. członkiem! Slay!")
            
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        channel = discord.utils.get(member.guild.text_channels, name=self.goodbye_channel_name)
        
        if channel:
            embed = discord.Embed(
                title="😢 A temu co? Ktoś uciekł...",
                description=f"**{member.name}** opuścił nasz plac zabaw. No cóż, jego strata!",
                color=discord.Color.red()
            )
            embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
            embed.set_footer(text="Mniej osób do dzielenia się twoją uwagą. ;)")

            await channel.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Events(bot))