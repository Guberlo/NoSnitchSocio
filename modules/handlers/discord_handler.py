from modules.data.config import Config

from telegram import Update, ParseMode
from telegram.ext import CallbackContext

import requests
import os
import random
import ast

config = Config()

def count_files(directory):
    file_count = 0
    for root, dirs, files in os.walk(directory):
        file_count += len(files)
    return file_count

def get_voice_members(update: Update, context: CallbackContext) -> str:
    users = requests.get(f'http://{config.discord_host}:{config.discord_port}')
    if users.text == '[]':
        update.message.reply_animation(getRandomEmptyGif())
    else:
        users = ast.literal_eval(users.text)
        update.message.reply_text(
            text='\n'.join(users)
        )

def getRandomEmptyGif() -> str:
    n_files = count_files(config.discord_gif_path)
    random_gif = random.randint(1, n_files)
    return open(f'{config.discord_gif_path}dead-server-{random_gif}.gif', 'rb').read()

