from telegram import Update
from telegram.ext import CallbackContext

from modules.data.config import Config
from modules.data.database import MysqlConnection

config = Config()
mysql = MysqlConnection(config)

def get_all_actions() -> str:
    query = "SELECT description FROM actions;"
    result = mysql.select(query)
    actions = [item for t in result for item in t]

    return '\n'.join(actions)

def show_actions(update: Update, context: CallbackContext):
    actions = get_all_actions()
    update.message.reply_text(actions)