import Database
from datetime import datetime
import System


def add_note(name, input_time, text):
    time = datetime.strptime(input_time, '%d.%m.%Y_%H:%M')
    if time < System.now():
        return f"Unable to create notification for past event."
    else:
        delta = time - System.now()
        sec = delta.seconds
    note = Database.command(f'''SELECT * FROM notes WHERE name='{name}' ''')
    if len(note) != 0:
        return f'Note {name} already exists.'
    else:
        Database.add_note(name, time, text, repeat='FALSE')
        return f'Note {name} added\nNotification for note {name} has been set...\nRemaining time: ' \
               f'{System.date_to_human(sec)}', sec


def delete_note(name):
    Database.command(f'''DELETE FROM notes where name='{name}' ''')
    return f"Note {name} successfully deleted"


def reload_note(ret):
    notes = Database.command('''SELECT * FROM notes''')
    for i in notes:
        note_date = datetime.strptime(i[1], '%Y-%m-%d %H:%M:%S')
        now = System.now()
        if note_date < now:
            Database.command(f'''DELETE FROM notes where name='{i[0]}' ''')
        elif note_date > now:
            ret.append(i)
