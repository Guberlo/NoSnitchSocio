from typing import List, Dict

from telegram import Update, InlineKeyboardButton
from telegram.ext import CallbackContext
from telegram_bot_pagination import InlineKeyboardPaginator
from bs4 import BeautifulSoup

from modules.data.config import Config
from modules.data.database import MysqlConnection
from modules.utils.message_paginator import split_messages

import requests
import re

config = Config()
mysql = MysqlConnection(config)

COMMAND = "!toniparro"
scrape_ops_url = "https://proxy.scrapeops.io/v1/"
params={
      'api_key': config.scrape_ops_key,
      'bypass': 'cloudflare'
}
reply = "Aspetta un minutino consulto gli archivi del Dr. Antonino Parrone.....🔎"

def get_top_link(update: Update, context: CallbackContext) -> str:
    if update.message.text == COMMAND:
        update.message.reply_text(config.no_link_message)
        return 

    prompt = update.message.text.split("!toniparro ")[1]
    if not prompt.startswith("https://") and not prompt.startswith("http://"):
        if prompt == "lista" or prompt == "list":
            show_names(update, context)
            return
        if not is_toniparrato_by_name(prompt):
            update.message.reply_text(config.not_found_message)
        else: 
            update.message.reply_text('\n'.join(get_links_by_name(prompt)))

        return
    
    try:
        msg = update.message.reply_text(reply)
        if (is_toniparrato_by_link(prompt)):
            context.bot.edit_message_text(chat_id=update.message.chat_id,
                                        message_id=msg.message_id,
                                        text='\n'.join(get_scraped_by_link(prompt)))
        else:
            scraped = scrape_link(prompt)
            context.bot.edit_message_text(chat_id=update.message.chat_id,
                                        message_id=msg.message_id,
                                        text=scraped['scraped_link'])
            save_scraped_link(scraped)
    except Exception as error:
        print(error)
        update.message.reply_text(config.error_message)

def show_names(update: Update, context: CallbackContext):
    splitted_names = split_messages(get_all_names())

    paginator = InlineKeyboardPaginator(
        len(splitted_names),
        data_pattern='name#{page}'
    )

    paginator.add_after(InlineKeyboardButton('Chiudi', callback_data='closeKeyboard'))

    update.message.reply_text(
        text=splitted_names[0],
        reply_markup=paginator.markup,
    )

def handle_names_pagination_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    page = int(query.data.split('#')[1])
    splitted_actions = split_messages(get_all_names())

    paginator = InlineKeyboardPaginator(
        len(splitted_actions),
        current_page=page,
        data_pattern='name#{page}'
    )

    paginator.add_after(InlineKeyboardButton('Chiudi', callback_data='closeKeyboard'))

    query.edit_message_text(
        text=splitted_actions[page - 1],
        reply_markup=paginator.markup
    )

def scrape_link(url: str) -> Dict[str, str]:
    params['url'] = url
    html = requests.get(scrape_ops_url, params=params)
    soup = BeautifulSoup(html.text, "html.parser")
    page_script = soup.select("body > script:nth-child(4)")[0].text

    return {
        'name': re.search("title: '(.*?)\',", page_script).group(1),
        'link': url,
        'scraped_link': re.search("link: '(.*?)\',", page_script).group(1)
    }

def save_scraped_link(scraped: Dict[str, str]) -> bool:
    query = f"""INSERT INTO toniparrate (name, link, scraped_link)
        VALUES ('{scraped['name'].lower()}', '{scraped['link']}', '{scraped['scraped_link']}')
    """

    return mysql.insert_or_update(query=query)

def get_links_by_name(name: str) -> List[str]:
    query = f"SELECT scraped_link FROM toniparrate WHERE name='{name}'"
    result = mysql.select(query)
    links = [link for l in result for link in l]

    return links

def get_scraped_by_link(link: str) -> List[str]:
    query = f"SELECT scraped_link FROM toniparrate WHERE link='{link}'"
    result = mysql.select(query)
    links = [link for l in result for link in l]

    return links

def is_toniparrato_by_link(link: str) -> bool:
    query = f"SELECT COUNT(*) FROM toniparrate WHERE link='{link}'"
    result = mysql.select(query)
    print("COUNT: ", result)
    return result[0][0] != 0

def is_toniparrato_by_name(name: str) -> bool:
    query = f"SELECT COUNT(*) FROM toniparrate WHERE name='{name.lower()}'"
    result = mysql.select(query)
    return result[0][0] != 0

def get_all_names() -> List[str]:
    query = "SELECT DISTINCT name FROM toniparrate;"
    result = mysql.select(query)
    names = [name for n in result for name in n]

    return names
