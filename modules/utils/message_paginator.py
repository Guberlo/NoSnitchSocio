from typing import List

from telegram import Update, InlineKeyboardButton
from telegram.ext import CallbackContext

from telegram_bot_pagination import InlineKeyboardPaginator

def split_messages(messages: List[str], page_size=15) -> List[str]:
    splitted_messages = []
    start_index = 0
    index = 0

    while start_index <= len(messages):
        end_index = min(start_index + (page_size), len(messages))
        actions_txt = '\n'.join(messages[start_index:end_index])
        splitted_messages.append(actions_txt)
        start_index = (index + 1) * page_size
        index += 1
    
    return splitted_messages

def handle_keyboard_closure(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    query.edit_message_text(
        text='Puppata al bomber 😮🍆⚽️ :))'
    )