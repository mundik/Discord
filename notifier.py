import threading
import System


def add_notify(name, date_time, text):
    #if date_time < System.now():
    #    return f"Unable to create notification for past event."
    delta = (date_time-System.now())
    sec = delta.seconds
    t = threading.Timer(sec, lambda: notify(name, text))
    t.start()
    return f'Notification for note {name} has been set...\n Remaining time: {System.date_to_human(sec)}'


def notify(name, text):
    print(name, text)
