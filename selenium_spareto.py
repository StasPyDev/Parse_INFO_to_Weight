from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import json


def search_for_number(driver, brand, number):
    cards = driver.find_elements(By.CLASS_NAME, 'card-col')
    for card in cards:
        url_card = card.find_element(By.CLASS_NAME, 'card-product-details').find_element(By.TAG_NAME, 'a').get_attribute('href')
        card_brand = card.find_element(By.CLASS_NAME, 'brand').text
        card_number = card.find_element(By.CLASS_NAME, 'part_number').text

        if card_brand == brand and card_number == number:
            driver.get(url=url_card)

            info_cards = driver.find_elements(By.CLASS_NAME, 'card')
            if len(info_cards) >= 2:
                for info_card in info_cards:
                    trs = info_card.find_elements(By.TAG_NAME, 'tr')
                    return_elements = find_weight(info=trs)
                    if return_elements:
                        return return_elements
                    else:
                        continue
            else:
                return find_weight(info=info_cards)

        else:
            continue


def find_weight(info):
    for tr_card in info:
        tds = tr_card.find_elements(By.TAG_NAME, 'td')
        for td in tds:
            if td.text.lower() == 'weight':
                return tds[-1].text.split(' ')[0]
