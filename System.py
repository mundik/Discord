from datetime import *
import Database


def now():
    return datetime.now()


def today():
    return date.today()


def date_anime():
    anime_date = (Database.command(f'''SELECT date from System_time WHERE type='anime' ''')[0][0])
    return anime_date


def date_work():
    workout_date = (Database.command(f'''SELECT date from System_time WHERE type='workout' ''')[0][0])
    return workout_date


def strp(input_date):
    return datetime.strptime(input_date, '%Y-%m-%d').date()


def datewrite(typ, add):
    sql = f'''SELECT date from System_time WHERE type='{typ}' '''
    get_date = (Database.command(sql)[0][0])
    add = timedelta(days=add)
    get_date += add
    Database.command(f"UPDATE System_time SET date='{get_date}' WHERE type='{typ}'")


def time_to_human(input_time):
    seconds = int(input_time)
    periods = [
        ('month', 60 * 60 * 24 * 30),
        ('day', 60 * 60 * 24),
        ('hour', 60 * 60),
        ('minute', 60),
        ('second', 1)]
    strings = []
    for period_name, period_seconds in periods:
        if seconds > period_seconds:
            period_value, seconds = divmod(seconds, period_seconds)
            has_s = 's' if period_value > 1 else ''
            strings.append(f"{period_value} {period_name}{has_s}")
    return ", ".join(strings)


def days_to_human(string):
    string = string.replace("_", " ")
    string = string.replace("Mon", "Monday")
    string = string.replace("Tue", "Tuesday")
    string = string.replace("Wed", "Wednesday")
    string = string.replace("Thu", "Thursday")
    string = string.replace("Fri", "Friday")
    string = string.replace("Sat", "Saturday")
    string = string.replace("Sun", "Sunday")
    return string
