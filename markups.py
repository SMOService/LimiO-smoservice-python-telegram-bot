from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
import database


main_markup = ReplyKeyboardMarkup()
main_markup.row('Создать новый заказ')
main_markup.row('Мои заказы', 'Пополнить баланс')
main_markup.row('Заработать', 'Поддержка', 'FAQ')


markup_yes_no = ReplyKeyboardMarkup(True, True)
markup_yes_no.row('Да', 'Нет')


markup_balance = InlineKeyboardMarkup()
button_balance = InlineKeyboardButton(
    text='Пополнить баланс',
    url='https://smoservice.media/personal/balance/'
)
markup_balance.row(button_balance)


markup_faq = InlineKeyboardMarkup()
button_faq = InlineKeyboardButton(
    text='Заработать!',
    url='https://smoservice.media/pages/partner_program/'
)
markup_faq.row(button_faq)


markup_support = InlineKeyboardMarkup()
button_support = InlineKeyboardButton(
    text='Поддержка!',
    url='t.me/smoservice_bot'
)
markup_support.row(button_support)


def category_markup(act):
    markup = InlineKeyboardMarkup()
    categories = database.get_categories()
    for category in categories:
        button = InlineKeyboardButton(
            text=category[1],
            callback_data=f'{act}_category_{category[0]}'
        )
        markup.row(button)
    return markup


def product_markup(act, category_id):
    markup = InlineKeyboardMarkup()
    products = database.get_products(category_id)
    for product in products:
        text = f"""{product[1]}"""
        button = InlineKeyboardButton(
            text=text,
            callback_data=f'{act}_product_{product[0]}'
        )
        markup.row(button)
    button_menu = InlineKeyboardButton(text='Назад', callback_data=f'back_to_{act}_category')
    markup.row(button_menu)
    return markup


def confirm_markup(thing, act, category_id, product_id=None):
    markup = InlineKeyboardMarkup()
    button_confirm = InlineKeyboardButton(
        text='Уверен',
        callback_data=f'yes_{act}_{thing}_{category_id}' if not product_id else f'yes_{act}_{thing}_{product_id}')
    button_back = InlineKeyboardButton(
        text='Нет',
        callback_data=f'back_{act}_{thing}' if not product_id else f'back_{act}_{thing}_{category_id}')
    markup.row(button_confirm, button_back)
    return markup


