from typing import List, Dict

from telegram import Update, InlineKeyboardButton, Message, MessageEntity
from telegram.ext import CallbackContext
from telegram_bot_pagination import InlineKeyboardPaginator
from bs4 import BeautifulSoup

from modules.data.config import Config
from modules.data.database import MysqlConnection
from modules.utils.message_paginator import split_messages

import requests
import logging
import time
import base64
import json

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from prometheus_client import Counter

# extension_path = "/home/guberlo/NoSnitchSocio/config/ublock_origin-1.51.0.xpi"
service = Service()
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0")
driver = webdriver.Firefox(service=service, options=options)
wait = WebDriverWait(driver, 5)
# driver.install_addon(extension_path, temporary=True)

config = Config()
logger = logging.getLogger(__name__)
mysql = MysqlConnection(config)
toniparro_counter = Counter('toniparro_counter', 'Counter for toniparro command')

COMMAND = "!toniparro"
BYPASSER_URL = "https://nabilafk.github.io/bypasser/"
reply = "Aspetta un minutino consulto gli archivi del Dr. Antonino Parrone.....🔎"

def get_top_link(update: Update, context: CallbackContext) -> str:
    toniparro_counter.inc()

    logger.debug("TONIPARRO PARTE")

    # Plain simple command
    if update.message.text == COMMAND and not update.message.reply_to_message:
        update.message.reply_text(config.no_link_message)
        return 

    # Case 1: reply to a preexisting message
    if update.message.reply_to_message:
        logger.debug("CASO 1")
        # Get the replied message text
        replied_text = update.message.reply_to_message.caption
        logger.debug("Replied message caption: " + str(update.message.reply_to_message))

        if not replied_text:
            logger.debug("Replied message: " + str(update.message.reply_to_message))
            update.message.reply_text(config.no_link_message)
            return

        # Get name
        name = replied_text.splitlines()[0] or "NoName"
        logger.debug("NAME " + name)

        # Get the first URL inside the message
        link = get_link_in_message(update.message.reply_to_message)
        if not link:
            update.message.reply_text(config.error_message)
            return
        
        logger.debug("LINK " + link)

        try:
            msg = update.message.reply_text(reply)
            if (is_toniparrato_by_link(link)):
                context.bot.edit_message_text(chat_id=update.message.chat_id,
                                            message_id=msg.message_id,
                                            text='\n'.join(get_scraped_by_link(link)))
            else:
                scraped = scrape_link(link)
                context.bot.edit_message_text(chat_id=update.message.chat_id,
                                            message_id=msg.message_id,
                                            text=scraped)
                save_scraped_link({'link': link, 'scraped_link': scraped, 'name': name})
        except Exception as error:
            logger.error(error)
            update.message.reply_text(config.error_message)

    # Case 2: command with arguments
    else:
        logger.debug("CASO 2")
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
                                            text=scraped)
                #save_scraped_link(scraped)
        except Exception as error:
            logger.error(error)
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
    driver.get(BYPASSER_URL)

    # Wait for input box and add link
    input_box = wait.until(EC.presence_of_element_located((By.ID, "input_link")))
    logger.debug("INPUT BOX FOUND!")
    input_box.clear()
    input_box.send_keys(url)

    # Wait for the submit button
    submit_button = wait.until(EC.presence_of_element_located((By.ID, "submit_btn")))
    logger.debug("SUBMIT BUTTON FOUND!")
    submit_button.click()

    # Wait for the result to be visible and that has text
    logger.debug("LOOKING FOR ANSWER")
    result = wait.until(text_not_empty((By.ID, "results")))
    logger.debug("Result: " + result.text)

    return result.text

def get_link_in_message(message: Message) -> str:
    entities = message.caption_entities or []
    link = None

    logger.debug("Scanning message entities")
    try:
        for entity in entities:
            if entity.type == MessageEntity.URL:
                logger.debug("Found URL entity!")
                # URL is present as-is in the text
                link = message.parse_caption_entity(entity)
                break
            elif entity.type == MessageEntity.TEXT_LINK:
                logger.debug("Found TEXT LINK entity!")
                # Embedded link
                link = entity.url
                break
        return link
    except Exception as e:
        logger.error(f"Error scanning entities: ${e}")
        return None


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

## Helper for driver
# Custom ExpectedCondition: wait until element has non-empty text
class text_not_empty:
    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        element = driver.find_element(*self.locator)
        if element.text.strip():
            return element
        return False
