import logging

from telegram.ext import Updater

from modules.handlers import add_commands, add_handlers
from modules.data.config import Config
from modules.data.database import MysqlConnection

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def main(config: Config):
    """Main method that starts the bot"""
    updater = Updater(config.bot_token,
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
    config = Config()
    print(config.bot_token)
    main(config)