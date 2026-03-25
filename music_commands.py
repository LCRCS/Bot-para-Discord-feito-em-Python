"""
Comandos relacionados ao player de música (/play, /skip, /fila, etc.).
Registra os comandos na árvore do Discord importada de config.py.
"""

import discord
from discord import app_commands

from config import tree
from music_player import (
    get_player,
    extract_info,
    fmt_dur,
    now_playing_embed,
    play_next,
)


@tree.command(name="play", description="Toca uma música (link ou busca no YouTube)")
@app_commands.describe(musica="URL ou nome da música")
async def play(interaction: discord.Interaction, musica: str):
    await interaction.response.defer()

    if not interaction.user.voice:
        await interaction.followup.send("❌ Entre em um canal de voz primeiro!", ephemeral=True)
        return

    voice_channel       = interaction.user.voice.channel
    player              = get_player(interaction.guild_id)
    player.text_channel = interaction.channel

    if not player.voice_client or not player.voice_client.is_connected():
        player.voice_client = await voice_channel.connect()
    elif player.voice_client.channel != voice_channel:
        await player.voice_client.move_to(voice_channel)

    query = musica if musica.startswith("http") else f"ytsearch:{musica}"
    await interaction.followup.send(f"Procurando a boa chefia👍: `{musica}`...")

    info = await extract_info(query)
    if not info:
        await interaction.channel.send("❌ Não foi possível carregar essa música.")
        return

    player.queue.append(info)

    if not player.voice_client.is_playing():
        await play_next(interaction.guild_id)
    else:
        await interaction.channel.send(
            f"➕ **{info['title']}** ({fmt_dur(info['duration'])}) adicionado — "
            f"posição **{len(player.queue)}** na fila."
        )


@tree.command(name="skip", description="Pula a música atual")
async def skip(interaction: discord.Interaction):
    player = get_player(interaction.guild_id)
    if not player.voice_client or not player.voice_client.is_playing():
        await interaction.response.send_message("❌ Nenhuma música tocando.", ephemeral=True)
        return
    player.voice_client.stop()
    await interaction.response.send_message("⏭ Pulando...")


@tree.command(name="fila", description="Mostra a fila de músicas")
async def fila(interaction: discord.Interaction):
    player = get_player(interaction.guild_id)
    embed  = discord.Embed(title="🎵 Fila de músicas", color=discord.Color.blurple())

    if player.current:
        embed.add_field(
            name="▶ Tocando agora",
            value=f"[{player.current['title']}]({player.current['webpage_url']}) "
                  f"({fmt_dur(player.current['duration'])})",
            inline=False,
        )

    if player.queue:
        items = "\n".join(
            f"`{i+1}.` [{m['title']}]({m['webpage_url']}) — {fmt_dur(m['duration'])}"
            for i, m in enumerate(player.queue)
        )
        embed.add_field(name="📋 Próximas", value=items[:1024], inline=False)
    elif not player.current:
        embed.description = "A fila está vazia."

    embed.set_footer(text=f"Loop: {'✅ ativado' if player.loop else '❌ desativado'}")
    await interaction.response.send_message(embed=embed)


@tree.command(name="pausar", description="Pausa a música atual")
async def pausar(interaction: discord.Interaction):
    player = get_player(interaction.guild_id)
    if player.voice_client and player.voice_client.is_playing():
        player.voice_client.pause()
        await interaction.response.send_message("⏸ Pausado.")
    else:
        await interaction.response.send_message("❌ Nada tocando.", ephemeral=True)


@tree.command(name="continuar", description="Continua a música pausada")
async def continuar(interaction: discord.Interaction):
    player = get_player(interaction.guild_id)
    if player.voice_client and player.voice_client.is_paused():
        player.voice_client.resume()
        await interaction.response.send_message("▶ Continuando.")
    else:
        await interaction.response.send_message("❌ Nada pausado.", ephemeral=True)


@tree.command(name="loop", description="Ativa ou desativa o loop da fila")
async def loop_cmd(interaction: discord.Interaction):
    player      = get_player(interaction.guild_id)
    player.loop = not player.loop
    estado      = "✅ ativado" if player.loop else "❌ desativado"
    await interaction.response.send_message(f"🔁 Loop {estado}.")


@tree.command(name="volume", description="Ajusta o volume (0–100)")
@app_commands.describe(nivel="Volume de 0 a 100")
async def volume(interaction: discord.Interaction, nivel: int):
    if not 0 <= nivel <= 100:
        await interaction.response.send_message("❌ Use um valor entre 0 e 100.", ephemeral=True)
        return
    player = get_player(interaction.guild_id)
    player.volume = nivel / 100
    if player.voice_client and player.voice_client.source:
        player.voice_client.source.volume = player.volume
        await interaction.response.send_message(f"🔊 Volume ajustado para **{nivel}%**.")
    else:
        await interaction.response.send_message("❌ Nenhuma música tocando para ajustar o volume.", ephemeral=True)

@tree.command(name="stop", description="Para a música, limpa a fila e desconecta")
async def parar(interaction: discord.Interaction):
    player = get_player(interaction.guild_id)
    if player.voice_client:
        player.queue.clear()
        player.current = None
        player.voice_client.stop()
        await player.voice_client.disconnect()
        player.voice_client = None
    await interaction.response.send_message("⏹ Parado e fila limpa.")
