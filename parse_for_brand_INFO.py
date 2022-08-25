from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import json


def page_input_search(number, driver):
    input_search = driver.find_element(By.ID, 'search-autocomplete')
    input_search.clear()
    input_search.send_keys(number)
    input_search.send_keys(Keys.ENTER)
    time.sleep(15)

    result = driver.find_element(By.TAG_NAME, 'search-product-list')

    return result


def cutting_numbers(number):
    number = number[1:]

    return number


def good_number(driver, search, first_number):
    product_links = []
    products_box = search.find_elements(By.CLASS_NAME, 'product-box')

    for product_box in products_box:
        link_product = product_box.find_element(By.TAG_NAME, 'a').get_attribute('href')
        product_links.append(link_product)
    print(f'{len(product_links)} link(s)')
    data = []
    for product_link in enumerate(product_links):
        print(f'{product_link[0] + 1} link')
        driver.get(url=product_link[1])
        time.sleep(4)

        product_brand = driver.find_element(By.CLASS_NAME, 'main-info-brand').text

        product_number = driver.find_element(By.CLASS_NAME, 'main-info-code').text

        if product_brand == 'FEBI BILSTEIN':
            product_brand = 'FE'
            sku_site = product_brand + product_number
        elif product_brand == 'AJUSA':
            product_brand = 'AJU'
            sku_site = product_brand + product_number
        else:
            sku_site = product_brand + product_number

        data_list = {}

        if sku_site == first_number:
            data_list[f'{first_number}'] = {'Number': product_number,
                         'Brand': product_brand}
            data.append(data_list)
            break
    with open('Parse_Weight.json', 'a') as file:
        json.dump(data, file, ensure_ascii=True, indent=4)
    return data


def restart(sku, driver, first_number):
    sku = cutting_numbers(number=sku)
    parse_autodoc(number=sku, driver=driver, first_number=first_number)


def parse_autodoc(number, driver, first_number):
    global empty_search

    search = page_input_search(number=number, driver=driver)
    try:
        empty_search = search.find_element(By.CLASS_NAME, 'product-list')
        empty_search = search.find_element(By.TAG_NAME, 'p').text
    except Exception as ex_:
        print(first_number)
        print(ex_)
    if empty_search == 'Нічого не знайдено?':
        restart(sku=number, driver=driver, first_number=first_number)
    else:
        data_r = good_number(driver=driver, search=search, first_number=first_number)
        # return data_r


def main_parse(numbers, driver):
    number = numbers.strip()
    data = parse_autodoc(number=number, driver=driver, first_number=number)
    # return data


if __name__ == '__main__':
    main_parse()
