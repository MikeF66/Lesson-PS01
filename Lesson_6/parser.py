from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import csv


class DivanNavigator:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 15)  # Увеличенное время ожидания

    def parse_page(self, url):
        self.driver.get(url)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Прокрутка страницы вниз
        time.sleep(10)
        lamps = []
        items = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, '_Ud0k.U4KZV')))

        for item in items:
            try:
                title = item.find_element(By.CSS_SELECTOR, 'span[itemprop="name"]').text
                price = item.find_element(By.CSS_SELECTOR, 'meta[itemprop="price"]').get_attribute('content')
                link = item.find_element(By.CSS_SELECTOR, 'a.ui-GPFV8.qUioe.ProductName.ActiveProduct').get_attribute(
                    'href')
                lamps.append([title, price, link])
            except Exception as e:
                print(f'Ошибка при парсинге элемента: {e}')
        return lamps

    def parse_all_pages(self, base_url, total_pages):
        all_lamps = []
        for page in range(1, total_pages + 1):
            url = f'{base_url}/page-{page}'
            print(f'Парсинг страницы: {url}')
            lamps = self.parse_page(url)
            all_lamps.extend(lamps)

        return all_lamps

def main():
    base_url = 'https://www.divan.ru/category/svet'
    total_pages = 7

    navigator = DivanNavigator()
    all_lamps = navigator.parse_all_pages(base_url, total_pages)

    # for lamp in all_lamps:
    #     print(lamp)
    # print(f'Всего элементов - {len(all_lamps)}')

    navigator.driver.quit()

    with open('divan2.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Название', 'Цена', 'Ссылка'])
        writer.writerows(all_lamps)


if __name__ == "__main__":
    main()
