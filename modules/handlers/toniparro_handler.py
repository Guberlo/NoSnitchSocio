from telegram import Update
from telegram.ext import CallbackContext

from modules.data.config import Config
	
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By

import re

config = Config()
COMMAND = "!toniparro"

options = Options()
# options.add_argument('--headless')
# options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

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
    driver.get(url)
    page_script = driver.find_element(By.XPATH, "/html/body/script[1]").get_attribute("textContent")
    print(page_script)
    return re.search("link: '(.*?)\',", page_script).group(1)



