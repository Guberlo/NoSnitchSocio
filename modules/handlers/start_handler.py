from telegram import Update
from telegram.ext import CallbackContext

def start(update: Update, context: CallbackContext):
    """Handles the /start command.
    Sends a welcoming message
    Args:
        update: update event
        context: context passed by the handler
    """
    context.bot.send_message(chat_id=update.effective_chat.id, text="Nico7 Vinsmoke vado ad Utrecht lo disintegroo")