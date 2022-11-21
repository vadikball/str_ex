import logging
import os
import traceback
from typing import Optional

from bs4 import BeautifulSoup
from pydantic import BaseModel
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

url = 'https://www.vsemayki.ru/catalog/group/man_tshirts?page='

logger = logging.getLogger(__name__)


class ItemSchema(BaseModel):
    name: str
    price: int
    photo: str


def scrap_vse_mayki(driver: webdriver.Chrome):
    shirts_info = []
    for i in range(1, 4):
        driver.get(url + str(i))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        t_shirts = soup.find_all(class_='_2o6OVoxH')

        for shirt in t_shirts:
            photo = shirt.find(class_='_90Cp5Gp7').attrs['src']
            price = shirt.find(class_='price')
            price = int(price.text[:-2]) // 100
            name = shirt.find(class_='_38-vDi9W').text
            shirts_info.append(ItemSchema(
                photo=photo, price=price, name=name
            ))

    return shirts_info


def get_data() -> Optional[list[ItemSchema]]:
    logger.info('start scrapping')
    options = Options()
    options.headless = True
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    chrome_prefs = dict()
    options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    driver = webdriver.Chrome(options=options, executable_path=os.environ.get('DRIVER_PATH', '/usr/bin/chromedriver'))
    data = scrap_vse_mayki(driver)
    if data:
        print('success')
    driver.quit()
    return data
