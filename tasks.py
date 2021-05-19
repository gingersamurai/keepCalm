import random


class task:
    def __init__(self, level):
        self.level = level
        self.statement, self.ans = self.genTask()

    def genTask(self):
        typ = random.randint(1, 4)
        a = random.randint(1, 10 ** self.level)
        b = random.randint(1, 10 ** self.level)
        statement = str()
        ans = str()
        if typ == 1:
            statement = f'{a} * {b} ='
            ans = a * b
        elif typ == 2:
            a = a * 10 + random.randint(0, 9)
            a -= a % b
            statement = f'{a} / {b} ='
            ans = a // b
        elif typ == 3:
            a = a * 10 + random.randint(0, 9)
            b = b * 10 + random.randint(0, 9)
            statement = f'{a} + {b} ='
            ans = a + b
        else:
            a = a * 10 + random.randint(0, 9)
            b = b * 10 + random.randint(0, 9)
            statement = f'{a} - {b} ='
            ans = a - b
        return statement, ans

    def dbg(self):
        print(f"""
        level = {self.level}
        statement = {self.statement}
        ans = {self.ans}

        """)


