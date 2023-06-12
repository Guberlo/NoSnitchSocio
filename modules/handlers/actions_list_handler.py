from typing import List

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from telegram_bot_pagination import InlineKeyboardPaginator

from modules.data.config import Config
from modules.data.database import MysqlConnection
from modules.utils.message_paginator import split_messages

config = Config()
mysql = MysqlConnection(config)

def get_all_actions() -> List[str]:
    query = "SELECT description FROM actions;"
    result = mysql.select(query)
    actions = [item for t in result for item in t]

    return actions

def show_actions(update: Update, context: CallbackContext):
    splitted_actions = split_messages(get_all_actions())
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

def handle_actions_pagination_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    page = int(query.data.split('#')[1])
    splitted_actions = split_messages(get_all_actions())

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

