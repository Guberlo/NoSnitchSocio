from telegram import Update
from telegram.ext import CallbackContext
from bs4 import BeautifulSoup

from modules.data.config import Config

import requests
import re

config = Config()
COMMAND = "!toniparro"
scrape_ops_url = "https://proxy.scrapeops.io/v1/"
params={
      'api_key': config.scrape_ops_key,
      'bypass': 'cloudflare'
}

def get_top_link(update: Update, context: CallbackContext) -> str:
    if update.message.text == COMMAND:
        update.message.reply_text(config.no_link_message)
        return 

    link = update.message.text.split("!toniparro ")[1]
    if not link.startswith("https://") and not link.startswith("http://"):
        update.message.reply_text(config.no_link_message)
        return
    try:
        msg = update.message.reply_text("Aspetta un minuttino consulto gli archivi del Dr. Antonino Parrone.....🔎")
        context.bot.edit_message_text(chat_id=update.message.chat_id,
                                      message_id=msg.message_id,
                                      text=scrape_link(link))

    except Exception as error:
        print(error)
        update.message.reply_text(config.error_message)

def scrape_link(url: str) -> str:
    params['url'] = url
    html = requests.get(scrape_ops_url, params=params)
    soup = BeautifulSoup(html.text, "html.parser")
    page_script = soup.select("body > script:nth-child(4)")[0].text
    return re.search("link: '(.*?)\',", page_script).group(1)