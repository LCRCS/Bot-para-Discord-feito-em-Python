"""
─────────
Carrega variáveis de ambiente e expõe as configurações globais do bot.
"""

import os
import discord
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()

# ── Tokens / Chaves ─────────────────────────────────────
DISCORD_TOKEN  = os.environ["DISCORD_TOKEN"]

# ── Cliente Discord ──────────────────────────────────────
intents = discord.Intents.default()
client  = discord.Client(intents=intents)
tree    = app_commands.CommandTree(client)
