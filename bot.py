import time
import telebot
from telebot import types
import config
import myData

bot = telebot.TeleBot(config.TOKEN)
lastQuery = -1
def flood_protect(message):
    print(message.text)
    global lastQuery
    print(lastQuery, message.date)
    if(message.date - lastQuery < 1):
        bot.send_message(message.chat.id, 'тихо-тихо. Я устал уже..')
        lastQuery = message.date
        return False
    else:
        lastQuery = message.date
        return True




# приветствие
@bot.message_handler(commands=["start"])
def greeting(message):
    if not flood_protect(message):
        return
    markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_start = types.KeyboardButton(r'/start')
    item_solve = types.KeyboardButton(r'/solve')
    item_sendReview = types.KeyboardButton(r'/sendReview')
    markup_reply.add(item_solve, item_start, item_sendReview)
    bot.send_message(message.chat.id, myData.greet, reply_markup=markup_reply)


# отправление отзыва
@bot.message_handler(commands=["sendReview"])
def review(message):
    if not flood_protect(message):
        return
    if config.keepCalm:
        bot.send_message(message.chat.id, "извините, мой создатель отдыхает")
        return
    userReview = bot.send_message(message.chat.id, "напишите отзыв:")
    bot.register_next_step_handler(userReview, sendToAdmin)


def sendToAdmin(message):
    if not flood_protect(message):
        return
    bot.send_message(config.adminId, f'вам пришел отзыв!\n{message.from_user.username}: {message.text}')


# генерация задания
@bot.message_handler(commands=["solve"])
def genTask(message):
    time.sleep(1)
    task, ans = myData.genTask()
    userAns = bot.send_message(message.chat.id, task)
    if not flood_protect(userAns):
        return
    bot.register_next_step_handler(userAns, checkAns, ans, task)



# проверяем ответ
def checkAns(userAns, ans, task):
    if not flood_protect(userAns):
        return
    if userAns.text == r"/start":
        greeting(userAns)
        return
    if userAns.text == str(ans):
        bot.send_message(userAns.chat.id, 'Отлично! у тебя получилось решить этот пример🥺')
    else:
        bot.send_message(userAns.chat.id, f'Нет😡 правильный ответ {ans}')
        if not config.keepCalm:
            bot.send_message(config.adminId, f'{userAns.from_user.username} думал, что {task} {userAns.text}, а не {ans}')
    genTask(userAns)


# # запуск бота
if __name__ == '__main__':
    bot.infinity_polling()
