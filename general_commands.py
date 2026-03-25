"""
general_commands.py
───────────────────
Comandos gerais do bot (/info).
"""

import discord

from config import tree
from music_player import get_player

@tree.command(name="info", description="Mostra todos os comandos disponíveis")
async def info(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Bot de Música Supremo",
        description="Player de música, Spotify, Deezer, Youtube Music.",
        name="🎵 Música",
        value=(
            "`/play` — Toca por link ou busca\n"
            "`/skip` — Pula a atual\n"
            "`/fila` — Mostra a fila\n"
            "`/pausar` / `/continuar`\n"
            "`/loop` — Ativa/desativa loop\n"
            "`/volume` — Ajusta o volume\n"
            "`/parar` — Para e desconecta"
        ),
        inline=True,
    )
    player = get_player(interaction.guild_id)
    embed.set_footer(
        text=f"Músicas na fila: {len(player.queue)}"
    )
    await interaction.response.send_message(embed=embed)
