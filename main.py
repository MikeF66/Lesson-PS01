import requests
from bs4 import BeautifulSoup
from googletrans import Translator
def get_english_word():
    url = "https://randomword.com/"
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        english_word = soup.find("div", id="random_word").text.strip()
        word_definition = soup.find("div", id="random_word_definition").text.strip()
        return {
            "english_word": english_word,
            "word_definition": word_definition
        }
    except:
        print(f"Произошла ошибка. Статус-код: {response.status_code}")
def word_game():
    print('Добро пожаловать в игру "Угадай слово"')
    translator = Translator()
    while True:
        word_dict = get_english_word()
        word = word_dict.get("english_word")
        word_definition = word_dict.get("word_definition")
        result1 = translator.translate(word, dest="ru")
        result2 = translator.translate(word_definition, dest="ru")
        ru_word = result1.text
        print(ru_word) # вывожу слово, иначе, с учетом перевода, никогда не отгадаешь )))
        ru_word_definition = result2.text
        print(f"Слово имеет следующее значение: {ru_word_definition}")
        user = input("Введите слово:")
        if user == ru_word:
            print("Правильно!")
        else:
            print(f"Неверно. Правильный ответ {ru_word}")
        play_again = input("Вы хотите сыграть еще раз? д/н")
        if play_again != "д":
            print("Спасибо за игру! До свидания!")
            break

word_game()
