#!/usr/bin/env python3

from streamlink import Streamlink
from streamlink.plugins.radiko import Radiko


RADIKO_TEST_URL = "https://radiko.jp/live/TBS"


def get_region():

    session = Streamlink()

    plugin = Radiko(
        session,
        RADIKO_TEST_URL
    )

    token, area_id = plugin._authorize()

    return {
        "token": token,
        "area_id": area_id
    }


if __name__ == "__main__":

    region = get_region()

    print(region)
