import System
import Database


def check():
    today = System.today()
    begin = System.workout_begin
    data = Database.command(f'''SELECT * FROM Workout ''')[0]
    date = System.date_work()
    delta = (today - date).days
    if delta > 0:
        number = data[1]
        for i in range(delta):
            number += (date - begin).days + 12 + i
        Database.command(f"UPDATE Workout SET value = {str(number)} WHERE name like 'push'")
        # elif i[0] == 'run':
        # Database.command(f'''UPDATE Workout SET value = {i[1] + delta * 250} WHERE name = 'run' ''')
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
