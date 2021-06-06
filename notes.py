import Database
import Notifier
from datetime import datetime


def add_note(name, input_time, text, *interval):
    note = Database.command(f'''SELECT * FROM notes WHERE name='{name}' ''')
    if len(note) != 0:
        return f'Note {name} already exists.'
    else:
        time = datetime.strptime(input_time, '%d.%m.%Y %H:%M')
        try:
            Database.add_repeat_note(name, time, text, interval[0], repeat='TRUE')
        except IndexError:
            Database.add_note(name, time, text, repeat='FALSE')
        ret = Notifier.add_notify(name, time, text)
        return f'Note {name} added\n{ret}'


print(add_note('A', '6.6.2021 14:50', 'test'))
