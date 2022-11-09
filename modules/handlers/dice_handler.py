from telegram import Update
from telegram.ext import CallbackContext

def handle_dice(update: Update, context: CallbackContext):
    context.bot.send_dice(chat_id=update.effective_chat.id, emoji='🎲')