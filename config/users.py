import sqlite3
import pickle
from users import user


connection = sqlite3.connect('database.db')
cursor = connection.cursor()
cursor.execute("""SELECT * FROM users""")
users_list = cursor.fetchall()
users = {}
try:
    orders = pickle.load(open('local_base/orders.pkl', 'rb'))
except EOFError:
    orders = {}
    pickle.dump(orders, open('local_base/orders.pkl', 'wb'), 2)
for bot_user in users_list:
    tg_id = bot_user[0]
    email = bot_user[1]
    login = bot_user[2]
    password = bot_user[3]
    smo_id = bot_user[4]
    api_key = bot_user[5]
    users[tg_id] = user.User(tg_id, smo_id=smo_id, api_key=api_key, email=email, login=login, password=password)

