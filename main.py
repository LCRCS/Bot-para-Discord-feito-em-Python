"""
Ponto de entrada do bot.
Importa os módulos de comandos
E inicia o Bot.
"""

import discord

from config import client, tree, DISCORD_TOKEN
""""
 Importar os módulos de comandos faz com que os decoradores @tree.command sejam executados e os comandos sejam registrados.
 O comentário noqa: F401 é para evitar avisos de importação não utilizada, já que a função principal desses imports é registrar os comandos via decoradores.
 A ordem de importação pode ser importante se houver dependências entre os comandos, mas aqui  não há, então a ordem é indiferente.
 Se houver comandos que dependem de outros, certifique-se de importar na ordem correta para que os decoradores sejam processados na sequência necessária.  
 @tree.command sejam executados e os comandos sejam registrados.
"""
import music_commands      # noqa: F401
import general_commands    # noqa: F401


@client.event
async def on_ready():
    await tree.sync()
    print(f"Bot online como {client.user}")
    print(f"   Comandos: {[c.name for c in tree.get_commands()]}")
    await client.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.listening,
            name="/play"
        )
    )


if __name__ == "__main__":
    client.run(DISCORD_TOKEN)
