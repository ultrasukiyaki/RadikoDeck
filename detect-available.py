#!/usr/bin/env python3

import json
from pathlib import Path
from streamlink import Streamlink
from streamlink.plugins.radiko import Radiko


BASE = Path(__file__).parent

STATIONS = BASE / "data/stations.json"
AVAILABLE = BASE / "data/available.json"
FAVORITES = BASE / "data/favorites.json"
REGION = BASE / "data/region.json"


# 除外対象
EXCLUDE_KEYWORDS = [
    "KOSHIEN",
    "高校野球",
    "オーディオ高校野球",
]


def get_region():
    s = Streamlink()

    p = Radiko(
        s,
        "https://radiko.jp/live/TBS"
    )

    token, area = p._authorize()

    return area


def is_valid_station(st):

    sid = st.get("id", "")
    name = st.get("name", "")

    text = sid + name

    for key in EXCLUDE_KEYWORDS:
        if key.lower() in text.lower():
            return False

    return True


def main():

    area_id = get_region()

    print("Detected area:", area_id)

    stations = json.loads(
        STATIONS.read_text(
            encoding="utf-8"
        )
    )


    available = []

    for st in stations:

        if st.get("area_id") != area_id:
            continue

        if not is_valid_station(st):
            continue

        available.append(st)



    REGION.write_text(
        json.dumps(
            {
                "area_id": area_id
            },
            ensure_ascii=False,
            indent=4
        ),
        encoding="utf-8"
    )


    AVAILABLE.write_text(
        json.dumps(
            available,
            ensure_ascii=False,
            indent=4
        ),
        encoding="utf-8"
    )


    FAVORITES.write_text(
        json.dumps(
            available,
            ensure_ascii=False,
            indent=4
        ),
        encoding="utf-8"
    )


    print(
        "Available stations:",
        len(available)
    )

    print(
        "Favorites generated:",
        len(available)
    )

    print(
        "Saved:",
        FAVORITES
    )


if __name__ == "__main__":
    main()
