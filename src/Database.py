from datetime import *
from mysql.connector import *
from mysql.connector.cursor import MySQLCursor
from mysql.connector.cursor_cext import CMySQLCursor
from mysql.connector.pooling import PooledMySQLConnection
import System


def add_watching_anime(name: str, curr_ep: int, ep: int, url: str, mal_id: int) -> bool:
    conn, cur = db_connect()
    sql = f'''INSERT INTO anime_watching (name, current_ep, episodes, url, mal_id) VALUES
    ("{name}", {curr_ep}, {ep}, "{url}", {mal_id})'''
    try:
        cur.execute(sql)
        if add_anime_list(cur, name, mal_id, typ="finished"):
            return True
        return False
    except (Exception, DatabaseError) as error:
        print(error)
        return False
    finally:
        disconnect(conn)


def add_ongoing_anime(url: str, name: str, ep: int, last: int, update_time: datetime, mal_id: int) -> bool:
    conn, cur = db_connect()
    sql = f'''INSERT INTO anime_ongoing (name, current_ep, latest_ep, update_time, url, mal_id)
VALUES("{name}", {ep}, {last}, '{update_time}', "{url}", {mal_id})'''
    try:
        cur.execute(sql)
        if add_anime_list(cur, name, mal_id, typ="ongoing"):
            return True
        return False
    except (Exception, DatabaseError) as error:
        print(error)
        return False
    finally:
        disconnect(conn)


def add_finished_anime(url: str, name: str, mal_id: int) -> bool:
    conn, cur = db_connect()
    sql = f'''INSERT INTO anime_finished (name, url, mal_id, finish_time) VALUES("{name}", "{url}", {mal_id}, {System.now()})'''
    try:
        cur.execute(sql)
        return True
    except (Exception, DatabaseError) as error:
        print(error)
        return False
    finally:
        disconnect(conn)


def add_anime_list(cur: MySQLCursor | CMySQLCursor, name: str, mal_id: int, typ: str) -> bool:
    sql = f'''INSERT INTO anime_list(name, type, mal_id) VALUES("{name}", "{typ}", {mal_id})'''
    try:
        cur.execute(sql)
        return True
    except (Exception, DatabaseError) as error:
        print(error)
        return False


def get_anime_type(name: str) -> tuple[str, int]:
    conn, cur = db_connect()
    sql = f'''SELECT type, mal_id FROM anime_list where name LIKE "%{name}%"  '''
    try:
        cur.execute(sql)
        ret = cur.fetchall()
        if len(ret) != 0:
            typ, mal_id = ret[0]
            return typ, mal_id
        disconnect(conn)
    except (Exception, DatabaseError) as error:
        print(error)
        disconnect(conn)


def get_anime(name: str) -> tuple[list | str, str, str | int]:
    conn, cur = db_connect()
    typ, mal_id = get_anime_type(name)
    if typ == "ongoing":
        sql = f'''SELECT name, current_ep, FROM anime_ongoing where mal_id = {mal_id} '''
    elif typ == "finished":
        sql = f'''SELECT name, current_ep FROM anime_watching where mal_id = {mal_id} '''
    else:
        return "", "", ""
    cur.execute(sql)
    ret = cur.fetchall()
    disconnect(conn)
    return ret, typ, mal_id


def command(sql: str) -> list:
    conn = ""
    try:
        conn, cur = db_connect()
        cur.execute(sql)
        try:
            ret = cur.fetchall()
        except ProgrammingError:
            ret = ""
        return ret
    except ProgrammingError:
        exit(f"Wrong SQL request: {sql}")
    except OperationalError:
        exit("Cannot connect to database.")
    finally:
        disconnect(conn)


def add_note(name: str, note_date: str, note_time: str, text: str, repeat: str) -> None:
    conn, cur = db_connect()
    sql = f'''INSERT INTO notes(name, date, time, repeat, text) VALUES('{name}', '{note_date}', '{note_time}', {repeat}, '{text}')'''
    cur.execute(sql)
    disconnect(conn)


def add_repeat_note(name: str, note_time: datetime.time, text: str, interval: timedelta, repeat: bool) -> None:
    conn, cur = db_connect()
    sql = f'''INSERT INTO notes(name, time, repeat, every,text)VALUES('{name}','{note_time}',{repeat},{interval},'{text}')'''
    cur.execute(sql)
    disconnect(conn)


def db_connect() -> tuple[PooledMySQLConnection | MySQLConnection | CMySQLConnection, MySQLCursor | CMySQLCursor]:
    conn = connect(host=System.credentials("SQL_HOST"), password=System.credentials("SQL_PASSWORD"),
                   database=System.credentials("SQL_DATABASE"), user=System.credentials("SQL_USER"))
    cur = conn.cursor()
    return conn, cur


def disconnect(conn: MySQLConnection) -> None:
    conn.commit()
    if conn is not None:
        conn.close()
