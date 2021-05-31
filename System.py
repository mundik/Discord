import datetime
import Database


def now():
    return datetime.datetime.now()


def today():
    return strp(str(datetime.date.today()))


def dateanime():
    anime_date = (Database.command(f'''SELECT date from System_date WHERE type='anime' ''')[0][0])
    return anime_date


def datework():
    workout_date = (Database.command(f'''SELECT date from System_date WHERE type='workout' ''')[0][0])
    return workout_date


def strp(date):
    return datetime.datetime.strptime(date, '%Y-%m-%d').date()


def datewrite(typ, add):
    sql = f'''SELECT date from System_date WHERE type='{typ}' '''
    date = (Database.command(sql)[0][0])
    add = datetime.timedelta(days=add)
    date += add
    Database.command(f'''UPDATE System_date SET date='{date}' WHERE type='{typ}' ''')
