import random

from telegram import Update
from telegram.ext import CallbackContext

from modules.data.config import Config
from modules.data.database import MysqlConnection
from modules.handlers.save_action_handler import send_post_to_admins
from prometheus_client import Counter


config = Config()
mysql = MysqlConnection(config)

dice_counter = Counter('dice_counter', 'Counts the number of dice commands issued')
dice_queries_counter = Counter('dice_queries_counter', 'Counts the number of queries issued within the dice command')

prefix = "Se esce"
COMMAND = "!dado"

def get_random_action() -> str:
    query = f"SELECT id FROM {config.db_database}.actions"
    result = mysql.select(query)
    dice_queries_counter.inc()
    ids = [item for t in result for item in t]
    
    query = f"SELECT description FROM {config.db_database}.actions a WHERE a.id={random.choice(ids)}"
    description = mysql.select(query)
    dice_queries_counter.inc()
    return description[0][0]

def handle_dice(update: Update, context: CallbackContext):
    dice_counter.inc()
    if update.message.text == COMMAND or update.message.text == COMMAND + " random":
        random_action = get_random_action()
        update.message.reply_text(f"{prefix} {random.randint(1,6)} {random_action}")
        context.bot.send_dice(chat_id=update.effective_chat.id, emoji='🎲')
    else:
        action = update.message.text.split("!dado ")[1]
        update.message.reply_text(f"{prefix} {random.randint(1,6)} {action}")
        context.bot.send_dice(chat_id=update.effective_chat.id, emoji='🎲')
        send_post_to_admins(update, context)