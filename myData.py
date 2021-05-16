import random


def genTask():
    mx = 100

    a = random.randint(1, 100)
    b = random.randint(1, 100)
    task = f"{a} + {b} = "
    ans = a + b
    return [task, ans]


greet = r"""
привет! поздравляю, ты попал в математическое рабство.
все просто: я даю примерчики, а ты их решаешь.
* нажми /solve  чтобы начать
* нажми /start чтобы вернуться в меню
* нажим /sendReview чтобы отправить отзыв моему создателю
"""
