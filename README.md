# Bot-para-Discord-feito-em-Python

Bot de música para Discord com player de áudio integrado, suportando YouTube, Spotify, Deezer e YouTube Music

---

## 📋 Requisitos

- Python 3.12.10 (Python 3.14+ pode ter conflitos com o Discord.py)
- FFmpeg (incluído na pasta `bin/ffmpeg/`)
- Conta no [Discord Developer Portal](https://discord.com/developers/applications)

---

## ⚙️ Instalação

**1. Clone o repositório ou copie os arquivos para uma pasta.**

**2. Crie e ative um ambiente virtual:**
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate
```

**3. Instale as dependências:**
```bash
pip install -r requirements.txt
```

**4. Configure as variáveis de ambiente:**

Crie um arquivo `.env` na raiz do projeto:
```env
DISCORD_TOKEN=seu_token_aqui
```

> Obtenha o token em [discord.com/developers/applications](https://discord.com/developers/applications) → seu app → **Bot** → **Reset Token**.

**5. Certifique-se de que o FFmpeg está no caminho correto:**
```
Bot_Discord/
└── bin/
    └── ffmpeg/
        └── ffmpeg.exe
```

---

## 🚀 Executando

```bash
python main.py
```

Ao iniciar, o bot sincronizará os slash commands automaticamente e exibirá no terminal os comandos registrados.

---

## 📁 Estrutura do Projeto

```
Bot_Discord/
├── main.py               # Ponto de entrada
├── config.py             # Configurações e clientes Discord
├── music_player.py       # Classe MusicPlayer e lógica de reprodução
├── music_commands.py     # Comandos slash de música
├── general_commands.py   # Comandos gerais (/info)
├── requirements.txt      # Dependências Python
├── .env                  # Variáveis de ambiente (não versionar)
└── bin/
    └── ffmpeg/
        └── ffmpeg.exe    # Binário do FFmpeg
```

---

## 🎮 Comandos

### 🎵 Música

| Comando | Descrição |
|---|---|
| `/play <música>` | Toca por link (YouTube, Spotify, Deezer) ou busca pelo nome |
| `/skip` | Pula a música atual |
| `/fila` | Exibe a fila de músicas |
| `/pausar` | Pausa a reprodução |
| `/continuar` | Retoma a reprodução pausada |
| `/loop` | Ativa ou desativa o loop da fila |
| `/volume <0-100>` | Ajusta o volume (persiste entre músicas) |
| `/stop` | Para a reprodução, limpa a fila e desconecta |

### ℹ️ Geral

| Comando | Descrição |
|---|---|
| `/info` | Mostra todos os comandos disponíveis |

---

## 🔧 Configuração do Bot no Discord

1. Acesse o [Discord Developer Portal](https://discord.com/developers/applications)
2. Crie uma nova aplicação e vá em **Bot**
3. Ative as intents necessárias: **Server Members Intent** e **Message Content Intent**
4. Em **OAuth2 → URL Generator**, selecione os escopos `bot` e `applications.commands`
5. Nas permissões, marque: `Connect`, `Speak`, `Send Messages`, `Embed Links`
6. Use o link gerado para convidar o bot ao seu servidor

---

## 📦 Principais Dependências

| Pacote | Uso |
|---|---|
| `discord.py` | Framework do bot Discord |
| `yt-dlp` | Extração de áudio de plataformas de streaming |
| `PyNaCl` | Criptografia necessária para áudio no Discord |
| `python-dotenv` | Leitura do arquivo `.env` |

---

## ⚠️ Observações

- O arquivo `.env` **não deve ser versionado** (adicione ao `.gitignore`)
- O volume definido via `/volume` persiste durante toda a sessão do bot no canal
- O FFmpeg precisa estar no caminho `bin/ffmpeg/ffmpeg.exe` relativo ao `music_player.py`

- README feito com auxílio do CLAUDE
