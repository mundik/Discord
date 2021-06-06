from datetime import *
import Database


def now():
    return datetime.now()


def today():
    return strp(str(date.today()))


def dateanime():
    anime_date = (Database.command(f'''SELECT date from System_date WHERE type='anime' ''')[0][0])
    return anime_date


def datework():
    workout_date = (Database.command(f'''SELECT date from System_date WHERE type='workout' ''')[0][0])
    return workout_date


def strp(input_date):
    return datetime.strptime(input_date, '%Y-%m-%d').date()


def datewrite(typ, add):
    sql = f'''SELECT date from System_date WHERE type='{typ}' '''
    get_date = (Database.command(sql)[0][0])
    add = timedelta(days=add)
    get_date += add
    Database.command(f'''UPDATE System_date SET date='{get_date}' WHERE type='{typ}' ''')


def date_to_human(input_time):
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
