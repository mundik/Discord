import mysql.connector


def add_finished_anime(name, curr_ep, ep, url):
    conn, cur = connect()
    sql = f'''INSERT INTO anime_finished (name, current_ep, episodes, url) VALUES
    ("{name}", {curr_ep}, {ep}, "{url}")'''
    try:
        cur.execute(sql)
        if add_anime_list(cur, name, typ="finished"):
            return True
        return False
    except (Exception, mysql.connector.DatabaseError) as error:
        print(error)
        return False
    finally:
        disconnect(conn)


def add_ongoing_anime(url, name, ep, last, update_date, update_time):
    conn, cur = connect()
    sql = f'''INSERT INTO anime_ongoing (name, current_ep, latest_ep, update_date, update_time, url)
VALUES("{name}", {ep}, {last}, '{update_date}', {update_time}, "{url}")'''
    try:
        cur.execute(sql)
        if add_anime_list(cur, name, typ="ongoing"):
            return True
        return False
    except (Exception, mysql.connector.DatabaseError) as error:
        print(error)
        return False
    finally:
        disconnect(conn)


def add_anime_list(cur, name, typ):
    sql = f'''INSERT INTO anime_list(name, type) VALUES("{name}", "{typ}")'''
    try:
        cur.execute(sql)
        return True
    except (Exception, mysql.connector.DatabaseError) as error:
        print(error)
        return False


def get_anime_type(name):
    conn, cur = connect()
    sql = f'''SELECT type FROM anime_list where name LIKE "%{name}%" '''
    try:
        cur.execute(sql)
        ret = cur.fetchall()
        if len(ret) != 0:
            ret = ret[0][0]
        disconnect(conn)
        return ret
    except (Exception, mysql.connector.DatabaseError) as error:
        print(error)
        disconnect(conn)


def get_anime(name):
    conn, cur = connect()
    typ = get_anime_type(name)
    if typ == "ongoing":
        sql = f'''SELECT "current_ep" FROM "anime_ongoing" where name LIKE "%{name}%" '''
    elif typ == "finished":
        sql = f'''SELECT "current_ep" FROM "anime_finished" where name LIKE "%{name}%" '''
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
        except mysql.connector.ProgrammingError:
            ret = ""
        return ret
    except mysql.connector.ProgrammingError:
        exit(f"Wrong SQL request: {sql}")
    except mysql.connector.OperationalError:
        exit("Cannot connect to database.")
    finally:
        disconnect(conn)


def add_note(name, date, time, text, repeat):
    conn, cur = connect()
    sql = f'''INSERT INTO notes(name, date, time, repeat, text) VALUES('{name}', '{date}', '{time}', {repeat}, '{text}')'''
    cur.execute(sql)
    disconnect(conn)


def add_repeat_note(name, time, text, interval, repeat):
    conn, cur = connect()
    sql = f'''INSERT INTO notes(name, time, repeat, every,text)VALUES('{name}','{time}',{repeat},{interval},'{text}')'''
    cur.execute(sql)
    disconnect(conn)


def connect():
    conn = mysql.connector.connect(password='Iin++dmiFqTQ^sD2!jjwwZ05', database='s83933_PROJECT_ECHELON',
                              host='51.77.202.155', user='u83933_yhy1QuwcdF')
    cur = conn.cursor()
    return conn, cur


def disconnect(conn):
    conn.commit()
    if conn is not None:
        conn.close()
