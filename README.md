# Nawa 2.0 – Discord Bot

Nawa 2.0 is a Discord bot built with `discord.py` that recreates the personalities of characters from the Korean light novel “Nawa Horang-nim” in a Discord server.

## Features

### Mini-games and engagement

- Several interactive mini-games.
- Level and experience system for active users.
- Character-based responses that reflect the personalities of Rangi, Chii, and Sehee.

### Music

- Music playback using Wavelink and Lavalink.
- Supports standard queue controls (play, skip, pause, resume, etc.).
- Updated as needed to stay compatible with recent Discord changes.

### Server and user management

- Basic moderation and utility commands to help manage a server.
- User-related commands for simple management tasks.
- Most commands are implemented as slash commands.

### Virtual stock market

- In-server virtual stock system where users can buy and sell simulated assets.
- Designed to give users something persistent to interact with over time.

## Chatbot behavior

- The bot defines different speaking styles for Rangi, Chii, and Sehee.
- Uses `on_message` to listen to user messages and reply in character, not only to explicit commands.

## Data storage

- User and server data are stored as per-server JSON files.
- Each guild has its own JSON file so configuration and user state are kept separate per server.

## Tech stack

- Language: Python
- Library: `discord.py`
- Audio: Wavelink, Lavalink
- Storage: JSON files (per server)

## Getting started

_Example setup steps — adjust to match your actual project structure._

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/Nawa_2.0.git
   cd Nawa_2.0
   
2. Install dependencies:

   ```bash
   pip install -r requirements.txt

3. Configure environment:

   - Set `DISCORD_TOKEN`.
   - Set up and start a Lavalink server (see the official Lavalink documentation for download and `java -jar Lavalink.jar` usage).
   - Configure Wavelink to connect to your Lavalink node (host, port, password).
   - Adjust any bot or character settings if needed.
     
   Adjust any bot or character settings if needed.

4. Run the bot:

   ```bash
   python3 bot.py

# Nawa_2.0
나와 아해들 2.0 디스코드 봇은 discord py를 기반으로 뒀으며 대한민국 라이트노벨 "나와 호랑이님" 캐릭터들의 성격을 재현한 디스코드 봇입니다.

# 기능
해당봇은 다양한 미니게임, 음악, 서버 관리, 유저관리, 레벨업, 주식등 다양한 기능이 있으며 "랑이","치이","세희" 캐릭터들의 말투를 이용한 챗봇기능을 갖추었습니다.

# 명령어
대부분의 명령어는 슬래시 커맨드를 사용하고 있으며 대답 기능은 자연스러움을 위해 on_message를 사용하여 유저의 메세지를 인식하게 만들었습니다.

# 음악기능
해당봇의 음악 기능은 wavelink와 lavalink를 이용했으며, 지속적으로 최신버전으로 업데이트를 하고있습니다.
