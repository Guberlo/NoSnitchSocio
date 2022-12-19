from telegram import Update, ParseMode
from telegram.ext import CallbackContext

GROUP_ID = -1631780791

def send_anonym_message(update: Update, context: CallbackContext):
    """Handles the /send_anonymous command.
    Sends an anonymous message to the group
    Args:
        update: update event
        context: context passed by the handler
    """

    context.bot.send_message(chat_id=GROUP_ID, text=update.message.text.replace('/send_anonym', ''))