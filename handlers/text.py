from config.bot import bot
import config.messages as messages
from config.users import users, orders
from users.user import User
import markups
import functions
import database


@bot.message_handler(commands=['start'])
def start_message(message):
    tg_id = message.from_user.id
    markup = markups.markup_yes_no
    if tg_id not in users or not users[tg_id].is_registered:
        users[tg_id] = User(tg_id, is_registered=False)
        users[tg_id].status = 'choosing_registered'
        text = messages.choose_is_registered_text
    elif not users[tg_id].email:
        text = messages.send_email_text
        users[tg_id].status = 'typing_email'
    elif not users[tg_id].login:
        text = messages.send_login_text
        users[tg_id].status = 'typing_login'
    elif not users[tg_id].password:
        text = messages.send_password_text
        users[tg_id].status = 'typing_password'
    else:
        text = messages.start_message,
        markup = markups.main_markup
    bot.send_message(
        message.from_user.id,
        text,
        reply_markup=markup
    )


@bot.message_handler(
    func=lambda message: message.from_user.id in users and users[message.from_user.id].status == 'choosing_registered')
def choosing_registered_text(message):
    answers = ['Да', 'Нет']
    m_text = message.text
    if m_text in answers:
        user = users[message.from_user.id]
        user.status = 'typing_email' if m_text == 'Да' else 'typing_new_email'
        user.is_registered = True if m_text == 'Да' else False
        text = messages.send_email_text if m_text == 'Да' else messages.send_new_mail_text
        bot.send_message(
            user.id,
            text
        )


@bot.message_handler(
    func=lambda message: message.from_user.id in users and users[message.from_user.id].status == 'typing_new_email')
def new_mail_text_text(message):
    random_password = functions.password_generate()
    user = users[message.from_user.id]
    user.email = message.text
    user.login = message.text
    user.password = random_password
    reg_json = user.registration_user()
    if reg_json['type'] == 'success':
        text = user.get_account_info()
        user.status = 'afk'
        markup = markups.main_markup
        orders[user.id] = {}
        functions.save_pickle(orders)
        user.add_user(reg_json)
    else:
        markup = markups.markup_yes_no
        text = messages.bad_new_email + '\n' + reg_json['data']['message'] + '\n' + messages.choose_is_registered_text
        user.reset_registration()
    bot.send_message(
        user.id,
        text=text,
        reply_markup=markup,
        parse_mode='markdown'
    )


@bot.message_handler(
    func=lambda message: message.from_user.id in users and users[message.from_user.id].status == 'typing_email')
def mail_text(message):
    user = users[message.from_user.id]
    user.status = 'typing_password'
    user.email = message.text
    user.login = message.text
    text = messages.send_password_text
    bot.send_message(
        user.id,
        text
    )


@bot.message_handler(
    func=lambda message: message.from_user.id in users and users[message.from_user.id].status == 'typing_password')
def api_key_text(message):
    user = users[message.from_user.id]
    user.password = message.text
    json = user.authentication_user()
    if user.add_user(json):
        markup = markups.main_markup
        text = user.get_auth_info()
        orders[user.id] = {}
        functions.save_pickle(orders)
        user.status = 'afk'
    else:
        markup = markups.markup_yes_no
        text = messages.bad_registration_text
        user.reset_registration()
    bot.send_message(
        user.id,
        text,
        reply_markup=markup
    )


@bot.message_handler(func=lambda message:  message.from_user.id in users and message.text == 'Создать новый заказ')
def create_new_order_text(message):
    user = users[message.from_user.id]
    user.reset_selected()
    bot.send_message(
        user.id,
        messages.category_text,
        reply_markup=markups.category_markup('buy')
    )


@bot.message_handler(func=lambda message:  message.from_user.id in users and message.text == 'Заработать')
def faq_text(message):
    bot.send_message(
        message.from_user.id,
        messages.take_money_text,
        reply_markup=markups.markup_faq
    )


@bot.message_handler(func=lambda message:  message.from_user.id in users and message.text == 'Пополнить баланс')
def add_balance_text(message):
    user = users[message.from_user.id]
    bot.send_message(
        message.from_user.id,
        f'Ваш баланс: {user.get_balance()}'+'\n'+messages.add_balance_text,
        reply_markup=markups.markup_balance
    )


@bot.message_handler(func=lambda message:  message.from_user.id in users and message.text == 'Мои заказы')
def my_orders(message):
    user = users[message.from_user.id]
    bot.send_message(
        user.id,
        user.get_my_orders(orders[message.from_user.id])
    )


@bot.message_handler(func=lambda message:  message.from_user.id in users and message.text == 'Поддержка')
def support_text(message):
    bot.send_message(
        message.from_user.id,
        messages.support_text,
        reply_markup=markups.markup_support
    )


@bot.message_handler(func=lambda message:  message.from_user.id in users and message.text == 'FAQ')
def faq_text(message):
    bot.send_message(
        message.from_user.id,
        messages.FAQ_text,
    )


@bot.message_handler(
    func=lambda message: message.from_user.id in users and users[message.from_user.id].status == 'typing_number')
def number_text(message):
    user = users[message.from_user.id]
    if functions.is_int(message.text) and user.available_max >= int(message.text) >= user.available_min:
        user.number = int(message.text)
        user.status = 'typing_url'
        bot.send_message(
            user.id,
            messages.url_text
        )
    else:
        bot.send_message(
            user.id,
            messages.bad_number_text
        )


@bot.message_handler(
    func=lambda message: message.from_user.id in users and users[message.from_user.id].status == 'typing_url')
def number_text(message):
    user = users[message.from_user.id]
    user.url = message.text
    user.status = 'afk'
    json = user.create_order()
    if json['type'] == 'success':
        order_info = database.get_product_info(user.selected_product_id)
        total = json['data']['price']
        orders[user.id][json['data']['order_id']] = {'total': total, 'name': order_info[1]}
        functions.save_pickle(orders)
        text = messages.end_form_text
    else:
        text = messages.bad_order_start_text + json['desc'] + messages.bad_order_end_text
    bot.send_message(
        user.id,
        text,
        disable_web_page_preview=True
    )
    user.reset_selected()


