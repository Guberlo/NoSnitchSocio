from telegram import Update
from telegram.ext import CallbackContext

def generate_action(type: str, update: Update, context: CallbackContext):
    # Based on the type generate an action calling the other method