import telebot
from telebot import types
import config
import myData

bot = telebot.TeleBot(config.TOKEN)


# приветствие
@bot.message_handler(commands=["start"])
def greeting(message):
    markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_start = types.KeyboardButton(r'/start')
    item_solve = types.KeyboardButton(r'/solve')
    item_sendReview = types.KeyboardButton(r'/sendReview')
    markup_reply.add(item_solve, item_start, item_sendReview)
    bot.send_message(message.chat.id, myData.greet, reply_markup=markup_reply)


@bot.message_handler(commands=["sendReview"])
def review(message):
    userReview = bot.send_message(message.chat.id, "напишите отзыв:")
    bot.register_next_step_handler(userReview, sendToAdmin)


def sendToAdmin(message):
    bot.send_message(config.adminId, f'вам пришел отзыв!\n{message.from_user.username}: {message.text}')


# ответ на сообщения
@bot.message_handler(commands=["solve"])
def genTask(message):
    task, ans = myData.genTask()
    userAns = bot.send_message(message.chat.id, task)
    bot.register_next_step_handler(userAns, checkAns, ans, task)


# проверяем ответ
def checkAns(userAns, ans, task):
    if userAns.text == r"/start":
        greeting(userAns)
        return
    if userAns.text == str(ans):
        bot.send_message(userAns.chat.id, 'Отлично! у тебя получилось решить этот пример🥺')
    else:
        bot.send_message(userAns.chat.id, f'Нет😡 правильный ответ {ans}')
        bot.send_message(config.adminId, f'{userAns.from_user.username} думал, что {task} {userAns.text}, а не {ans}')
    genTask(userAns)


# # запуск бота
if __name__ == '__main__':
    bot.infinity_polling()
