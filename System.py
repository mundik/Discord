import datetime
import Git_update as Git
file = "Sysinfo.txt"


def now():
    return datetime.datetime.now()


def today():
    return strp(str(datetime.date.today()))
    # return datetime.datetime.now().strftime("%a")


def dateanime():
    anime_date = dateread()[1]
    anime_date = (anime_date.strip().split(" "))[1]
    return strp(anime_date)


def datework():
    workout_date = dateread()[0]
    workout_date = (workout_date.strip().split(" "))[1]
    return strp(workout_date)


def dateread():
    with open(file, "r+") as _file:
        workout_date = _file.readline()
        anime_date = _file.readline()
    return workout_date, anime_date


def strp(date):
    return datetime.datetime.strptime(date, '%Y-%m-%d').date()


def datewrite(typ, date):
    if typ == "w":
        date1 = dateanime()
        with open(file, "w") as _file:
            _file.write(str("Workout: " + str(date) + "\n"))
            _file.write(str("Anime: " + str(date1) + "\n"))
    elif typ == "a":
        date1 = datework()
        with open(file, "w+") as _file:
            _file.write(str("Workout: " + str(date1) + "\n"))
            _file.write(str("Anime: " + str(date) + "\n"))
    Git.new_commit(file)
