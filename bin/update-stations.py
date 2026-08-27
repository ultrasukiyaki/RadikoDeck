#!/usr/bin/env python3

import json
import time
from pathlib import Path
import requests
from xml.etree import ElementTree as ET


OUT = Path("data/stations.json")

BASE_URL = "https://radiko.jp/v3/station/list/JP{}.xml"


def fetch_area(area):

    url = BASE_URL.format(area)

    for retry in range(3):

        try:
            print(f"[GET] {url}")

            r = requests.get(
                url,
                timeout=10,
                headers={
                    "User-Agent": "RadikoDeck/1.0"
                }
            )

            r.raise_for_status()

            r.encoding = "utf-8"

            return r.text

        except Exception as e:
            print(
                f"[WARN] JP{area} retry {retry+1}: {e}"
            )
            time.sleep(1)

    return None



def parse(xml):

    root = ET.fromstring(xml)

    area_id = root.attrib.get("area_id")
    area_name = root.attrib.get("area_name")

    stations=[]

    for st in root.findall("station"):

        sid = st.findtext("id")

        if not sid:
            continue

        logo = None

        lg = st.find("logo")

        if lg is not None:
            logo = lg.text

        stations.append({
            "id": sid,
            "name": st.findtext("name"),
            "ascii_name": st.findtext("ascii_name"),
            "area_id": area_id,
            "area_name": area_name,
            "logo": logo
        })

    return stations



def main():

    result=[]

    for area in range(1,48):

        xml = fetch_area(area)

        if not xml:
            print(
                f"[FAIL] JP{area:02d}"
            )
            continue


        try:
            stations=parse(xml)

            print(
                f"JP{area:02d}: {len(stations)}"
            )

            result.extend(stations)

        except Exception as e:
            print(
                f"[PARSE FAIL] JP{area:02d}: {e}"
            )


    # unique
    uniq={}

    for s in result:
        uniq[f'{s["area_id"]}:{s["id"]}']=s


    result=list(uniq.values())


    OUT.write_text(
        json.dumps(
            result,
            ensure_ascii=False,
            indent=4
        ),
        encoding="utf-8"
    )


    print()
    print(
        "Stations:",
        len(result)
    )

    print(
        "Areas:",
        len(set(
            x["area_id"]
            for x in result
        ))
    )


if __name__=="__main__":
    main()
