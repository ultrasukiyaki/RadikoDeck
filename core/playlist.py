#!/usr/bin/env python3

from pathlib import Path


BASE = Path(__file__).parent.parent

PLAYLIST_DIR = BASE / "playlist"


class Playlist:


    def __init__(self):

        PLAYLIST_DIR.mkdir(
            exist_ok=True
        )


    def write_m3u(self, filename, stations):

        path = PLAYLIST_DIR / filename

        with open(
            path,
            "w",
            encoding="utf-8"
        ) as f:

            f.write("#EXTM3U\n")

            for st in stations:

                sid = st["id"]

                name = st.get(
                    "name",
                    sid
                )

                f.write(
                    f"#EXTINF:-1,{name}\n"
                )

                f.write(
                    f"https://radiko.jp/live/{sid}\n"
                )


        print(
            "Saved:",
            path,
            "Count:",
            len(stations)
        )


    def all(self, stations):

        self.write_m3u(
            "radiko-all.m3u",
            stations
        )


    def favorites(
        self,
        stations,
        favorites
    ):

        keys = {
            (
                x["area_id"],
                x["id"]
            )
            for x in favorites
        }


        selected = [
            st
            for st in stations
            if (
                st.get("area_id"),
                st.get("id")
            )
            in keys
        ]


        self.write_m3u(
            "favorites.m3u",
            selected
        )
