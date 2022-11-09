import logging

from telegram.ext import Updater

from modules.handlers import add_commands, add_handlers

TOKEN_TO_REMOVE = "5668925324:AAGCofex3jA0Sr4IM8C6cmgzw7WIBClAELQ"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def main():
    """Main method that starts the bot"""
    updater = Updater(TOKEN_TO_REMOVE,
                      request_kwargs={
                          'read_timeout': 20,
                          'connect_timeout': 20
                      },
                      use_context=True)

    add_commands(updater)
    add_handlers(updater.dispatcher)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()