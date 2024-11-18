from telegram import Update, ParseMode
from telegram.ext import CallbackContext

from prometheus_client import Counter

GROUP_ID = -1001631780791

anonym_counter = Counter('anonym_counter', 'Counter for anonymous command')

def send_anonym_message(update: Update, context: CallbackContext):
    """Handles the /send_anonymous command.
    Sends an anonymous message to the group
    Args:
        update: update event
        context: context passed by the handler
    """
    anonym_counter.inc()
    print(f"From: {update.message.from_user}/t Message: {update.message.text.replace('/send_anonymous', '')}")
    context.bot.send_message(chat_id=GROUP_ID, text=update.message.text.replace('/send_anonymous', ''))