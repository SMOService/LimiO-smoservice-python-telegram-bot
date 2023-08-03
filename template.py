import os


os.mkdir('config')
os.mkdir('handlers')
os.mkdir('users')


def create_file(filename):
    with open(filename, 'w') as file:
        file.close()


create_file('database.py')
create_file('database.db')
create_file('markups.py')
create_file('functions.py')
create_file('config/config.py')
create_file('handlers/text.py')
create_file('handlers/callback.py')
create_file('users/user.py')
create_file('users/admin.py')


main_file_text = """from config.bot import bot
from handlers import text, callback


bot.polling()
"""
bot_file_text = """from telebot import TeleBot
TOKEN = ''
bot = TeleBot(TOKEN)
"""
config_file_text = """creator = 36082701
admins = [creator]"""
markups_file = """from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup"""
handlers_file = """from config.bot import bot
import database"""
user_file = """import database

class User:
    def __init__(self, user_cortege):
        self.id = user_cortege[0]"""

with open('main.py', 'w') as file:
    file.write(main_file_text)
    file.close()


with open('config/bot.py', 'w') as file:
    file.write(bot_file_text)
    file.close()


with open('config/config.py', 'w') as file:
    file.write(config_file_text)
    file.close()


with open('markups.py', 'w') as file:
    file.write(markups_file)
    file.close()


with open('users/user.py', 'w') as file:
    file.write(user_file)
    file.close()


with open('handlers/text.py', 'w') as file:
    file.write(handlers_file)
    file.close()


with open('handlers/callback.py', 'w') as file:
    file.write(handlers_file)
    file.close()