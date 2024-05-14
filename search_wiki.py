from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from random import choice


class WikipediaNavigator:
    def __init__(self):
        self.browser = webdriver.Chrome()

    def open_wikipedia(self, search_query):
        self.browser.get("https://ru.wikipedia.org/wiki/%D0%97%D0%B0%D0%B3%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0")
        search_box = self.browser.find_element(By.ID, "searchInput")
        search_box.clear()
        search_box.send_keys(search_query)
        search_box.send_keys(Keys.RETURN)
        a = self.browser.find_element(By.LINK_TEXT, search_query)
        a.click()
        time.sleep(2)

    def list_paragraphs(self):
        paragraphs = self.browser.find_elements(By.CSS_SELECTOR, "p")
        for index, paragraph in enumerate(paragraphs):
            input(f"Параграф {index + 1}:\n{paragraph.text}\nНажмите Enter для следующего параграфа...\n")

    def choose_related_article(self):
        hatnotes = []
        for element in self.browser.find_elements(By.CLASS_NAME, "hatnote"):
            if "navigation-not-searchable" in element.get_attribute("class"):
                hatnotes.append(element)
        if hatnotes:  # проверяем, что есть найденные элементы
            hatnote = choice(hatnotes)
            link_element = hatnote.find_element(By.TAG_NAME, "a")
            link = link_element.get_attribute("href")
            if link.startswith("https://ru.wikipedia.org/wiki/"): # проверяем, что ссылка ведет на статью Википедии
                self.browser.get(link)
                time.sleep(2)
                print(self.browser.title)
            else:
                print("Найденная ссылка не является статьей Википедии.")
        else:
            print("Не найдено связанных статей.")

    def close(self):
        self.browser.quit()

def main():
    navigator = WikipediaNavigator()

    try:
        initial_query = input("Введите поисковый запрос: ")
        navigator.open_wikipedia(initial_query)

        while True:
            action = input("Выберите действие:\n1) Листать параграфы,\n2) Перейти на связанную страницу,\n3) Выйти\nВаш выбор: ")
            if action == "1":
                navigator.list_paragraphs()
            elif action == "2":
                navigator.choose_related_article()
            elif action == "3":
                break
            else:
                print("Неверный ввод, попробуйте снова.")

    finally:
        navigator.close()


if __name__ == "__main__":
    main()
