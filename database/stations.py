import json
from pathlib import Path


BASE = Path(__file__).parent.parent

STATION_FILE = BASE / "data" / "stations.json"


def load():

    if not STATION_FILE.exists():
        return []

    with open(STATION_FILE, encoding="utf-8") as f:
        return json.load(f)



def save(stations):

    STATION_FILE.parent.mkdir(
        exist_ok=True
    )

    with open(
        STATION_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            stations,
            f,
            indent=2,
            ensure_ascii=False
        )



def merge(new_stations):

    current = load()

    index = {
        s["id"]: s
        for s in current
    }


    for st in new_stations:

        index[st["id"]] = st


    result = list(
        index.values()
    )


    save(result)

    return result
