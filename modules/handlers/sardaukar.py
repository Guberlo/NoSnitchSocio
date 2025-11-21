from telegram import Update, ParseMode
from telegram.ext import CallbackContext
from modules.files.markdown import read_md

def sardaukar(update: Update, context: CallbackContext):
    """Handles the sardaukar command.
    Sends an audio message committed by Lhurd
    Args:
        update: update event
        context: context passed by the handler
    """
    update.message.reply_voice(voice=open('voices/sardaukar.ogg', 'rb'))