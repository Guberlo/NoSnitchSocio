from telegram import BotCommand
from telegram.ext import Dispatcher, Updater, CommandHandler, MessageHandler, CallbackQueryHandler

from .start_handler import start
from .dice_handler import handle_dice
from .help_handler import help
from .anonym_handler import send_anonym_message
from .actions_list_handler import show_actions
from .save_action_handler import handle_action_decision
from modules.filters import DiceCommandFilter, ListCommandFilter, AnonymousCommandFilter

dice_filter = DiceCommandFilter()
list_filter = ListCommandFilter()

def add_handlers(disp: Dispatcher):
    """Adds all the needed handlers to the dispatcher
    Args:
        disp: supplied dispatcher
    """
    # Start handler
    disp.add_handler(CommandHandler("start", start))
    disp.add_handler(CommandHandler("help", help))
    disp.add_handler(CommandHandler("send_anonymous", send_anonym_message))
    disp.add_handler(MessageHandler(dice_filter, handle_dice))
    disp.add_handler(MessageHandler(list_filter, show_actions))

    # Callback handlers
    disp.add_handler(CallbackQueryHandler(handle_action_decision))


def add_commands(updater: Updater):
    """Adds the list of commands with their description to the bot
    Args:
        updater: supplied Updater
    """
    commands = [
        BotCommand("start", "Nicola Mattiuzzo ti devasto!")
    ]

    updater.bot.set_my_commands(commands=commands)