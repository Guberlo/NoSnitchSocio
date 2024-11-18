from modules.data.config import Config

from telegram import Update, ParseMode
from telegram.ext import CallbackContext

from prometheus_client import Counter, Gauge

import requests
import os
import random
import json

config = Config()

discord_counter = Counter('discord_counter', 'Counter for discord command')
voice_members_counter = Gauge('voice_members_counter', 'Counter for voice members in discord')

def count_files(directory):
    file_count = 0
    for root, dirs, files in os.walk(directory):
        file_count += len(files)
    return file_count

def get_voice_members(update: Update, context: CallbackContext) -> str:
    discord_counter.inc()
    users = requests.get(f'http://{config.discord_host}:{config.discord_port}')
    if users.text == '[]':
        update.message.reply_animation(get_random_empty_gif())
    else:
        users = json.loads(users.text)
        voice_members_counter.set(len(users))
        update.message.reply_text(
            text='\n'.join(map(lambda x: add_emoji_to_name(x), users))
        )

def get_random_empty_gif() -> str:
    n_files = count_files(config.discord_gif_path)
    random_gif = random.randint(1, n_files)
    return open(f'{config.discord_gif_path}dead-server-{random_gif}.gif', 'rb').read()

def add_emoji_to_name(user_info) -> str:
    suffix = "      "
    if user_info['muted']:
        suffix += "🤐"
    if user_info['deaf']:
        suffix += "🔇"
    if user_info['cam']:
        suffix += "📸"
    if user_info['streaming']:
        suffix += "🔴"
    
    return user_info['name'] + suffix

