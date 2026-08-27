import subprocess


def check_station(station_id):

    url = (
        f"https://radiko.jp/live/{station_id}"
    )


    cmd = [
        "streamlink",
        "--can-handle-url",
        url
    ]


    try:

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )


        return result.returncode == 0


    except FileNotFoundError:

        return False



def collect():

    """
    Temporary collector.

    Later:
    - inspect streamlink plugin
    - auto discover stations

    """

    candidates = [

        {
            "id":"TBS",
            "name":"TBSラジオ"
        },

        {
            "id":"QRR",
            "name":"文化放送"
        },

        {
            "id":"LFR",
            "name":"ニッポン放送"
        },

        {
            "id":"MBS",
            "name":"MBSラジオ"
        }

    ]


    result=[]


    for st in candidates:

        if check_station(st["id"]):

            st["available"] = True
            result.append(st)

        else:

            st["available"] = False
            result.append(st)


    return result
