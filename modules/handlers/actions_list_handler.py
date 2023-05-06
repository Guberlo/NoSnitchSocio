from typing import List

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from telegram_bot_pagination import InlineKeyboardPaginator

from modules.data.config import Config
from modules.data.database import MysqlConnection

config = Config()
mysql = MysqlConnection(config)

def get_all_actions() -> List[str]:
    query = "SELECT description FROM actions;"
    result = mysql.select(query)
    actions = [item for t in result for item in t]

    return actions

def split_actions(actions: List[str], page_size=15) -> List[str]:
    splitted_actions = []
    start_index = 0
    index = 0

    while start_index <= len(actions):
        end_index = min(start_index + (page_size), len(actions))
        actions_txt = '\n'.join(actions[start_index:end_index])
        splitted_actions.append(actions_txt)
        start_index = (index + 1) * page_size
        index += 1
    
    return splitted_actions

def show_actions(update: Update, context: CallbackContext):
    splitted_actions = split_actions(get_all_actions())
    user_id = update.message.from_user['id']

    paginator = InlineKeyboardPaginator(
        len(splitted_actions),
        data_pattern='action#{page}'
    )

    paginator.add_after(InlineKeyboardButton('Chiudi', callback_data='closeKeyboard'))

    update.message.reply_text(
        text="Lista inviata in privato",
    )

    context.bot.send_message(
        chat_id=user_id,
        text=splitted_actions[0],
        reply_markup=paginator.markup
    )

def handle_pagination_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    page = int(query.data.split('#')[1])
    splitted_actions = split_actions(get_all_actions())

    paginator = InlineKeyboardPaginator(
        len(splitted_actions),
        current_page=page,
        data_pattern='action#{page}'
    )

    paginator.add_after(InlineKeyboardButton('Chiudi', callback_data='closeKeyboard'))

    query.edit_message_text(
        text=splitted_actions[page - 1],
        reply_markup=paginator.markup
    )

def handle_keyboard_closure(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    query.edit_message_text(
        text='Puppata al bomber 😮🍆⚽️ :))'
    )

