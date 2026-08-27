#!/usr/bin/env python3

import json
from pathlib import Path


BASE = Path(__file__).parent.parent

FAVORITES_FILE = BASE / "data/favorites.json"


class Favorites:

    def __init__(self):

        if FAVORITES_FILE.exists():

            self.data = json.loads(
                FAVORITES_FILE.read_text(
                    encoding="utf-8"
                )
            )

        else:
            self.data = []


    def all(self):

        return self.data


    def ids(self):

        return [
            x["id"]
            for x in self.data
        ]


    def contains(self, station_id):

        return any(
            x["id"] == station_id
            for x in self.data
        )


    def add(self, area_id, station_id):

        if not self.contains(station_id):

            self.data.append(
                {
                    "area_id": area_id,
                    "id": station_id
                }
            )

            self.save()


    def remove(self, station_id):

        self.data = [
            x
            for x in self.data
            if x["id"] != station_id
        ]

        self.save()


    def save(self):

        FAVORITES_FILE.write_text(
            json.dumps(
                self.data,
                ensure_ascii=False,
                indent=4
            ),
            encoding="utf-8"
        )
