import json
from users.user import User
import config.config as config


user = User(1, config.user_id, config.api_key, email='limio.ananas@gmail.com', password='12345678')
services = user.get_services()['data']

with open('local_base/main.json') as file:
    dictionary = json.load(file)


def get_product_info(name):
    for i in services:
        if i['name'] == name:
            return [i['id'], i['price'], i['max'], i['min']]
    print(name)
    return '0'


new_dict = {}
for category in dictionary.keys():
    new_dict[category] = {}
    for subcategory, name in dictionary[category].items():
        new_dict[category][subcategory] = {name: get_product_info(name)}

with open('local_base/new.json', 'w') as file:
    json.dump(new_dict, file)