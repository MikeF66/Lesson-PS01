from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class DivanNavigator:
    def __init__(self):
        options = Options()
        options.add_argument("--headless")  # Открыть браузер в фоновом режиме
        options.add_argument("start-maximized")
        options.add_argument("disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 20)  # Увеличенное время ожидания

    def parse_page(self, url):
        self.driver.get(url)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Прокрутка страницы вниз
        time.sleep(10)  # Увеличенное время ожидания для загрузки элементов
        lamps = []
        items = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, '_Ud0k.U4KZV')))
        for item in items:
            try:
                link_element = item.find_element(By.CSS_SELECTOR, 'a.ui-GPFV8.qUioe.ProductName.ActiveProduct')
                name = link_element.find_element(By.CSS_SELECTOR, 'span[itemprop="name"]').text
                price = item.find_element(By.CSS_SELECTOR, 'meta[itemprop="price"]').get_attribute('content')
                link = link_element.get_attribute('href')
                lamps.append([name, price, link])
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
    for lamp in all_lamps:
        print(lamp)
    navigator.driver.quit()

if __name__ == "__main__":
    main()
