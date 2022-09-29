import threading

from selenium import webdriver
import csv

from selenium_spareto import search_for_number


def process(url, number, pool, options):
    with open('Parse_Spareto_KLOKERHOLM.csv', 'a', newline='') as file:
        csvwriter = csv.writer(file, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)

        with pool:
            selenium(url=url, files=number, options=options, csv_writer=csvwriter)


def selenium(url, files, options, csv_writer):
    driver = webdriver.Chrome(executable_path='C:\\Users\\Stas2\\PycharmProjects\\Parse_for_Weight\\chromedriver\\chromedriver.exe',
                              options=options)

    brand = files.split(';')[1].strip()
    number = files.split(';')[0]
    url = url + number

    driver.get(url=url)

    try:
        weight = search_for_number(driver=driver, brand=brand, number=number)
        csv_writer.writerow([number, weight])
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()


def main():
    options = webdriver.ChromeOptions()
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--headless')

    url_spareto = 'https://spareto.com/products?utf8=%E2%9C%93&keywords='
    url2 = 'https://spareto.com/'
    url = 'https://www.buycarparts.co.uk/'
    url3 = 'https://autodoc.ua/'
    with open('Collect weight-37к.csv', 'r') as file:
        src = file.readlines()
    select_operations = int(input("1. Threading\n2. One process\n"))

    if select_operations == 1:
        max_connections = int(input('How process to start: '))

        pool = threading.BoundedSemaphore(value=max_connections)
        for i in enumerate(src):
            thr = threading.Thread(target=process, args=(url_spareto, i[1].strip(), pool, options), name=f'thr-{i[0]}')
            thr.start()
    else:
        with open('Parse_Spareto_3.csv', 'a', newline='') as file:
            csvwriter = csv.writer(file, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)

            for number in enumerate(src):
                print(f'Number {number[0]} is {len(src)} go')
                selenium(url=url_spareto, files=number[1], options=options, csv_writer=csvwriter)


if __name__ == '__main__':
    main()
