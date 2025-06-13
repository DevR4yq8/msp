import discord
from discord.ext import commands
from collections import defaultdict
import time
from datetime import timedelta

BANNED_WORDS = ["kurde", "cholera", "głupi", "idiota"]

SPAM_THRESHOLD = 5
SPAM_TIMEFRAME = 5.0  # w sekundach

class AutoMod(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.spam_control = defaultdict(list)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        if message.author.guild_permissions.manage_messages:
            return

        content_lower = message.content.lower()
        if any(word in content_lower for word in BANNED_WORDS):
            try:
                await message.delete()
                await message.channel.send(f"{message.author.mention}, pilnuj słownictwa, słodziaku! ;)", delete_after=5)
                print(f"Usunięto wulgarną wiadomość od {message.author.name}")
            except discord.errors.Forbidden:
                print(f"Nie mogłem usunąć wulgarnej wiadomości - brak uprawnień na kanale {message.channel.name}")
            return
            
        current_time = time.time()
        
        self.spam_control[message.author.id] = [t for t in self.spam_control[message.author.id] if current_time - t < SPAM_TIMEFRAME]
        
        self.spam_control[message.author.id].append(current_time)
        
        if len(self.spam_control[message.author.id]) > SPAM_THRESHOLD:
            try:
                duration = timedelta(seconds=60)
                await message.author.timeout(duration, reason="Spamowanie na kanale.")
                await message.channel.send(f"{message.author.mention} ląduje na karnej ławce za spam! Cisza na 60 sekund.", delete_after=10)
                print(f"Wyciszono {message.author.name} za spam.")
                self.spam_control[message.author.id].clear()
            except discord.errors.Forbidden:
                print(f"Nie mogłem wyciszyć {message.author.name} za spam - brak uprawnień.")

async def setup(bot: commands.Bot):
    await bot.add_cog(AutoMod(bot))