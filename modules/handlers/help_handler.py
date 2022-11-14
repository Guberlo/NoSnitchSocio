from telegram import Update, ParseMode
from telegram.ext import CallbackContext
from modules.files.markdown import read_md

ASCII_ART = """
                   (( _______
         _______     /\O    O\
        /O     /\   /  \      \
       /   O  /O \ / O  \O____O\ ))
    ((/_____O/    \\    /O     /
      \O    O\    / \  /   O  /
       \O    O\ O/   \/_____O/
        \O____O\/ )) mrf      ))
      (("""

def help(update: Update, context: CallbackContext):
    """Handles the /help command.
    Sends an help message
    Args:
        update: update event
        context: context passed by the handler
    """
    text = read_md("help")
    context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=ParseMode.MARKDOWN_V2, disable_web_page_preview=True)
    context.bot.send_message(chat_id=update.effective_chat.id, text=ASCII_ART)