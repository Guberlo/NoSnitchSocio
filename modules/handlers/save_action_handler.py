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
        command = update.message.text
        message = f"Vuoi inserire <{update.message.text[6:]}> al pool delle azioni?"
        group_id = config.bot_admin_chat

        if message:
            context.bot.send_message(chat_id=group_id,
                                                    text=message,
                                                    reply_markup=get_approve_kb()
                                                    ).message_id

def save_action_on_db(action: str, risk: str) -> bool:
    query = f"""INSERT INTO actions (description, risk, tag)
        VALUES ('{action}', '{risk}', '0')
    """

    return mysql.insert_or_update(query=query)

def handle_action_decision(update: Update, context: CallbackContext):
    decision = update.callback_query.data
    
    if decision == "approve":
        approve_action(update, context)
    elif decision == "reject": 
        reject_action(update, context)
    elif decision == "1" or decision == "2" or decision == "3":
        assign_risk_and_save(update, context)

def assign_risk_and_save(update: Update, context: CallbackContext):
    query = update.callback_query
    action = re.findall("<([^']*)>", query.message.text)[0]
    query.answer()
    if (save_action_on_db(action, query.data)):
        query.edit_message_text(text="Azione correttamente salvata su db ✅")
    else:
        query.edit_message_text(text="Errore nel salvataggio su db ❌")


def approve_action(update: Update, context: CallbackContext) -> None:
    """Approves the action sent by a user and saves it into the database."""
    query = update.callback_query
    action = re.findall("<([^']*)>", query.message.text)[0]
    risk_text = f"Seleziona il grado di rischio per lazione <{action}>"
    query.answer()
    query.edit_message_text(text=risk_text, reply_markup=get_risk_kb())

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
        InlineKeyboardButton("🔴 Rifiuta", callback_data="reject")
    ]])

def get_risk_kb() -> InlineKeyboardMarkup:
    """Generates the InlineKeyboard for the pending request
    Returns:
        new inline keyboard
    """
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("1️⃣ Basso", callback_data="1"),
        InlineKeyboardButton("2️⃣ Medio", callback_data="2"),
        InlineKeyboardButton("3️⃣ Alto", callback_data="3")
    ]])
