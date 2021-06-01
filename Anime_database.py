from datetime import timedelta
import System
import Database


def watched(name, add):
    ep, typ = Database.get_anime(name)
    if len(ep) == 0:
        return f"Anime {name} not found."
    else:
        ep = ep[0][0] + int(add)
        if typ == "ongoing":
            sql = f'''UPDATE anime_ongoing SET current_ep = {ep} WHERE name = '{name}' '''
        elif typ == "finished":
            sql = f'''UPDATE anime_finished SET current_ep = {ep} WHERE name = '{name}' '''
        else:
            return "error"
        Database.command(sql)
        return f"Anime {name} updated."


def new_anime_going(name, ep, last, day, update_date, update_time):
    sql = f'''SELECT * FROM anime_list as Anime where Anime.name = '{name}' '''
    find = Database.command(sql)
    if len(find) != 0:
        return "Anime already on list"
    else:
        sql = f'''INSERT INTO anime_ongoing(name, current_ep, latest_ep, day, update_date, update_time) 
    VALUES('{name}', {ep}, {last}, '{day}', {update_date}, {update_time})'''
        Database.command(sql)
        sql = f'''INSERT INTO anime_list(name, type) VALUES('{name}', 'ongoing')'''
        Database.command(sql)
        return f"Anime {name} succesfully added."


def new_anime(name, ep, max_ep):
    sql = f'''SELECT * FROM anime_list as Anime where Anime.name = '{name}' '''
    find = Database.command(sql)
    if len(find) != 0:
        return "Anime already on list"
    else:
        sql = f'''INSERT INTO anime_finished(name, current_ep, episodes) VALUES('{name}', {ep}, {max_ep})'''
        Database.command(sql)
        sql = f'''INSERT INTO anime_list(name, type) VALUES('{name}', 'finished')'''
        Database.command(sql)
        return f"Anime {name} succesfully added."


def delete_anime(name):
    sql = f'''SELECT * FROM anime_list as Anime where Anime.name = '{name}' '''
    find = Database.command(sql)
    if len(find) != 0:
        sql = f'''DELETE FROM anime_list as Anime where Anime.name = '{name}' '''
        Database.command(sql)
        return f"Anime {name} was removed from watchlist."
    else:
        return "Anime not found."


def status():
    ret = ""
    data_list = Database.command(f'''SELECT * FROM anime_finished''')
    for i in data_list:
        ret += f"Name: {i[0]}, Episode: {i[1]} out of {i[2]} \n"
    data_list = Database.command(f'''SELECT * FROM anime_ongoing''')
    for i in data_list:
        ret += f"Name: {i[0]}, Episode: {i[1]}, Last episode: {i[2]}, Airing in {i[3]} at {i[5]}:00\n"
    ret = ret.replace("_", " ")
    ret = ret.replace("Mon", "Monday")
    ret = ret.replace("Tue", "Tuesday")
    ret = ret.replace("Wed", "Wednesday")
    ret = ret.replace("Thu", "Thursday")
    ret = ret.replace("Fri", "Friday")
    ret = ret.replace("Sat", "Saturday")
    ret = ret.replace("Sun", "Sunday")
    return ret


def waiting():
    data_list = Database.command(
        f'''SELECT name, current_ep, latest_ep  FROM anime_ongoing WHERE latest_ep > current_ep''')
    ret = ""
    for i in data_list:
        diff = i[2] - i[1]
        if diff > 1:
            ret += f"Anime {i[0]} have {diff} unwatched episodes.\n"
        elif diff == 1:
            ret += f"Anime {i[0]} have {diff} unwatched episode.\n"
    ret = ret.replace("_", " ")
    return ret


def new_episode():
    last_time = System.dateanime()
    today = System.today()
    delta = today - last_time
    ret = ""
    for j in range(0, delta.days + 1):
        day = (last_time + timedelta(days=j)).strftime("%a")
        data_list = Database.command(
            f'''SELECT * FROM anime_ongoing WHERE day = '{day}' ''')
        for i in data_list:
            i = list(i)
            if i[4] == today.timetuple().tm_yday:
                diff = i[5] - System.now().hour
                if System.now().minute > 30:
                    diff -= 1
                if diff > 0:
                    ret += f"Anime {i[0]} will have new episode in {diff} hours.\n"
                    continue
                elif diff == 0:
                    ret += f"Anime {i[0]} will have new episode within hour.\n"
                    continue
            if i[4] <= today.timetuple().tm_yday:
                while i[4] <= today.timetuple().tm_yday:
                    i[2] += 1
                    i[4] += 7
                ret += f"Anime {i[0]} have {i[2] - i[1]} new episode.\n"
                Database.command(
                    f'''UPDATE anime_ongoing SET latest_ep = {i[2]}, update_date = {i[4]} WHERE name = '{i[0]}' ''')
    ret = ret.replace("_", " ")
    System.datewrite("anime", delta.days)
    return ret
