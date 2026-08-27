#!/usr/bin/env python3

import json
from pathlib import Path


BASE = Path(__file__).parent.parent

STATIONS_FILE = BASE / "data/stations.json"


class Stations:


    def __init__(self):

        self.data = json.loads(
            STATIONS_FILE.read_text(
                encoding="utf-8"
            )
        )


    def all(self):

        return self.data



    def by_area(self, area_id):

        return [
            st
            for st in self.data
            if st.get("area_id") == area_id
        ]



    def find(self, area_id, station_id):

        for st in self.data:

            if (
                st.get("area_id") == area_id
                and
                st.get("id") == station_id
            ):
                return st


        return None
