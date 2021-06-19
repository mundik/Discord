import psycopg2


def add_finished_anime(name, curr_ep, ep):
    conn, cur = connect()
    sql = f'''INSERT INTO anime_finished(name, current_ep, episodes) VALUES('{name}', {curr_ep}, {ep})'''
    try:
        cur.execute(sql)
        add_anime_list(cur, name, typ="finished")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        disconnect(conn)


def add_ongoing_anime(name, ep, last, day, update_date, update_time):
    conn, cur = connect()
    sql = f'''INSERT INTO anime_ongoing(name, current_ep, latest_ep, day, update_date, update_time) 
VALUES('{name}', {ep}, {last}, '{day}', {update_date}, {update_time})'''
    try:
        cur.execute(sql)
        add_anime_list(cur, name, typ="ongoing")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        disconnect(conn)


def add_anime_list(cur, name, typ):
    sql = f'''INSERT INTO anime_list(name, type) VALUES('{name}', '{typ}')'''
    cur.execute(sql)


def get_anime_type(name):
    conn, cur = connect()
    sql = f'''SELECT type FROM anime_list as Anime where Anime.name = '{name}' '''
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
        sql = f'''SELECT "current_ep" FROM anime_ongoing as Anime where Anime.name = '{name}' '''
    elif typ == "finished":
        sql = f'''SELECT "current_ep" FROM anime_finished as Anime where Anime.name = '{name}' '''
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
        ret = cur.fetchall()
    except psycopg2.ProgrammingError:
        disconnect(conn)
    except psycopg2.OperationalError:
        exit("Cannot connect to database.")
    else:
        disconnect(conn)
        return ret


def add_note(name, time, text, repeat):
    conn, cur = connect()
    sql = f'''INSERT INTO notes(name, time, repeat, text) VALUES('{name}', '{time}', {repeat}, '{text}')'''
    cur.execute(sql)
    disconnect(conn)


def add_repeat_note(name, time, text, interval, repeat):
    conn, cur = connect()
    sql = f'''INSERT INTO notes(name, time, repeat, every,text)VALUES('{name}','{time}',{repeat},{interval},'{text}')'''
    cur.execute(sql)
    disconnect(conn)


def connect():
    conn = psycopg2.connect(
        host="ec2-176-34-222-188.eu-west-1.compute.amazonaws.com",
        database="d4o5mkpmeckcat",
        user="yrzjbiwgpfrlgj",
        password="9de630f05402aa55664087645ecc1e278f943c0f7ad78f62d9c8432dadd5351f",
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
