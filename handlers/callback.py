from config.bot import bot
from config.users import users
import config.messages as messages
import markups


@bot.callback_query_handler(func=lambda call: call.data.startswith('buy_category_'))
def category_call(call):
    category_id = int(call.data[13:])
    user = users[call.from_user.id]
    user.selected_category_id = category_id
    bot.edit_message_text(
        chat_id=call.from_user.id,
        text=messages.product_text,
        message_id=call.message.message_id,
        reply_markup=markups.product_markup('buy', category_id)
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith('buy_product_'))
def category_call(call):
    product_id = int(call.data[12:])
    user = users[call.from_user.id]
    user.selected_product_id = product_id
    user.status = 'typing_number'
    bot.edit_message_text(
        chat_id=call.from_user.id,
        text=user.get_product_text(),
        message_id=call.message.message_id,
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith('back_to_buy_category'))
def back_to_choose_category(call):
    user = users[call.from_user.id]
    user.selected_category_id = None
    bot.edit_message_text(
        chat_id=call.from_user.id,
        text=messages.product_text,
        message_id=call.message.message_id,
        reply_markup=markups.category_markup('buy')
    )