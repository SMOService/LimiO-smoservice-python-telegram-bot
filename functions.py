import pickle
from random import choice


def is_int(text):
    try:
        int(text)
        return True
    except ValueError:
        return False


def add_func(number, comment, list_of_letter):
    for i in range(number):
        comment += choice(list_of_letter)
    return comment


def password_generate():
    alphabet = "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z"
    list_of_letter = [letter.lower() for letter in alphabet.split()]
    list_of_letter += [str(i) for i in range(10)]
    comment = ''
    comment = add_func(10, comment, list_of_letter)
    return comment


def save_pickle(orders):
    with open('local_base/orders.pkl', 'wb') as file:
        pickle.dump(orders, file, 2)
        file.close()


if __name__ == '__main__':
    print(is_int('fad'))
