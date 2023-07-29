import requests
import System


def headers(auth: str = "basic") -> dict:
    header = {}
    if auth == "basic":
        header["X-MAL-CLIENT-ID"] = System.credentials("MAL_CLIENT_ID")
    elif auth == "advanced":
        header["Authorization"] = f"Bearer {System.credentials('MAL_ACCESS_TOKEN')}"
    return header


def get_anime_list(url: str) -> list:
    resp = requests.get(url, headers=headers())
    ret = resp.json()
    anime = []
    for i in ret["data"]:
        anime.append(i["node"]["id"])
    return anime


def find_anime(name: str, limit: int = 5) -> list:
    url = f"https://api.myanimelist.net/v2/anime?q={name}&limit={limit}"
    resp = requests.get(url, headers=headers(auth="advanced"))
    ret = resp.json()
    return ret["data"]


def get_id_from_anime(anime: dict) -> int:
    return anime["node"]["id"]


def update_anime(anime_id: int, data: str = ""):
    url = f"https://api.myanimelist.net/v2/anime/{anime_id}/my_list_status"
    resp = requests.put(url, headers=headers(auth="advanced"), data=data)
    ret = resp.json()
    print(ret)


# update_anime(get_id_from_anime(find_anime("Koikomo")[0]))
