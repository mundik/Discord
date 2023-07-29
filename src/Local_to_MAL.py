import re
import Mal_Api
with open("../Anime.txt", encoding="utf-8") as source:
    content = source.read()
    list_anime = re.findall("\*\*\*Watched\*\*\*:\n([^\*]+)\n\n", content)[0].split("\n")
    for i in list_anime:
        anime_name = i.split("(")[0].split("[")[0]
        anime = Mal_Api.find_anime(anime_name)
        print(anime)
