import Database
from datetime import datetime
import System


def add_note(name, input_date, input_time, text):
    timestamp = datetime.strptime(f'{input_date} {input_time}', '%d.%m.%Y %H:%M')
    now = System.now()
    if timestamp < now:
        return f"Unable to create notification for past event."
    else:
        delta = timestamp - now
        sec = (delta.days * 86400) + delta.seconds
    note = Database.command(f'''SELECT * FROM notes WHERE name='{name}' ''')
    if len(note) != 0:
        return f'Note {name} already exists.'
    else:
        input_date = datetime.strptime(input_date, '%d.%m.%Y').strftime('%Y-%m-%d')
        Database.add_note(name, input_date, input_time, text, repeat='FALSE')
        return f'Note {name} added\nNotification for note {name} has been set...\nRemaining time: ' \
               f'{System.date_to_human(sec)}', sec


def delete_note(name):
    Database.command(f'''DELETE FROM notes where name='{name}' ''')
    return f"Note {name} successfully deleted"


def clear_due():
    notes = Database.command('''SELECT * FROM notes''')
    for i in notes:
        if (datetime.strptime(i[1], '%H:%M:%S') < System.now() and
           datetime.strptime(i[2], '%Y-%m-%d') == System.today()) or \
           (datetime.strptime(i[2], '%Y-%m-%d') < System.today()):
            Database.command(f'''DELETE FROM notes where name='{i[0]}' ''')
