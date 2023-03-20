from datetime import timedelta
import System
import Database


def watched(name, add):
    if isinstance(name, tuple):
        name = " ".join(name)
    ret, typ = Database.get_anime(name)
    if len(ret) == 0:
        return f"Anime \"{name}\" not found."
    else:
        if not isinstance(add, int):
            return f"{add} is not a number."
        full_name, ep = ret[0]
        ep += + add
        if typ == "ongoing":
            sql = f'''UPDATE anime_ongoing SET current_ep = {ep} WHERE name LIKE "%{name}%" '''
        elif typ == "finished":
            sql = f'''UPDATE anime_finished SET current_ep = {ep} WHERE name LIKE "%{name}%" '''
        else:
            return "Database Error."
        Database.command(sql)
        return f"Anime \"{full_name}\" updated."


def new_anime_going(url, ep, last, update_time, name=None):
    if name is None:
        name = System.parse_url(url)
    elif isinstance(name, tuple):
        name = " ".join(name)
    find = Database.command(f'''SELECT * FROM anime_list where name LIKE "%{name}%" ''')
    if len(find) != 0:
        return f"Anime \"{name}\" already on list."
    else:
        if Database.add_ongoing_anime(url, name, ep, last, update_time):
            return f"Anime \"{name}\" succesfully added."
        return "Database error."


def new_anime(url, ep, max_ep, name=None):
    if name is None:
        name = System.parse_url(url)
    elif isinstance(name, tuple):
        name = " ".join(name)
    find = Database.command(f'''SELECT * FROM anime_list where name LIKE "%{name}%" ''')
    if len(find) != 0:
        return "Anime already on list."
    else:
        if Database.add_finished_anime(name, ep, max_ep, url):
            return f"Anime \"{name}\" succesfully added."
        return "Database error."


def new_anime_url(url):
    name, anime_type, episode, remain = System.parse_page(url)
    air_time = System.add_time(System.now(), remain)
    if air_time.minute >= 30:
        air_time = air_time.replace(second=0, microsecond=0, minute=0, hour=air_time.hour+1)
    else:
        air_time = air_time.replace(second=0, microsecond=0, minute=0)
    if anime_type == "Ongoing":
        ret = new_anime_going(url, 0, episode, air_time + timedelta(hours=1), name=name)
    else:
        ret = new_anime(url, 0, episode, name=name)
    return ret


def finished(name):
    if isinstance(name, tuple):
        name = " ".join(name)
    typ = Database.get_anime_type(name)
    if len(typ) == 0:
        return "Anime not found."
    if typ == "ongoing":
        sql = f'''DELETE FROM anime_ongoing where name LIKE "%{name}%" '''
    elif typ == "finished":
        sql = f'''DELETE FROM anime_finished where name LIKE "%{name}%" '''
    else:
        return f"Database Error: type: {typ}"
    Database.command(sql)
    Database.command(f'''DELETE FROM anime_list where name LIKE "%{name}%" ''')
    return f"Anime \"{name}\" was removed from watchlist."


def transfer(name):
    if isinstance(name, tuple):
        name = " ".join(name)
    data = Database.command(f'''SELECT * FROM anime_ongoing where name LIKE "%{name}%" ''')
    if len(data) > 0:
        data = data[0]
        finished(name)
        Database.add_finished_anime(data[0], data[1], data[2], data[5])
        return f"Anime \"{name}\" transfered from ongoing to finished."
    else:
        return f"Anime \"{name}\" not found."


def status():
    ret = ""
    data_list = Database.command(f'''SELECT * FROM anime_finished ''')
    for i in data_list:
        ret += f"Name: {i[0]}, Episode: {i[1]} out of {i[2]} \n"
    data_list = Database.command(f'''SELECT * FROM anime_ongoing ORDER BY update_time''')
    for i in data_list:
        ret += f"Name: {i[0]}, Episode: {i[1]}, Last episode: {i[2]}, Airing in {i[3].strftime('%A')} at {i[3].strftime('%H')}:00\n<{i[4]}>\n"
    ret = "No anime in database" if ret == "" else ret
    return ret


def waiting():
    data_list = Database.command(
        f'''SELECT name, current_ep, latest_ep  FROM anime_ongoing WHERE latest_ep > current_ep''')
    ret = ""
    for i in data_list:
        diff = i[2] - i[1]
        append = "s" if diff > 1 else ""
        ret += f"Anime \"{i[0]}\" have {diff} unwatched episode{append}.\n"
    ret = "Nothing on waitlist" if ret == "" else ret
    return ret


def change_time(name, hour):
    if isinstance(name, tuple):
        name = " ".join(name)
    Database.command(f'''UPDATE anime_ongoing SET update_time = {hour} WHERE name LIKE "%{name}%" ''')
    return f"Anime \"{name}\" update time set to {hour}:00"


def update():
    now = System.now()
    ret = ""
    day = (now + timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
    data_list = Database.command(f'''SELECT * FROM anime_ongoing WHERE update_time <= '{day}' ORDER BY update_time''')
    for i in data_list:
        name, ep, latest, update_time, url = i
        delta = (update_time - now).total_seconds()
        temp_update = update_time
        if temp_update >= now:
            diff = round(delta / 3600)
            if 24 > diff > 0:
                append = "s" if diff > 1 else ""
                ret += f"Anime \"{name}\" will have new episode in {diff} hour{append}.\n"
                continue
            elif diff == 0:
                if not int(System.parse_page(url)[2]) > latest:
                    ret += f"Anime \"{name}\" will have new episode within hour.\n"
                    continue
                else:
                    temp_update = now
        if temp_update <= now:
            released = int(System.parse_page(url)[2])
            old = latest
            while update_time <= now:
                if released > latest:
                    latest += 1
                update_time += timedelta(days=7)
            diff = latest - old
            if diff == 0:
                ret += f"Anime \"{name}\" don't have any new episode.\n"
            else:
                append = "s" if diff > 1 else ""
                ret += f"Anime \"{name}\" have {diff} new episode{append}.\n"
            Database.command(f'''UPDATE anime_ongoing SET latest_ep = {latest}, update_time = '{update_time}' WHERE name LIKE "%{name}%"''')
    ret = "Nothing to update" if ret == "" else ret
    return ret
