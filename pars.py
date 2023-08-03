import bs4
import requests
import selenium
from selenium.webdriver import Firefox
from users.user import User
import config.config as config
from time import sleep
import json


def get_html(url):
    r = requests.get(url)
    return r.text


def get_second_name(new_html):
    new_soup = bs4.BeautifulSoup(new_html, 'lxml')
    item = new_soup.find('div', class_='service__item')
    new_name = item.find('h6', class_='service__title').text.strip()
    return new_name


user = User(1, config.user_id, config.api_key, email='limio.ananas@gmail.com', password='12345678')
categories = ['Инстаграм',
              'ВКонтакте',
              'Ютуб',
              'Телеграм',
              'Одноклассники',
              'Фейсбук',
              'Твиттер',
              'Мой мир',
              'АСКфм',
              'Твич',
              'Музыка',
              'Приложения',
              'ТикТок']
dictionary = {key: {} for key in categories}
services = user.get_services()


main_url = 'https://smoservice.media/'
html = get_html(main_url)
soup = bs4.BeautifulSoup(html, 'lxml')
main_div = soup.find('div', id='uaccordion').find('div', class_='row')
rows = main_div.find_all('div', class_='col-sm-4')
for row in rows:
    cards = row.find_all('div', class_='ucard mb-3')
    for card in cards:
        name = card.find('h6').text.strip()[:-10].strip()
        subcategories = card.find('div', class_='pt-4').find('ul').find_all('li', class_='nav-item')
        for li in subcategories:
            try:
                subcategory_name = li.text.strip()
                url = li.find('a').get('href')
                new_page = get_html(main_url+url)
                second_name = get_second_name(new_page)
                dictionary[name][subcategory_name] = [second_name]
            except Exception as e:
                print(url)


with open('local_base/main.json', 'w') as file:
    json.dump(dictionary, file)

