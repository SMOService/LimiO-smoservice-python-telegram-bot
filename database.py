import sqlite3
from config.config import database_name
import config.config as config
import json


def create_base():
    with sqlite3.connect(database_name) as connection:
        cursor = connection.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                            tg_id INTEGER NOT NULL,
                            email TEXT NOT NULL,
                            login TEXT NOT NULL,
                            password TEXT NOT NULL,
                            smo_id INTEGER NOT NULL,
                            api_key TEXT NOT NULL
                            )""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS categories (
            category_id INTEGER PRIMARY KEY,
            category_name TEXT NOT NULL
        );""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER NOT NULL,
            category_name TEXT NOT NULL,
            product_name TEXT NOT NULL,
            price INTEGER NOT NULL,
            max INTEGER NOT NULL,
            min INTEGER NOT NULL
        );""")
        connection.commit()


def get_users():
    with sqlite3.connect(database_name) as connection:
        cursor = connection.cursor()
        cursor.execute("""SELECT tg_id FROM users""")
        users = [user[0] for user in cursor.fetchall()]
        return users


def add_user(user):
    with sqlite3.connect(database_name) as connection:
        cursor = connection.cursor()
        info = (user.id, user.email, user.login, user.password, user.smo_id, user.api_key)
        cursor.execute("""INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)""", info)
        connection.commit()


def set_category(category):
    with sqlite3.connect(config.database_name) as connection:
        cursor = connection.cursor()
        cursor.execute(f"""INSERT INTO categories(category_name) VALUES (?)""", (category,))
        connection.commit()


def get_categories():
    with sqlite3.connect(config.database_name) as connection:
        cursor = connection.cursor()
        cursor.execute("""SELECT category_id, category_name FROM categories""")
        try:
            return cursor.fetchall()
        except Exception as e:
            print(e)
            return None


def set_product(category_name, product_name, info):
    with sqlite3.connect(config.database_name) as connection:
        cursor = connection.cursor()
        new_list = [info[0], category_name, product_name] + info[1:]
        cursor.execute(f"""INSERT INTO products VALUES (?, ?, ?, ?, ?, ?)""", tuple(new_list))
        connection.commit()


def get_category_name_by_id(category_id):
    with sqlite3.connect(config.database_name) as connection:
        cursor = connection.cursor()
        cursor.execute(f"""SELECT category_name FROM categories WHERE category_id = {category_id}""")
        return cursor.fetchone()[0]


def get_product_name_by_id(product_id):
    with sqlite3.connect(config.database_name) as connection:
        cursor = connection.cursor()
        cursor.execute(f"""SELECT product_name FROM products WHERE product_id = {product_id}""")
        return cursor.fetchone()[0]


def get_products(category_id):
    with sqlite3.connect(config.database_name) as connection:
        cursor = connection.cursor()
        category_name = get_category_name_by_id(category_id)
        cursor.execute(f"""SELECT product_id, product_name, price FROM products WHERE category_name = '{category_name}'""")
        try:
            return cursor.fetchall()
        except Exception as e:
            print(e)
            return []


def get_product_info(product_id):
    with sqlite3.connect(config.database_name) as connection:
        cursor = connection.cursor()
        cursor.execute(f"""SELECT category_name, product_name, price, min, max FROM products 
                        WHERE product_id = {product_id}""")
        try:
            return cursor.fetchone()
        except Exception as e:
            print(e)
            return []


if __name__ == '__main__':
    create_base()
    new_dict = json.load(open('local_base/new.json'))
    for category, subcategories in new_dict.items():
        set_category(category + ' раскрутка')
        for subcategory, subcategory_dict in subcategories.items():
            for name, info_list in subcategory_dict.items():
                set_product(category + ' раскрутка', name, info_list)

