import System
import Database


def daily_check():
    today = System.today()
    data = Database.command(f'''SELECT * FROM workout ''')
    date = System.datework()
    delta = (today-date).days
    for i in data:
        if i[0] == 'push':
            Database.command(f'''UPDATE workout SET value = {i[1] + delta * 20} WHERE name = 'push' ''')
        elif i[0] == 'run':
            Database.command(f'''UPDATE workout SET value = {i[1] + delta * 250} WHERE name = 'run' ''')
    System.datewrite("workout", delta)


def substract(option, num):
    data = Database.command(f'''SELECT * FROM workout ''')
    ret = ""
    for i in data:
        if i[0] == option:
            Database.command(f'''UPDATE workout SET value = {i[1] - int(num)} WHERE name = '{option}' ''')
            ret = i[1] - num
            break
    return ret


def status():
    ret = ""
    data = Database.command(f'''SELECT * FROM workout ''')
    for i in data:
        ret += f'{i[0]}: {i[1]}\n'
    return ret
