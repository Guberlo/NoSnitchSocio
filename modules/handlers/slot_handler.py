import random

from telegram import Update
from telegram.ext import CallbackContext

from prometheus_client import Counter

from modules.data.config import Config
from modules.data.database import MysqlConnection
from modules.handlers.save_action_handler import send_post_to_admins


config = Config()
mysql = MysqlConnection(config)
slot_counter = Counter('slot_counter', 'Counter for slot command')

prefix = "Se esce"
COMMAND = "!slot"
symbols = ['7️⃣', '🍒', '🍋','⬛️']

def get_random_action() -> str:
    query = f"SELECT id FROM {config.db_database}.actions"
    result = mysql.select(query)
    ids = [item for t in result for item in t]
    
    query = f"SELECT description FROM {config.db_database}.actions a WHERE a.id={random.choice(ids)}"
    description = mysql.select(query)
    return description[0][0]

def handle_slot(update: Update, context: CallbackContext):
    slot_counter.inc()
    if update.message.text == COMMAND or update.message.text == COMMAND + " random":
        random_action = get_random_action()
        update.message.reply_text(f"{prefix} '{random.choice(symbols)} {random.choice(symbols)} {random.choice(symbols)}' {random_action}")
        context.bot.send_dice(chat_id=update.effective_chat.id, emoji='🎰')
    else:
        action = update.message.text.split("!slot ")[1]
        update.message.reply_text(f"{prefix} '{random.choice(symbols)} {random.choice(symbols)} {random.choice(symbols)}' {action}")
        context.bot.send_dice(chat_id=update.effective_chat.id, emoji='🎰')
        send_post_to_admins(update, context)