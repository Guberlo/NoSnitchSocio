from telegram import BotCommand
from telegram.ext import Dispatcher, Updater, CommandHandler, MessageHandler, CallbackQueryHandler

from .start_handler import start
from .dice_handler import handle_dice
from .slot_handler import handle_slot
from .help_handler import help
from .anonym_handler import send_anonym_message
from .actions_list_handler import show_actions, handle_actions_pagination_callback
from .save_action_handler import handle_action_decision
from .discord_handler import get_voice_members
from .toniparro_handler import get_top_link, handle_names_pagination_callback

from modules.utils.message_paginator import handle_keyboard_closure

from modules.filters import DiceCommandFilter, ListCommandFilter, AnonymousCommandFilter, SlotCommandFilter, DiscordCommandFilter, ToniparroCommandFilter

dice_filter = DiceCommandFilter()
list_filter = ListCommandFilter()
slot_filter = SlotCommandFilter()
discord_filter = DiscordCommandFilter()
toniparro_filter = ToniparroCommandFilter()

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
    disp.add_handler(MessageHandler(slot_filter, handle_slot))
    disp.add_handler(MessageHandler(discord_filter, get_voice_members))
    disp.add_handler(MessageHandler(toniparro_filter, get_top_link))

    # Callback handlers
    disp.add_handler(CallbackQueryHandler(handle_actions_pagination_callback, pattern='^action#'))
    disp.add_handler(CallbackQueryHandler(handle_names_pagination_callback, pattern='^name#'))
    disp.add_handler(CallbackQueryHandler(handle_keyboard_closure, pattern='^closeKeyboard'))
    disp.add_handler(CallbackQueryHandler(handle_action_decision))


def add_commands(updater: Updater):
    """Adds the list of commands with their description to the bot
    Args:
        updater: supplied Updater
    """
    commands = [
        BotCommand("start", "Non serve a nulla, Nicola Mattiuzzo ti devasto!"),
        BotCommand("help", "Questo ti fa vedere come usare il dado"),
        BotCommand("send_anonymous", "Questo per mandare i messaggi anonimi!!"),
        BotCommand("dado", "Questo per fare cose pazze con dado"),
        BotCommand("slot", "Questo per fare cose più pazze con slot"),
        BotCommand("discord", "Questo per vedere chi c'è su discord!!!")
    ]

    updater.bot.set_my_commands(commands=commands)