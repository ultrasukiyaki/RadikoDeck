#!/usr/bin/env python3

import os
import json
from collections import defaultdict


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DATA_FILE = os.path.join(
    BASE_DIR,
    "data",
    "stations.json"
)

PLAYLIST_DIR = os.path.join(
    BASE_DIR,
    "playlist"
)


def load_stations():

    with open(
        DATA_FILE,
        encoding="utf-8"
    ) as f:

        data = json.load(f)

    return data["stations"]



def write_m3u(filename, stations):

    path = os.path.join(
        PLAYLIST_DIR,
        filename
    )

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(
            "#EXTM3U\n"
        )

        for st in stations:

            f.write(
                "\n"
            )

            f.write(
                "#EXTINF:-1,"
                + st["name"]
                + "\n"
            )

            f.write(
                st["url"]
                + "\n"
            )

    print(
        f"[OK] {path} ({len(stations)} stations)"
    )



def main():

    os.makedirs(
        PLAYLIST_DIR,
        exist_ok=True
    )


    stations = load_stations()


    # 重複除去
    unique = {}

    for st in stations:

        key = st["id"]

        if key not in unique:
            unique[key] = st


    stations = list(
        unique.values()
    )


    # 名前順
    stations.sort(
        key=lambda x:
        x["name"]
    )


    #
    # 全国版
    #
    write_m3u(
        "radiko-all.m3u",
        stations
    )


    #
    # 地域別
    #
    areas = defaultdict(list)


    for st in stations:

        areas[
            st["area_id"]
        ].append(st)



    for area, items in areas.items():

        items.sort(
            key=lambda x:
            x["name"]
        )

        write_m3u(
            f"{area}.m3u",
            items
        )


if __name__ == "__main__":
    main()
