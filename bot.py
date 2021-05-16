import time
import telebot
from telebot import types
import config
import myData

bot = telebot.TeleBot(config.TOKEN)
lastQuery = -1


def flood_protect(message):
    global lastQuery
    if (message.date - lastQuery < 1):
        bot.send_message(message.chat.id, 'тихо-тихо. Я устал уже< подожди пару секунд')
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
    bot.send_message(message.chat.id, """
    привет! поздравляю, ты попал в математическое рабство😺
все просто: я даю примерчики, а ты их решаешь🧑‍🎓
* нажми /menu чтобы попасть в меню
    """, reply_markup=myData.start_rmk)


# главное меню
@bot.message_handler(commands=['menu'])
def mainMenu(message):
    bot.send_message(message.chat.id, """
    * нажмите /solve чтобы начать решать 
* нажмите /sendReview чтобы отправить отзыв моему создателю
    """, reply_markup=myData.menu_rmk)


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
    bot.send_message(message.chat.id, "Спасибо за отзыв!")
    bot.send_message(config.adminId, f'вам пришел отзыв!\n{message.from_user.username}: {message.text}')
    mainMenu(message)


# генерация задания
@bot.message_handler(commands=["solve"])
def genTask(message, level=1, cur=0):
    time.sleep(1)
    if cur == 5:
        level += 1
        cur = 0
        bot.send_message(message.chat.id, f'Поднимаем ставки! удачи на {level} уровне:)')
    elif cur < 0:
        level -= 1
        cur = 4
        bot.send_message(message.chat.id, f'увы, теперь ты на {level} уровне:(')
    bot.send_message(message.chat.id, f' тебя {level} уровень и {5 * (level - 1) + cur} рейтинга')
    task, ans = myData.genTask(level)
    userAns = bot.send_message(message.chat.id, task, reply_markup=myData.solve_rmk)
    if not flood_protect(userAns):
        return
    bot.register_next_step_handler(userAns, checkAns, ans, task, level, cur)


# проверяем ответ
def checkAns(userAns, ans, task, level, cur):
    if not flood_protect(userAns):
        return
    if userAns.text == r"/menu":
        bot.send_message(userAns.chat.id, 'Вы увернены, что хотите выйти? вам придется увеличивать рейтинг с нуля..')
        ext = bot.send_message(userAns.chat.id,
                               'чтобы выйти нажмите /menu еще раз, а чтобы остаться нажмите на любую другую кнопку')
        bot.register_next_step_handler(ext, rUsure, userAns, ans, task, level, cur)
        return
    if userAns.text == str(ans):
        bot.send_message(userAns.chat.id, 'Отлично! у тебя получилось решить этот пример🥺')
        cur += 1
    else:
        bot.send_message(userAns.chat.id, f'Нет😡 правильный ответ {ans}')
        if level > 1:
            cur -= 1
        if not config.keepCalm:
            bot.send_message(config.adminId,
                             f'{userAns.from_user.username} думал, что {task} {userAns.text}, а не {ans}')
    genTask(userAns, level, cur)


def rUsure(ext, userAns, ans, task, level, cur):
    userAns.date = ext.date
    if ext.text == '/menu':
        mainMenu(ext)
    else:
        userAns = bot.send_message(ext.chat.id, task, reply_markup=myData.solve_rmk)
        bot.register_next_step_handler(userAns, checkAns, ans, task, level, cur)

# # запуск бота
if __name__ == '__main__':
    bot.infinity_polling()
