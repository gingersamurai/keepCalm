sepstr = ' @#$ '


def addToFile(statement, ans):
    file = open("userTask.txt", "a+", encoding="utf-8")
    file.write(statement + sepstr + ans + '\n')
    file.close()
