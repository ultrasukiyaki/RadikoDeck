#!/usr/bin/env python3

from core.radiko import get_region
from core.stations import Stations
from core.favorites import Favorites
from core.playlist import Playlist


class RadikoDeck:


    def __init__(self):


        self.stations = Stations()

        self.favorites = Favorites()

        self.playlist = Playlist()



    def show_area(self):

        info = get_region()

        print()

        print(
            "Area:",
            info["area_id"]
        )

        return info["area_id"]



    def show_stations(self, area_id):

        stations = self.stations.by_area(
            area_id
        )

        print()

        print(
            "Stations:",
            len(stations)
        )

        for i, st in enumerate(
            stations,
            1
        ):

            mark = "* " if self.favorites.contains(
                st["id"]
            ) else "  "

            print(
                f"{mark}{i}. {st['name']} ({st['id']})"
            )



    def make_playlist(self):

        self.playlist.all(
            self.stations.all()
        )


        self.playlist.favorites(
            self.stations.all(),
            self.favorites.all()
        )



def main():

    app = RadikoDeck()


    area = app.show_area()


    while True:

        print()

        print(
            "[1] Show stations"
        )

        print(
            "[2] Export playlist"
        )

        print(
            "[q] Quit"
        )


        cmd = input("> ")


        if cmd == "1":

            app.show_stations(
                area
            )


        elif cmd == "2":

            app.make_playlist()


        elif cmd == "q":

            break



if __name__ == "__main__":
    main()
