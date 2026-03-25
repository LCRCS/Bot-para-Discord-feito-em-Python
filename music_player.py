"""
Classe MusicPlayer e funções auxiliares para o player de música.
"""

import asyncio
from collections import deque

import discord
import yt_dlp

from config import client

# ── Opções yt-dlp / FFmpeg ───────────────────────────────
YDL_OPTIONS = {
    "format":      "bestaudio/best",
    "quiet":       True,
    "no_warnings": True,
    "noplaylist":  True,
}

import os
FFMPEG_EXECUTABLE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bin", "ffmpeg", "ffmpeg.exe")

FFMPEG_EXECUTABLE = "bin\\ffmpeg\\ffmpeg.exe"

FFMPEG_OPTIONS = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options":        "-vn",
}


# ── Classe principal ─────────────────────────────────────
class MusicPlayer:
    """Gerencia a fila e reprodução de áudio."""

    def __init__(self):
        self.queue: deque                             = deque()
        self.current: dict | None                     = None
        self.voice_client: discord.VoiceClient | None = None
        self.loop: bool                               = False
        self.text_channel: discord.TextChannel | None = None
        self.volume: float                            = 1.0  # padrão 100%     
        


# ── Registro global de players por call────────────────
music_players: dict[int, MusicPlayer] = {}


def get_player(guild_id: int) -> MusicPlayer:
    """Retorna (ou cria) o MusicPlayer da call."""
    if guild_id not in music_players:
        music_players[guild_id] = MusicPlayer()
    return music_players[guild_id]


# ── Helpers ──────────────────────────────────────────────
async def extract_info(url: str) -> dict | None:
    """Extrai metadados de áudio via yt-dlp de forma assíncrona."""
    loop = asyncio.get_event_loop()
    with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
        try:
            info = await loop.run_in_executor(
                None, lambda: ydl.extract_info(url, download=False)
            )
            if "entries" in info:
                info = info["entries"][0]
            return {
                "title":       info.get("title", "Desconhecido"),
                "url":         info["url"],
                "duration":    info.get("duration", 0),
                "webpage_url": info.get("webpage_url", url),
                "thumbnail":   info.get("thumbnail"),
                "uploader":    info.get("uploader", ""),
            }
        except Exception as e:
            print(f"[yt-dlp] Erro: {e}")
            return None


def fmt_dur(seconds: int) -> str:
    """Formata segundos em MM:SS ou HH:MM:SS."""
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    return f"{h:02}:{m:02}:{s:02}" if h else f"{m:02}:{s:02}"


def now_playing_embed(track: dict, queue_len: int) -> discord.Embed:
    """Mostra o 'Tocando agora' e o conteúdo tocado."""
    embed = discord.Embed(
        title="▶ Tocando agora",
        description=f"**[{track['title']}]({track['webpage_url']})**",
        color=discord.Color.green(),
    )
    if track.get("thumbnail"):
        embed.set_thumbnail(url=track["thumbnail"])
    if track.get("uploader"):
        embed.add_field(name="Canal",   value=track["uploader"],          inline=True)
    embed.add_field(name="Duração",     value=fmt_dur(track["duration"]), inline=True)
    embed.add_field(name="Na fila",     value=str(queue_len),             inline=True)
    return embed


async def play_next(guild_id: int):
    """Toca o próximo item da fila (chamado automaticamente após cada faixa)."""
    player  = get_player(guild_id)
    channel = player.text_channel

    if player.loop and player.current:
        player.queue.appendleft(player.current)

    if not player.queue:
        player.current = None
        if channel:
            await channel.send("✅ Fila finalizada! Use `/play` para tocar mais músicas.")
        return

    player.current = player.queue.popleft()
    source = discord.FFmpegPCMAudio(player.current["url"], executable=FFMPEG_EXECUTABLE, **FFMPEG_OPTIONS)
    source = discord.PCMVolumeTransformer(source, volume=0.8)

    def after_play(error):
        if error:
            print(f"[player] Erro: {error}")
        asyncio.run_coroutine_threadsafe(play_next(guild_id), client.loop)

    player.voice_client.play(source, after=after_play)

    if channel:
        await channel.send(embed=now_playing_embed(player.current, len(player.queue)))
