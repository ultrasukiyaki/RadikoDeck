from pathlib import Path


def generate_m3u(stations, output):

    lines = [
        "#EXTM3U"
    ]

    for st in stations:
        lines.append(
            f'#EXTINF:-1,{st["name"]}'
        )
        lines.append(
            f'https://radiko.jp/live/{st["id"]}'
        )

    Path(output).write_text(
        "\n".join(lines),
        encoding="utf-8"
    )
