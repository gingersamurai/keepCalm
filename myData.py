import random
from telebot import types


def genTask(level):
    level = min(level, 8)
    level = max(level, 1)
    typ = random.randint(1, 4)
    a = random.randint(1, 10 ** level)
    b = random.randint(1, 10 ** level)
    task = str()
    ans = int()
    if typ == 1:
        task = f'{a} * {b} ='
        ans = a * b
    elif typ == 2:
        a = a * 10 + random.randint(0, 9)
        a -= a % b
        task = f'{a} / {b} ='
        ans = a // b
    elif typ == 3:
        a = a * 10 + random.randint(0, 9)
        b = b * 10 + random.randint(0, 9)
        task = f'{a} + {b} ='
        ans = a + b
    else:
        a = a * 10 + random.randint(0, 9)
        b = b * 10 + random.randint(0, 9)
        task = f'{a} - {b} ='
        ans = a - b
    return task, ans


start_rmk = types.ReplyKeyboardMarkup(resize_keyboard=True)
start_rmk.add(types.KeyboardButton('/menu'))

menu_rmk = types.ReplyKeyboardMarkup(resize_keyboard=True)
menu_rmk.add(types.KeyboardButton('/solve'), types.KeyboardButton('/sendReview'))

solve_rmk = types.ReplyKeyboardMarkup(resize_keyboard=True)
solve_rmk.add(types.KeyboardButton('/menu'))

rUsure_rmk = types.ReplyKeyboardMarkup(resize_keyboard=True)
rUsure_rmk.add(types.KeyboardButton('да'), types.KeyboardButton('нет'))
