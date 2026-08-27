#!/usr/bin/env python3

import json
from pathlib import Path

BASE = Path(__file__).parent

STATIONS = BASE / "data/stations.json"
FAVORITES = BASE / "data/favorites.json"

PLAYLIST = BASE / "playlist"


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def make_m3u(name, stations):

    out = PLAYLIST / name

    with open(out, "w", encoding="utf-8") as f:

        f.write("#EXTM3U\n\n")

        for st in stations:

            sid = st["id"]
            title = st.get("name", sid)

            f.write(
                f"#EXTINF:-1,{title}\n"
            )

            f.write(
                f"https://radiko.jp/live/{sid}\n\n"
            )

    print("Saved:", out)
    print("Count:", len(stations))


def main():

    PLAYLIST.mkdir(exist_ok=True)

    stations = load_json(STATIONS)


    # 全局
    make_m3u(
        "radiko-all.m3u",
        stations
    )


    # お気に入り
    fav_data = load_json(FAVORITES)


    fav_keys = {
        f'{x["area_id"]}:{x["id"]}'
        for x in fav_data
    }


    fav = [
        x for x in stations
        if f'{x["area_id"]}:{x["id"]}' in fav_keys
    ]


    make_m3u(
        "favorites.m3u",
        fav
    )


if __name__ == "__main__":
    main()
