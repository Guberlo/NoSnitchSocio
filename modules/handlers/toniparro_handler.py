from telegram import Update
from telegram.ext import CallbackContext
from bs4 import BeautifulSoup

from modules.data.config import Config

import requests
import re

config = Config()
COMMAND = "!toniparro"

def get_top_link(update: Update, context: CallbackContext) -> str:
    if update.message.text == COMMAND:
        update.message.reply_text(config.no_link_message)
        return 
    
    link = update.message.text.split("!toniparro ")[1]
    if not link.startswith("https://") and not link.startswith("http://"):
        update.message.reply_text(config.no_link_message)
        return
    try:
        update.message.reply_text(scrape_link(link))
    except Exception as error:
        print(error)
        update.message.reply_text(config.no_link_message)
    
def scrape_link(url: str) -> str:
    html = requests.get(url)
    soup = BeautifulSoup(html.text, "html.parser")
    page_script = soup.select("body > script:nth-child(4)")[0].text
    return re.search("link: '(.*?)\',", page_script).group(1)



