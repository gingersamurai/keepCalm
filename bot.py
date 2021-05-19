import time
import telebot
from telebot import types
import config
import markups
import taskClass
import workWithFile

bot = telebot.TeleBot(config.TOKEN)
lastQuery = -1


# приветствие
@bot.message_handler(commands=["start"])
def greeting(message):
    bot.send_message(message.chat.id, """
    привет! поздравляю, ты попал в математическое рабство😺
все просто: я даю примерчики, а ты их решаешь🧑‍🎓
* нажми /menu чтобы попасть в меню
    """, reply_markup=markups.start_rmk)


# главное меню
@bot.message_handler(commands=['menu'])
def mainMenu(message):
    bot.send_message(message.chat.id, """
    * нажмите /solve чтобы начать решать 
* нажмите /sendReview чтобы отправить отзыв моему создателю
* нажмите /addNewTask чтобы добавить новое задание в раздел пользовательских
    """, reply_markup=markups.menu_rmk)

#добавление своего задания
@bot.message_handler(commands=['addNewTask'])
def addTask(message):
    uTaskStatement = bot.send_message(message.chat.id, """
    напишите условие задания:
    """)
    bot.register_next_step_handler(uTaskStatement, addAns)


def addAns(uTaskStatement):
    uTaskAns = bot.send_message(uTaskStatement.chat.id, """
    Отлично! а теперь напишите правильный ответ
    """)
    bot.register_next_step_handler(uTaskAns, addTofile, uTaskStatement)


def addTofile(uTaskAns, uTaskStatement):
    workWithFile.addToFile(uTaskStatement.text, uTaskAns.text)
    mainMenu(uTaskAns)


# отправление отзыва
@bot.message_handler(commands=["sendReview"])
def review(message):
    if config.keepCalm:
        bot.send_message(message.chat.id, "извините, мой создатель отдыхает")
        return
    userReview = bot.send_message(message.chat.id, "напишите отзыв:")
    bot.register_next_step_handler(userReview, sendToAdmin)


def sendToAdmin(message):
    bot.send_message(message.chat.id, "Спасибо за отзыв!")
    bot.send_message(config.adminId, f'вам пришел отзыв!\n{message.from_user.username}: {message.text}')
    mainMenu(message)


# генерация задания
@bot.message_handler(commands=["solve"])
def createTask(message, nowRating=0, prevRating=0):
    if nowRating // 5 > prevRating // 5:
        bot.send_message(message.chat.id, f'поздравляю! Теперь ты на {nowRating // 5} уровне. Задания усложняются.')
    elif nowRating // 5 < prevRating // 5:
        bot.send_message(message.chat.id, f'соберись.. теперь ты на  {nowRating // 5} уровне.')
    task = taskClass.task(nowRating // 5)
    userAns = bot.send_message(message.chat.id, task.statement, reply_markup=myData.solve_rmk)
    bot.register_next_step_handler(userAns, checkAns, task, nowRating)


# проверяем ответ
def checkAns(userAns, task, nowRating):
    if userAns.text == r"/menu":
        bot.send_message(userAns.chat.id, 'Вы увернены, что хотите выйти? ваш рейтинг обнулится..')
        ext = bot.send_message(userAns.chat.id,
                               'чтобы выйти нажмите /menu еще раз, а чтобы остаться нажмите /back',
                               reply_markup=markups.ext_rmk)
        bot.register_next_step_handler(ext, confirmExt, userAns, task, nowRating)
        return
    nextRating = nowRating
    if userAns.text == str(task.ans):
        bot.send_message(userAns.chat.id, 'Отлично! у тебя получилось решить этот пример🥺')
        nextRating += 1
    else:
        bot.send_message(userAns.chat.id, f'Нет😡 правильный ответ {task.ans}')
        if nowRating > 1:
            nextRating -= 1
        if not config.keepCalm:
            bot.send_message(config.adminId,
                             f'{userAns.from_user.username} думал, что {task} {userAns.text}, а не {task.ans}')
    createTask(userAns, nextRating, nowRating)


def confirmExt(ext, userAns, task, nowRating):
    if ext.text == '/menu':
        mainMenu(ext)
    else:
        userAns = bot.send_message(ext.chat.id, task.statement, reply_markup=markups.solve_rmk)
        bot.register_next_step_handler(userAns, checkAns, task, nowRating)


# # запуск бота
if __name__ == '__main__':
    bot.infinity_polling()
