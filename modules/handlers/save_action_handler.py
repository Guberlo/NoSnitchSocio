import re

from modules.data.config import Config
from modules.data.database import MysqlConnection

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext


config = Config()
mysql = MysqlConnection(config)

def send_post_to_admins(update: Update, context: CallbackContext) -> None:
        """Sends the post to the admin group, so it can be approved
        """
        message = f"Vuoi inserire '{update.message.text.split('!dado ')[1]}' al pool delle azioni?"
        group_id = config.bot_admin_chat

        if message:
            context.bot.send_message(chat_id=group_id,
                                                    text=message,
                                                    reply_markup=get_approve_kb()
                                                    ).message_id

def save_action_on_db(action: str) -> bool:
    query = f"""INSERT INTO actions (description, risk, tag)
        VALUES ('{action}', '0', '0')
    """

    return mysql.insert_or_update(query=query)

def handle_action_decision(update: Update, context: CallbackContext):
    decision = update.callback_query.data
    if decision == "approve":
        approve_action(update, context)
    else: 
        reject_action(update, context)

def approve_action(update: Update, context: CallbackContext) -> None:
    """Approves the action sent by a user and saves it into the database."""
    query = update.callback_query
    action = re.findall("'([^']*)'", query.message.text)[0]
    query.answer()
    if (save_action_on_db(action=action)):
        query.edit_message_text(text="Azione correttamente memorizzata sul database! ✅")
    else:
        query.edit_message_text(text="Errore nel salvataggio su db ❌")

def reject_action(update: Update, context: CallbackContext):
    """Rejects the action sent by a user."""
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Proposta scartata ❌")

def get_approve_kb() -> InlineKeyboardMarkup:
    """Generates the InlineKeyboard for the pending post
    Returns:
        new inline keyboard
    """
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("🟢 Accetta", callback_data="approve"),
        InlineKeyboardButton("🔴 Rifiuta", callback_data="disapprove")
    ]])