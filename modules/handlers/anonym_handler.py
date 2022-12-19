from telegram import Update, ParseMode
from telegram.ext import CallbackContext

GROUP_ID = -1001863199799

def send_anonym_message(update: Update, context: CallbackContext):
    """Handles the /send_anonym command.
    Sends an anonymous message to the group
    Args:
        update: update event
        context: context passed by the handler
    """

    context.bot.send_message(chat_id=GROUP_ID, text=update.message.text)