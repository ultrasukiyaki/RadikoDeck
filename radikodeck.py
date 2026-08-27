#!/usr/bin/env python3

import argparse

from database.stations import (
    load,
    merge
)

from collectors.streamlink import (
    collect
)

from generators.m3u import (
    generate_m3u
)


def main():

    parser = argparse.ArgumentParser(
        prog="radikodeck"
    )


    sub = parser.add_subparsers(
        dest="cmd"
    )


    sub.add_parser("list")
    sub.add_parser("make")
    sub.add_parser("update")


    args = parser.parse_args()


    if args.cmd == "list":

        for s in load():

            status = ""

            if s.get("available"):
                status="OK"

            print(
                f'{s["id"]:8} {s["name"]:20} {status}'
            )


    elif args.cmd == "make":

        generate_m3u(
            load(),
            "output/radiko.m3u"
        )


    elif args.cmd == "update":

        print(
            "Collecting stations..."
        )


        stations = collect()


        merge(stations)


        print(
            "Database updated."
        )


if __name__=="__main__":

    main()
