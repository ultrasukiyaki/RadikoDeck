# 📻 RadikoDeck

A modern desktop radio player for Radiko.

Built with Python and CustomTkinter.

## Features

- 📻 Radiko station browser
- 🔎 Station search
- ⭐ Favorite stations
- ▶ mpv based playback
- ⏸ Pause / volume / mute control
- 🎵 M3U playlist export
- 🌑 Dark modern UI
- 🖥 4K display friendly

## Requirements

- Python 3.12+
- mpv
- CustomTkinter

### Install dependencies

```bash
pip install customtkinter
```

Ubuntu / Debian:

```bash
sudo apt install mpv
```

## Run

```bash
python3 main.py
```

## Project Structure

```text
RadikoDeck/
├── core/
│   ├── player.py
│   ├── stations.py
│   ├── favorites.py
│   ├── playlist.py
│   └── radiko.py
│
├── interface/
│   ├── gui.py
│   ├── gui_controls.py
│   └── cli.py
│
├── collectors/
│   └── streamlink.py
│
├── generators/
│   └── m3u.py
│
├── database/
│   └── stations.py
│
├── data/
│   ├── stations.json
│   ├── region.json
│   └── available.json
│
└── main.py
```

## Architecture

RadikoDeck separates each component:

- UI layer
- Player engine
- Station database
- Favorite management
- Playlist generator

Playback is handled by **mpv** through IPC control.

## UI

Current UI features:

- Dark theme
- CustomTkinter based interface
- Station card display
- Favorite marking
- Active station highlighting
- Playback status display

## Development

RadikoDeck is designed to be extensible.

Future improvements:

- System tray integration
- Program information display
- Recording support
- More playlist formats
- Additional player backends

## License

MIT License
