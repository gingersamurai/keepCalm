import random
from telebot import types


# hello from testing
start_rmk = types.ReplyKeyboardMarkup(resize_keyboard=True)
start_rmk.add(types.KeyboardButton('/menu'))

menu_rmk = types.ReplyKeyboardMarkup(resize_keyboard=True)
menu_rmk.add(types.KeyboardButton('/solve'), types.KeyboardButton('/sendReview'), types.KeyboardButton('/addNewTask'))

solve_rmk = types.ReplyKeyboardMarkup(resize_keyboard=True)
solve_rmk.add(types.KeyboardButton('/menu'))

ext_rmk = types.ReplyKeyboardMarkup(resize_keyboard=True)
ext_rmk.add(types.KeyboardButton('/menu'), types.KeyboardButton('/back'))

rUsure_rmk = types.ReplyKeyboardMarkup(resize_keyboard=True)
rUsure_rmk.add(types.KeyboardButton('да'), types.KeyboardButton('нет'))

