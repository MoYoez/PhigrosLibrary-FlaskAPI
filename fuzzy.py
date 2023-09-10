import difflib
from pathlib import Path


load_songname_list = []
load_dict = {}

load_data = Path().absolute() / "info.csv"


with open(load_data, "r", encoding="utf-8") as f:
    reader = f.readlines()
    i = 0
    for row in reader:
        split_data = row.split("\\")
        # Generate a dict
        song_id = split_data[0]
        song_name = split_data[1]
        # load dict
        load_dict.update({song_name: song_id})
        load_songname_list.append(split_data[1])
        i + 1


def search_song(parmas: str):
    best_match = None
    best_ratio = 0
    for i in range(len(load_songname_list)):
        get_name = load_songname_list[i]
        # use fuzzy
        similarity_ratio = difflib.SequenceMatcher(None, parmas, get_name).ratio()
        if similarity_ratio > best_ratio:
            best_ratio = similarity_ratio
            best_match = get_name
    best_song_id = load_dict[best_match]
    return best_match, best_ratio, best_song_id
