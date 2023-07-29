import os
from datetime import *
import dotenv
import requests
import re
import html
import Database


def now() -> datetime:
    return datetime.now()


def today() -> date:
    return date.today()


def date_work() -> date:
    workout_date = (Database.command(f'''SELECT date from System_time WHERE type='workout' ''')[0][0])
    return workout_date


def date_write(typ: str, add: int) -> None:
    sql = f'''SELECT date from System_time WHERE type='{typ}' '''
    get_date = (Database.command(sql)[0][0])
    add = timedelta(days=add)
    get_date += add
    Database.command(f"UPDATE System_time SET date='{get_date}' WHERE type='{typ}'")


def time_to_human(input_time: str) -> str:
    seconds = int(input_time)
    periods = [
        ('month', 60 * 60 * 24 * 30),
        ('day', 60 * 60 * 24),
        ('hour', 60 * 60),
        ('minute', 60),
        ('second', 1)]
    strings = []
    for period_name, period_seconds in periods:
        if seconds > period_seconds:
            period_value, seconds = divmod(seconds, period_seconds)
            has_s = 's' if period_value > 1 else ''
            strings.append(f"{period_value} {period_name}{has_s}")
    return ", ".join(strings)


def add_time(input_time: datetime, delta: list) -> datetime:
    if len(delta) == 2:
        input_time += timedelta(days=int(delta.pop(0)))
    input_time += timedelta(hours=int(delta[0]))
    return input_time


def parse_url(url: str) -> str:
    return (url[26:-1]).replace("-", " ").title()


def parse_page(url: str) -> tuple[str, str, int, list, int]:
    page_html = html.unescape(requests.get(url).text)
    name = re.findall("<title> (.*?) - AnimeDao</title>", page_html)[0]
    anime_type = re.findall('Status:</b></td><td class="align-middle">(.*?)</td>', page_html)[0]
    episode = len(re.findall('Episode (\d+)', page_html)) // 3
    mal_link = re.findall('https://myanimelist\.net/anime/([^"]+)', page_html)[0]
    try:
        remain = re.findall('\d+', re.findall('\d+ \S+(?: \S+ \d+ \S+)? left', page_html)[0])
    except IndexError:
        remain = "0"
    return name, anime_type, episode, remain, mal_link


workout_begin = datetime(year=2023, month=1, day=1)


def split_lines(data: str) -> str | list[str]:
    if len(data) < 2000:
        return data
    else:
        ret = []
        while len(data) >= 2000:
            split_num = 1
            split = data.rsplit("\n", split_num)
            while len(split[0]) >= 2000:
                split_num += 1
                split = data.rsplit("\n", split_num)
            ret.append(split[0])
            data = data.replace(split[0] + "\n", "")
        ret.append(data)
        return ret


def credentials(typ: str):
    return os.environ.get(typ)


dotenv.load_dotenv("../Credentials.env")
print("")
