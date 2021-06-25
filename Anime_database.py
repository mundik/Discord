from datetime import *
import System
import Database


def watched(name, add):
    ep, typ = Database.get_anime(name)
    if len(ep) == 0:
        return f"Anime {name} not found."
    else:
        if isinstance(add, int):
            return f"{add} is not a number."
        ep = ep[0][0] + int(add)
        if typ == "ongoing":
            sql = f'''UPDATE anime_ongoing SET current_ep = {ep} WHERE name LIKE '{name}' '''
        elif typ == "finished":
            sql = f'''UPDATE anime_finished SET current_ep = {ep} WHERE name LIKE '{name}' '''
        else:
            return "Database Error."
        Database.command(sql)
        return f"Anime {name} updated."


def new_anime_going(name, ep, last, day, update_date, update_time):
    find = Database.command(f'''SELECT * FROM anime_list as Anime where Anime.name LIKE '{name}' ''')
    if len(find) != 0:
        return "Anime already on list."
    else:
        Database.add_ongoing_anime(name, ep, last, day, update_date, update_time)
        return f"Anime {name} succesfully added."


def new_anime(name, ep, max_ep):
    find = Database.command(f'''SELECT * FROM anime_list as Anime where Anime.name LIKE '{name}' ''')
    if len(find) != 0:
        return "Anime already on list."
    else:
        Database.add_finished_anime(name, ep, max_ep)
        return f"Anime {name} succesfully added."


def delete_anime(name):
    typ = Database.command(f'''SELECT type FROM anime_list as Anime where Anime.name LIKE '{name}' ''')[0][0]
    if len(typ) == 0:
        return "Anime not found."
    if typ == "ongoing":
        sql = f'''DELETE FROM anime_ongoing as Anime where Anime.name LIKE '{name}' '''
    elif typ == "finished":
        sql = f'''DELETE FROM anime_finished as Anime where Anime.name LIKE '{name}' '''
    else:
        return "Database Error"
    Database.command(sql)
    Database.command(f'''DELETE FROM anime_list as Anime where Anime.name LIKE '{name}' ''')
    return f"Anime {name} was removed from watchlist."


def status():
    ret = ""
    data_list = Database.command(f'''SELECT * FROM anime_finished''')
    for i in data_list:
        ret += f"Name: {i[0]}, Episode: {i[1]} out of {i[2]} \n"
    data_list = Database.command(f'''SELECT * FROM anime_ongoing ORDER BY update_date, update_time''')
    for i in data_list:
        ret += f"Name: {i[0]}, Episode: {i[1]}, Last episode: {i[2]}, Airing in {i[3]} at {i[5]}:00\n"
    return System.days_to_human(ret)


def waiting():
    data_list = Database.command(
        f'''SELECT name, current_ep, latest_ep  FROM anime_ongoing WHERE latest_ep > current_ep''')
    ret = ""
    for i in data_list:
        diff = i[2] - i[1]
        append = "s" if diff > 1 else ""
        ret += f"Anime {i[0]} have {diff} unwatched episode{append}.\n"
    return System.days_to_human(ret)


def change_time(name, hour):
    Database.command(f'''UPDATE anime_ongoing SET update_time = {hour} WHERE name LIKE '{name}' ''')
    return f"Anime {name} update time set to {hour}:00"


def update():
    last_time = System.dateanime()
    today = System.today()
    delta = today - last_time
    ret = ""
    for j in range(0, delta.days + 1):
        day = (last_time + timedelta(days=j)).strftime("%a")
        data_list = Database.command(f'''SELECT * FROM anime_ongoing WHERE day LIKE '{day}' ''')
        for i in data_list:
            i = list(i)
            i[4] = datetime.strptime(i[4], "%Y-%m-%d").date()
            if i[4] == today:
                diff = i[5] - System.now().hour
                if System.now().minute > 30:
                    diff -= 1
                if diff == 0:
                    ret += f"Anime {i[0]} will have new episode within hour.\n"
                    continue
                elif diff > 0:
                    append = "s" if diff > 1 else ""
                    ret += f"Anime {i[0]} will have new episode in {diff} hour{append}.\n"
                    continue
            if i[4] <= today:
                diff = i[2]
                while i[4] <= today:
                    i[2] += 1
                    i[4] += timedelta(days=7)
                diff = i[2] - diff
                append = "s" if diff > 1 else ""
                ret += f"Anime {i[0]} have {diff} new episode{append}.\n"
                Database.command(f'''UPDATE anime_ongoing SET latest_ep = {i[2]}, update_date = '{i[4]}' 
                                     WHERE name LIKE '{i[0]}' ''')
    ret = ret.replace("_", " ")
    System.datewrite("anime", delta.days)
    return ret
