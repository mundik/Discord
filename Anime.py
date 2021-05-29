from datetime import timedelta
import System

filepath = "Anime.txt"


def read_file():
    data_list = []
    anime_list = []
    with open("Anime.txt", "r+") as file:
        for i in file:
            name, rest = i[:-1].split(" ", maxsplit=1)
            temp = rest.split(" ")
            if len(temp) == 5:
                data_list.append({"name": name, "ep": int(temp[0]), "last": int(temp[1]),
                                  "day": temp[2], "update": temp[3]})
            elif len(temp) == 3:
                data_list.append({"name": name, "ep": int(temp[0]), "max_ep": int(temp[1])})
            anime_list.append(name)
    return data_list, anime_list


def write_file(data_list):
    with open("Anime.txt", "w") as file:
        for i in data_list:
            for j in i.values():
                file.write(str(j) + " ")
            file.write("\n")


def watched(name, ep):
    data_list, anime_list = read_file()
    if name in anime_list:
        for i in data_list:
            if i["name"] == name:
                i["ep"] += int(ep)
                break
        write_file(data_list)
        return f"Anime {name} updated."
    else:
        return f"Anime {name} not found."


def new_anime_going(name, ep, last, day, update):
    data_list, anime_list = read_file()
    if name in anime_list:
        return "Anime already on list"
    else:
        data_list.append({"name": name, "ep": ep, "last": last, "day": day, "update": update})
    write_file(data_list)
    return f"Anime {name} succesfully added."


def new_anime(name, ep, max_ep):
    data_list, anime_list = read_file()
    if name in anime_list:
        return "Anime " + name + " already added."
    else:
        data_list.append({"name": name, "ep": ep, "max_ep": max_ep})
    write_file(data_list)
    return f"Anime {name} succesfully added."


def delete_anime(name):
    data_list, anime_list = read_file()
    if name in anime_list:
        for i in data_list:
            if i["name"] == name:
                data_list.remove(i)
                anime_list.remove(name)
                break
        write_file(data_list)
        return f"Anime {name} was removed from watchlist."
    else:
        return "Anime not found."


def status():
    data_list, anime_list = read_file()
    ret = ""
    for i in data_list:
        try:
            ret += f"Name: {i['name']}, Episode: {i['ep']}, Last episode: {i['last']}," \
                   f" Airing in {i['day']} at {(i['update'].split('_'))[1]}:00\n"
        except KeyError:
            ret += f"Name: {i['name']}, Episode: {i['ep']} out of {i['max_ep']} \n"
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
    data_list, anime_list = read_file()
    ret = ""
    for i in data_list:
        try:
            diff = int(i["last"]) - int(i["ep"])
            if diff > 1:
                ret += f"Anime {i['name']} have {diff} unwatched episodes.\n"
            elif diff == 1:
                ret += f"Anime {i['name']} have {diff} unwatched episode.\n"
        except KeyError:
            pass
    ret = ret.replace("_", " ")
    return ret


def new_episode():
    data_list, anime_list = read_file()
    last_time = System.dateanime()
    today = System.today()
    delta = today - last_time
    ret = ""
    for j in range(0, delta.days + 1):
        day = (last_time + timedelta(days=j)).strftime("%a")
        for i in data_list:
            try:
                if i["day"] == day:
                    old = i["last"]
                    upd_date, upd_time = i["update"].split("_")
                    upd_time = int(upd_time)
                    upd_date = int(upd_date)
                    if upd_date == today.timetuple().tm_yday:
                        diff = upd_time - System.now().hour
                        if System.now().minute > 30:
                            diff -= 1
                        if diff > 0:
                            ret += f"Anime {i['name']} will have new episode in {diff} hours.\n"
                            continue
                        elif diff == 0:
                            ret += f"Anime {i['name']} will have new episode within hour.\n"
                            continue
                    if upd_date <= today.timetuple().tm_yday:
                        while upd_date <= today.timetuple().tm_yday:
                            i["last"] = f"{int(i['last'])+1}"
                            upd_date += 7
                            i["update"] = f"{upd_date}_{upd_time}"
                        ret += f"Anime {i['name']} have {int(i['last']) - int(old)} new episode.\n"
            except KeyError:
                pass
    ret = ret.replace("_", " ")
    write_file(data_list)
    System.datewrite("a", System.today())
    if ret == "":
        ret = "No anime to update."
    return ret
