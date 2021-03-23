"""
В нашей школе мы не можем разглашать персональные данные пользователей,
но чтобы преподаватель и ученик смогли объяснить нашей поддержке,
кого они имеют в виду (у преподавателей, например, часто учится несколько Саш),
мы генерируем пользователям уникальные и легко произносимые имена.
Имя у нас состоит из прилагательного, имени животного и двузначной цифры.
В итоге получается, например, "Перламутровый лосось 77".
Для генерации таких имен мы и решали следующую задачу:
Получить с русской википедии список всех животных (Категория:Животные по алфавиту)
и вывести количество животных на каждую букву алфавита. Результат должен получиться
в следующем виде:
А: 642
Б: 412
В:....

"""

import requests
from bs4 import BeautifulSoup
import time

url = 'https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту'
headers = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 '
                         'Safari/537.36'}


desired_object = []  # Создаем пустой список для добавленния объектов.
alphabetical = []  # Создаем пустой список для заполнения значением страницы.
lead_time = []

start = time.time()


def composing_elements():
    # Разбиваем список по категория и подсчитываем количество элементов в определеной категории.

    global desired_object, alphabetical
    asc = alphabetical[2:]
    # Мы добавляем пустую строку в списки, чтобы вычислить последнюю точку.
    desired_object.append(' ')
    asc.append(' ')
    ind = 1  # Индекс по списку.
    point = 0  # Начальная точка.
    summing_up_the_esults = []  # Список для записи полученых значений.
    for i in desired_object:
        if i[0] == asc[ind]:
            index_element = desired_object.index(i)  # Уточняем индекс элемента
            interval = index_element - point  # Вычисляем количества элементов по определеному значению.
            point = index_element
            summing_up_the_esults.append(f'{asc[ind - 1]} : {interval}')
            ind += 1

    print('//////////////////////////////////////////////////////////////////////////////////////////////////////////')
    return summing_up_the_esults  # Возвращаем полученный результат.


def get_html(url_website, params=None):
    try:
        # Подключаемся к сайту.
        r = requests.get(url=url_website, params=params, headers=headers)
        return r
    except requests.exceptions.ConnectionError as error:
        print('Ошибка ', error)


def get_pages(html):
    global alphabetical
    try:
        # В функции ищем категории.
        soup = BeautifulSoup(html, 'lxml')

        pagination = soup.find_all('a', {'class': 'external text'})
        for i in pagination:
            if i.text != 'A':
                alphabetical.append(i.text)
            else:
                break
    except AttributeError as error:
        print('Ошибка', error)


def get_content(html):
    global desired_object
    # Функция собирает нужную информацию с сайта.
    soup = BeautifulSoup(html, 'lxml')
    divs = soup.find('div', {'class': 'mw-category'})
    # Через цикл собираем информация и добавляем с список.
    for div in divs:
        info = div.find_all('li')
        for i in info:
            title = i.find('a')
            desired_object.append(title.text)  # Добавяем полученое значение в список.


def parsing():
    global desired_object
    try:
        html = get_html(url)
        get_pages(html.text)
        if html.status_code == 200:
            print('Подключение к сайту прошло успешно.')

            print('Идет сбор информации странниц ')
            rr = 0
            html = get_html(url, params={"from": 'А'})
            get_content(html.text)
            while True:
                if desired_object[-1][0] == 'A':
                    break
                else:
                    html = get_html(url, params={'pagefrom': desired_object[-1]})
                    get_content(html.text)
                    rr += 1
            stop = time.time()
            print('Сбор данных завершен!!')
            print(f'На выполнение по сбору информации потребовалось {stop - start} секунд.')
            result = composing_elements()
            for i in result:
                print(i)

        else:
            print('Ошибка ')
    except AttributeError as error:
        print('Ошибка', error)


if __name__ == '__main__':
    parsing()
