import psycopg2


def add_finished_anime(name, curr_ep, ep):
    conn, cur = connect()
    sql = f'''INSERT INTO "anime_finished"(name, current_ep, episodes) VALUES('{name}', {curr_ep}, {ep})'''
    try:
        cur.execute(sql)
        if add_anime_list(cur, name, typ="finished"):
            return True
        return False
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return False
    finally:
        disconnect(conn)


def add_ongoing_anime(name, ep, last, update_date, update_time):
    conn, cur = connect()
    sql = f'''INSERT INTO "anime_ongoing"(name, current_ep, latest_ep, update_date, update_time)
VALUES('{name}', {ep}, {last}, '{update_date}', {update_time})'''
    try:
        cur.execute(sql)
        if add_anime_list(cur, name, typ="ongoing"):
            return True
        return False
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return False
    finally:
        disconnect(conn)


def add_anime_list(cur, name, typ):
    sql = f'''INSERT INTO "anime_list"(name, type) VALUES('{name}', '{typ}')'''
    try:
        cur.execute(sql)
        return True
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return False


def get_anime_type(name):
    conn, cur = connect()
    sql = f'''SELECT type FROM "anime_list" as Anime where Anime.name = '{name}' '''
    try:
        cur.execute(sql)
        ret = cur.fetchall()
        if len(ret) is not 0:
            ret = ret[0][0]
        disconnect(conn)
        return ret
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        disconnect(conn)


def get_anime(name):
    conn, cur = connect()
    typ = get_anime_type(name)
    if typ == "ongoing":
        sql = f'''SELECT "current_ep" FROM "anime_ongoing" as Anime where Anime.name = '{name}' '''
    elif typ == "finished":
        sql = f'''SELECT "current_ep" FROM "anime_finished" as Anime where Anime.name = '{name}' '''
    else:
        return "", ""
    cur.execute(sql)
    ret = cur.fetchall()
    disconnect(conn)
    return ret, typ


def command(sql):
    conn = ""
    try:
        conn, cur = connect()
        cur.execute(sql)
        try:
            ret = cur.fetchall()
        except psycopg2.ProgrammingError:
            ret = ""
        return ret
    except psycopg2.ProgrammingError:
        exit(f"Wrong SQL request: {sql}")
    except psycopg2.OperationalError:
        exit("Cannot connect to database.")
    finally:
        disconnect(conn)


def add_note(name, date, time, text, repeat):
    conn, cur = connect()
    sql = f'''INSERT INTO "notes"(name, date, time, repeat, text) VALUES('{name}', '{date}', '{time}', {repeat}, '{text}')'''
    cur.execute(sql)
    disconnect(conn)


def add_repeat_note(name, time, text, interval, repeat):
    conn, cur = connect()
    sql = f'''INSERT INTO "notes"(name, time, repeat, every,text)VALUES('{name}','{time}',{repeat},{interval},'{text}')'''
    cur.execute(sql)
    disconnect(conn)


def connect():
    conn = psycopg2.connect(
        host="ec2-52-209-134-160.eu-west-1.compute.amazonaws.com",
        database="del99f25i2or5s",
        user="brmccgpbxwkoki",
        password="a8b81c8a496be8142dfed4e75ea3e2379f4fbf56ebddc81bb0210ca44d8bb8a2",
        sslmode='require')
    cur = conn.cursor()
    return conn, cur


def connect_local():
    conn = psycopg2.connect(
        host="localhost",
        database="Mundik",
        user="postgres",
        password="osamelka2")
    cur = conn.cursor()
    return conn, cur


def disconnect(conn):
    conn.commit()
    if conn is not None:
        conn.close()
