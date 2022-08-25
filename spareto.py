import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


def spareto(driver, file):
    for sku in file:
        search_block = driver.find_element(By.ID, 'keywords')
        search_block.clear()
        search_block.send_keys(sku)
        search_block.send_keys(Keys.ENTER)
        time.sleep(5)

        brand = driver.find_element(By.CLASS_NAME, 'brand').text
        time.sleep(5)


if __name__ == '__main__':
    spareto()
