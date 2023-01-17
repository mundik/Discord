import System
import Database


def check():
    today = System.today()
    data = Database.command(f'''SELECT * FROM Workout ''')
    date = System.datework()
    delta = (today-date).days
    for i in data:
        if i[0] == 'push':
            Database.command(f'''UPDATE Workout SET value = {i[1] + delta * 20} WHERE name = 'push' ''')
        elif i[0] == 'run':
            Database.command(f'''UPDATE Workout SET value = {i[1] + delta * 250} WHERE name = 'run' ''')
    System.datewrite("workout", delta)


def substract(option, num):
    check()
    data = Database.command(f'''SELECT * FROM Workout ''')
    for i in data:
        if i[0] == option:
            diff = i[1] - int(num)
            Database.command(f'''UPDATE Workout SET value = {diff} WHERE name = '{option}' ''')
            return diff
    return ""


def status():
    check()
    ret = ""
    data = Database.command(f'''SELECT * FROM Workout ''')
    for i in data:
        ret += f'{i[0]}: {i[1]}\n'
    return ret
