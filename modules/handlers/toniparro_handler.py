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
import time
import base64
import json

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By

from prometheus_client import Counter

# extension_path = "/home/guberlo/NoSnitchSocio/config/ublock_origin-1.51.0.xpi"
# service = Service()
# options = Options()
# # options.add_argument('--headless')
# # options.add_argument('--no-sandbox')
# options.add_argument('--disable-dev-shm-usage')
# options.add_argument("user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0")
# driver = webdriver.Firefox(service=service, options=options)
# driver.install_addon(extension_path, temporary=True)

config = Config()
mysql = MysqlConnection(config)
toniparro_counter = Counter('toniparro_counter', 'Counter for toniparro command')

COMMAND = "!toniparro"
scrape_ops_url = "https://proxy.scrapeops.io/v1/"
params={
      'api_key': config.scrape_ops_key,
      'bypass': 'cloudflare'
}
reply = "Aspetta un minutino consulto gli archivi del Dr. Antonino Parrone.....🔎"

def get_top_link(update: Update, context: CallbackContext) -> str:
    toniparro_counter.inc()
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

def scrape_linkvertise(url: str) -> str: 
    first_link = 'https://publisher.linkvertise.com/api/v1/redirect/link/static/'
    second_link = 'https://publisher.linkvertise.com/api/v1/redirect/link/insert/linkvertise/path/here/target?serial=base64encodedjson'
    second_link_front = second_link[0:second_link.find('insert/linkvertise')]
    second_link_back = second_link[second_link.find('/target?serial'):second_link.find('base64encodedjson')]

    new_link = "None"

    try:
        input_link = url
        link = ''
        if '.com/' in input_link:
            if '?o=' in input_link:
                link = input_link[input_link.find('.com/')+5:input_link.find('?o=')]
            else:
                link = input_link[input_link.find('.com/')+5:len(input_link)]
        if '.net/' in input_link:
            if '?o=' in input_link:
                link = input_link[input_link.find('.net/')+5:input_link.find('?o=')]
            else:
                link = input_link[input_link.find('.net/')+5:len(input_link)]
            

        r = requests.get(first_link + link,timeout=2)
        text = r.text
        link_id = text[text.find('"id":')+5:text.find(',"url":')]

        new_json = {"timestamp":int(time.time()), "random":"6548307", "link_id":int(link_id)}

        s = json.dumps(new_json)
        json_converted = base64.b64encode(s.encode('utf-8'))
        json_converted = str(json_converted)
        json_converted = json_converted[2:len(json_converted)-1]

        r = requests.get(second_link_front + link + second_link_back + json_converted,timeout=4)
        converted_json = json.loads(r.text)
        new_link = converted_json['data']['target']

    except:
        filler_value = "filler_value"
    
    return new_link

def scrape_link(url: str) -> Dict[str, str]:
    if ("link-hub" in url):
        scraped_link = scrape_linkvertise(url)
        name = "Unknown"
    else:
        params['url'] = url
        html = requests.get(scrape_ops_url, params=params)
        soup = BeautifulSoup(html.text, "html.parser")
        page_script = soup.select("body > script:nth-child(4)")[0].text
        name =  re.search("title: '(.*?)\',", page_script).group(1)

    return {
        'name': name,
        'link': url,
        'scraped_link': scraped_link
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
