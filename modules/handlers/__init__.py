from telegram import BotCommand
from telegram.ext import Dispatcher, Updater, CommandHandler, MessageHandler, Filters

from .start_handler import start
from .dice_handler import handle_dice
from modules.filters import CommandFilter

command_filter = CommandFilter()

def add_handlers(disp: Dispatcher):
    """Adds all the needed handlers to the dispatcher
    Args:
        disp: supplied dispatcher
    """
    # Start handler
    disp.add_handler(CommandHandler("start", start))
    disp.add_handler(MessageHandler(command_filter, handle_dice))

def add_commands(updater: Updater):
    """Adds the list of commands with their description to the bot
    Args:
        updater: supplied Updater
    """
    commands = [
        BotCommand("start", "Ti fo vedere le troie")
    ]

    updater.bot.set_my_commands(commands=commands)