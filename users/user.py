import database
import config.config as config
import requests
import hashlib
import time


class User:
    def __init__(self,
                 tg_id,
                 smo_id=1,
                 api_key='fad',
                 is_registered=True,
                 email=None,
                 login=None,
                 password=None):
        self.id = tg_id
        self.is_registered = is_registered
        self.email = email
        self.login = login
        self.password = password
        self.smo_id = smo_id
        self.api_key = api_key
        self.status = 'afk'
        self.selected_category_id = None
        self.selected_product_id = None
        self.number = None
        self.phone = None
        self.url = None
        self.available_min = None
        self.available_max = None

    def authentication_user(self):
        data = {
            'action': 'auth',
            'api_id': config.user_id_secret,
            'login': self.login,
            'nonce': int(time.time()),
            'password': self.password,
        }
        sign = ';'.join(map(str, data.values()))
        sign += ';' + config.api_key_secret
        hash_item = hashlib.md5(sign.encode('utf-8'))
        hash_string = hash_item.hexdigest().upper()
        data['sign'] = hash_string
        r = requests.post(config.api_url, data=data)
        return r.json()

    def registration_user(self):
        data = {
            'action': 'register',
            'api_id': config.user_id_secret,
            'email': self.email,
            'login': self.login,
            'nonce': int(time.time()),
            'password': self.password,
        }
        sign = ';'.join(map(str, data.values()))
        sign += ';' + config.api_key_secret
        hash_item = hashlib.md5(sign.encode('utf-8'))
        hash_string = hash_item.hexdigest().upper()
        data['sign'] = hash_string
        r = requests.post(config.api_url, data=data)
        return r.json()

    def set_user_api(self, json):
        if json['type'] == 'success':
            self.smo_id = json['data']['USER_ID']
            self.api_key = json['data']['API_KEY']
            return True
        else:
            self.reset_registration()
            return False

    def get_balance(self):
        data = {
            'user_id': self.smo_id,
            'api_key': self.api_key,
            'action': 'balance'
        }
        r = requests.post(config.api_url, data=data)
        return r.json()['data']['balance']

    def get_categories(self):
        data = {
            'user_id': self.smo_id,
            'api_key': self.api_key,
            'action': 'services'
        }
        r = requests.post(config.api_url, data=data)
        return r.json()

    def create_order(self):
        data = {
            'user_id': self.smo_id,
            'api_key': self.api_key,
            'action': 'create_order',
            'service_id': self.selected_product_id,
            'count': self.number,
            'url': self.url
        }
        r = requests.post(config.api_url, data=data)
        return r.json()

    def get_order(self, order_id):
        data = {
            'user_id': self.smo_id,
            'api_key': self.api_key,
            'action': 'check_order',
            'order_id': order_id
        }
        r = requests.post(config.api_url, data=data)
        return r.json()

    def get_my_orders(self, orders):
        # Сообщение, вылезающее при нажатии на кнопку "мои заказы".
        # На 127 строчке начало, 132 строчка добавляет в текст один каждый заказ
        text = """Ваши заказы:\n"""
        for order_id, order_info in orders.items():
            order = self.get_order(order_id)
            order_name = order_info['name']
            total = order_info['total']
            text += f"""{order_name} - {total} RUB. Статус - {order['data']['status']}\n"""
        return text

    def get_services(self):
        data = {
            'user_id': self.smo_id,
            'api_key': self.api_key,
            'action': 'services',
        }
        r = requests.post(config.api_url, data=data)
        return r.json()

    def reset_registration(self):
        self.status = 'choosing_registered'
        self.email = None
        self.password = None
        self.login = None
        self.smo_id = None
        self.api_key = None

    def reset_selected(self):
        self.status = 'afk'
        self.selected_category_id = None
        self.selected_product_id = None
        self.number = None
        self.phone = None
        self.url = None

    def add_user(self, json):
        if not self.set_user_api(json):
            return False
        try:
            database.add_user(self)
            return True
        except TypeError:
            self.reset_registration()
            return False

    def get_product_text(self):
        # То самое сообщение, которое вы так хотели отредачить)
        product_info = database.get_product_info(self.selected_product_id)
        category_name = product_info[0]
        product_name = product_info[1]
        price = product_info[2]
        min_number = product_info[3]
        max_number = product_info[4]
        self.available_max = max_number
        self.available_min = min_number
        return f"""Вы делаете заказ на услугу \"{product_name}\" из категории {category_name}
Цена - {price} RUB.
Минимальное количество для заказа - {min_number}
Максимальное количество для заказа - {max_number}
Введите желаемое количество"""

    def get_account_info(self):
        # Сообщение, вылезающее при регистрации
        return f"""Поздравляем с регистрацией. 
Ваш новый логин - {self.login}
Ваш новый пароль - `{self.password}`"""

    def get_auth_info(self):
        # Сообщение, вылезающее при авторизации
        return f"""Поздравляем с авторизацией.
Ваш логин - {self.login}
Ваш пароль - `{self.password}`"""

