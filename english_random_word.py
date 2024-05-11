import requests
from bs4 import BeautifulSoup
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
    while True:
        word_dict = get_english_word()
        word = word_dict.get("english_word")
        word_definition = word_dict.get("word_definition")
        print(f"Слово имеет следующее значение: {word_definition}")
        user = input("Введите слово:")
        if user == word:
            print("Правильно!")
        else:
            print(f"Неверно. Правильный ответ {word}")
        play_again = input("Вы хотите сыграть еще раз? y/n")
        if play_again != "y":
            print("Спасибо за игру! До свидания!")
            break

word_game()
