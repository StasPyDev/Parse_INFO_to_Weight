import threading

from selenium import webdriver
import json

from spareto import spareto
from parse_for_brand_INFO import main_parse


def process(url, number, pool, options):

    with pool:
        # data = []
        print(f'Process is start - {number}')
        result = selenium(url=url, file=number, options=options)
        # data.append(result)
        # with open('Parse_Weight.json', 'w') as file:
        #     json.dump(data, file, ensure_ascii=True, indent=4)


def selenium(url, file, options):
    driver = webdriver.Chrome(executable_path='C:\\Users\\Stas2\\PycharmProjects\\Parse_for_Weight\\chromedriver\\chromedriver.exe',
                              options=options)

    driver.get(url=url)
    # data = []

    try:
        # data = []
        data_number_info = main_parse(numbers=file, driver=driver)
        # return data_number_info
        # data.append(data_number_info)

    except Exception as ex:
        print(ex)
    finally:
        # with open('Parse_Weight.json', 'a') as file:
        #     json.dump(data, file, ensure_ascii=True, indent=4)
        driver.close()
        driver.quit()


def main():
    options = webdriver.ChromeOptions()
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--headless')

    url2 = 'https://spareto.com/'
    url = 'https://www.buycarparts.co.uk/'
    url3 = 'https://autodoc.ua/'
    with open('Collect weight-37к.csv', 'r') as file:
        src = file.readlines()

    max_connections = int(input('How process to start: '))

    pool = threading.BoundedSemaphore(value=max_connections)
    for i in enumerate(src):
        thr = threading.Thread(target=process, args=(url3, i[1].strip(), pool, options), name=f'thr-{i[0]}')
        thr.start()

    # get_count_numbers(url=url3, numbers=src, options=options)
    # selenium(url=url3, file=src, options=options)


if __name__ == '__main__':
    main()
