import sys
sys.stdout.reconfigure(encoding='utf-8')

import discord
import aiohttp
from bs4 import BeautifulSoup
import asyncio
import datetime
import json
import os

# =============================
# CONFIG
# =============================

TOKEN = 'SEU_TOKEN_HERE'
CHANNEL_ID = 1447719273639182457

PLAYER_URL = 'https://eagleworld.com.br/characterprofile.php?name='
ONLINE_URL = 'https://eagleworld.com.br/onlinelist.php'

INTERVAL = 60
DATA_FILE = "player_levels.json"

# =============================
# DATA
# =============================

player_levels = {}

# =============================
# UTILS
# =============================

def log(msg):
    now = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[{now}] {msg}")

def load_data():
    global player_levels
    if not os.path.exists(DATA_FILE):
        save_data()
        return

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            player_levels = json.load(f)
        log(f"{len(player_levels)} players carregados.")
    except:
        player_levels = {}
        save_data()

def save_data():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(player_levels, f, indent=4, ensure_ascii=False)

# =============================
# SCRAPING
# =============================

async def get_online_players():
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(ONLINE_URL, timeout=10) as response:
                if response.status != 200:
                    return []

                content = await response.text()
                soup = BeautifulSoup(content, 'html.parser')

                table = soup.find("table")
                if not table:
                    return []

                rows = table.find_all("tr")[1:]
                players = []

                for row in rows:
                    cols = row.find_all("td")
                    if len(cols) >= 2:
                        nick = cols[1].text.strip()
                        players.append(nick)

                return players
        except:
            return []

async def get_player_info(nick):
    url = PLAYER_URL + nick

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, timeout=10) as response:
                if response.status != 200:
                    return None

                content = await response.text()
                soup = BeautifulSoup(content, 'html.parser')

                # LEVEL
                level_tag = soup.find('td', string='Level')
                if not level_tag:
                    return None

                level_value_tag = level_tag.find_next_sibling('td')
                level = int(level_value_tag.text.strip())

                # VOCATION
                vocation_tag = soup.find('td', string='Vocation')
                vocation_value_tag = vocation_tag.find_next_sibling('td')
                vocation = vocation_value_tag.text.strip().upper()

                return level, vocation

        except:
            return None

# =============================
# CORE
# =============================

async def check_players_level(channel):
    global player_levels

    online_players = await get_online_players()
    if not online_players:
        return

    tasks = [get_player_info(nick) for nick in online_players]
    results = await asyncio.gather(*tasks)

    changed = False

    for i, nick in enumerate(online_players):

        result = results[i]
        if not result:
            continue

        new_level, vocation = result

        if nick not in player_levels:
            player_levels[nick] = new_level
            changed = True
            continue

        old_level = player_levels[nick]

        # =============================
        # LEVEL UP
        # =============================
        if new_level > old_level:

            if "SORCERER" in vocation:
                emoji = "<a:egwand:956570904861761586>"

            elif "PALADIN" in vocation:
                emoji = "<:egbow:956570654562451496>"

            elif "KNIGHT" in vocation:
                emoji = "<:egkina:1131931874483253288>"

            elif "DRUID" in vocation:
                emoji = "<a:egrod:956571084944207932>"

            else:
                emoji = ""

            msg = f"{emoji} **{nick}** upou do **{old_level}** para **{new_level}**!"
            await channel.send(msg)

        # =============================
        # ATUALIZA SEMPRE (corrige morte)
        # =============================
        if new_level != old_level:
            player_levels[nick] = new_level
            changed = True

    if changed:
        save_data()

# =============================
# DISCORD
# =============================

class MyBot(discord.Client):

    async def on_ready(self):
        log("Bot conectado!")
        load_data()

        channel = self.get_channel(CHANNEL_ID)
        if not channel:
            log("Canal não encontrado.")
            return

        while True:
            try:
                await check_players_level(channel)
            except Exception as e:
                log(f"Erro global: {e}")

            await asyncio.sleep(INTERVAL)

# =============================
# START
# =============================

intents = discord.Intents.default()
bot = MyBot(intents=intents)

if not TOKEN:
    print("ERRO: Defina a variável DISCORD_TOKEN")
else:
    bot.run(TOKEN)