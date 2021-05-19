sepstr = ' @#$ '


def addToFile(statement, ans):
    file = open("userTask.txt", "a+")
    file.write(statement + sepstr + ans + '\n')
    file.close()
