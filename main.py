# main.py - by DevR4yq

import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
import database

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID'))

database.init_db()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.reactions = True

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="/", intents=intents)

    async def setup_hook(self):
        cogs_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cogs')
        for filename in os.listdir(cogs_path):
            if filename.endswith('.py') and filename != '__init__.py':
                try:
                    await self.load_extension(f'cogs.{filename[:-3]}')
                    print(f'Załadowano coga: {filename}')
                except Exception as e:
                    print(f'Nie udało się załadować coga {filename}. Błąd: {e}')
        
        try:
            guild = discord.Object(id=GUILD_ID)
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
            print(f"Zsynchronizowano komendy dla serwera: {GUILD_ID}")
        except Exception as e:
            print(f"Błąd synchronizacji komend: {e}")

    async def on_ready(self):
        print(f'Zalogowano jako {self.user.name} - gotowy!')
        print('------')
        await self.change_presence(activity=discord.Game(name="Ogląda bylezdac.pl"))

bot = MyBot()

if TOKEN is None:
    print("BŁĄD: Nie znalazłem TOKENU w pliku .env! Sprawdź go, słodziaku.")
else:
    try:
        bot.run(TOKEN)
    except discord.errors.LoginFailure:
        print("BŁĄD: Zły token! Wygląda na to, że wkleiłeś coś nie tak. Skopiuj go jeszcze raz z Discord Developer Portal.")