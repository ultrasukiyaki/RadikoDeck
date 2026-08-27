#!/usr/bin/env python3

import customtkinter as ctk
from tkinter import messagebox

from core.radiko import get_region
from core.stations import Stations
from core.playlist import Playlist
from core.favorites import Favorites
from core.player import Player
from interface.gui_controls import PlayerControls


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

ctk.set_widget_scaling(1.35)
ctk.set_window_scaling(1.15)


BG = "#181818"
CARD = "#242424"
SELECT = "#163a5f"
PLAY = "#0f2d4a"


def main():

    app = ctk.CTk()

    app.title("📻 RadikoDeck")
    app.geometry("650x900")
    app.configure(
        fg_color=BG
    )


    area = get_region()

    stations_db = Stations()

    stations_all = stations_db.by_area(
        area["area_id"]
    )

    favorites = Favorites()

    player = Player()

    controls = PlayerControls(
        player
    )


    selected_station = None
    playing_station = None


    station_buttons = {}


    playing_text = ctk.StringVar(
        value="⏹ Stopped"
    )


    ctk.CTkLabel(
        app,
        text="📻 RadikoDeck",
        font=("Sans",26,"bold")
    ).pack(
        pady=15
    )


    ctk.CTkLabel(
        app,
        text=f"Area : {area['area_id']}"
    ).pack()


    ctk.CTkLabel(
        app,
        textvariable=playing_text,
        font=("Sans",14)
    ).pack(
        pady=10
    )


    search = ctk.StringVar()


    ctk.CTkEntry(
        app,
        textvariable=search,
        placeholder_text="Search station..."
    ).pack(
        fill="x",
        padx=20,
        pady=10
    )


    frame = ctk.CTkScrollableFrame(
        app,
        fg_color=BG
    )

    frame.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=10
    )


    def update_colors():

        for sid, data in station_buttons.items():

            btn = data["button"]


            if selected_station == sid:

                btn.configure(
                    fg_color=SELECT
                )

            else:

                btn.configure(
                    fg_color=CARD
                )



    def redraw():

        for child in frame.winfo_children():

            child.destroy()


        station_buttons.clear()


        keyword = search.get().lower()


        for st in stations_all:


            if keyword:

                if (
                    keyword not in st["name"].lower()
                    and
                    keyword not in st["id"].lower()
                ):
                    continue


            sid = st["id"]


            fav = favorites.contains(
                sid
            )


            if playing_station == sid:

                play_mark = "▶ "

            else:

                play_mark = ""


            mark = "★" if fav else "☆"


            text = (
                f"{play_mark}{mark} {st['name']} ({sid})"
            )


            btn = ctk.CTkButton(
                frame,
                text=text,
                anchor="w",
                height=42,
                fg_color=CARD,
                command=lambda x=st: select_station(x)
            )


            btn.pack(
                fill="x",
                pady=3
            )


            station_buttons[sid] = {
                "button": btn,
                "station": st
            }


        update_colors()



    def select_station(st):

        nonlocal selected_station

        selected_station = st["id"]

        update_colors()

        playing_text.set(
            f"Selected : {st['name']} ({st['id']})"
        )



    def favorite():

        if not selected_station:

            return


        if favorites.contains(
            selected_station
        ):

            favorites.remove(
                selected_station
            )

        else:

            favorites.add(
                area["area_id"],
                selected_station
            )


        redraw()



    def play():

        nonlocal playing_station


        if not selected_station:

            messagebox.showwarning(
                "RadikoDeck",
                "Select station"
            )

            return


        st = next(
            x for x in stations_all
            if x["id"] == selected_station
        )


        player.play(
            f"{st['name']} ({st['id']})",
            f"https://radiko.jp/live/{st['id']}"
        )


        playing_station = selected_station


        redraw()


        playing_text.set(
            f"▶ Playing : {st['name']}"
        )



    def stop():

        nonlocal playing_station

        player.stop()

        playing_station = None

        redraw()

        playing_text.set(
            "⏹ Stopped"
        )



    search.trace_add(
        "write",
        lambda *args: redraw()
    )


    ctk.CTkButton(
        app,
        text="★ Favorite",
        command=favorite
    ).pack(
        pady=5
    )


    controls_frame = ctk.CTkFrame(
        app,
        fg_color=BG
    )

    controls_frame.pack(
        pady=10
    )


    ctk.CTkButton(
        controls_frame,
        text="▶ Play",
        command=play
    ).pack(
        side="left",
        padx=5
    )


    ctk.CTkButton(
        controls_frame,
        text="⏸ Pause",
        command=controls.pause
    ).pack(
        side="left",
        padx=5
    )


    ctk.CTkButton(
        controls_frame,
        text="⏹ Stop",
        command=stop
    ).pack(
        side="left",
        padx=5
    )


    def export():

        playlist = Playlist()

        all_stations = stations_db.all()

        playlist.all(
            all_stations
        )

        playlist.favorites(
            all_stations,
            favorites.all()
        )

        messagebox.showinfo(
            "RadikoDeck",
            "Playlist exported!"
        )


    ctk.CTkButton(
        app,
        text="🎵 Export M3U",
        command=export
    ).pack(
        pady=15
    )


    def close():

        player.stop()

        app.destroy()


    app.protocol(
        "WM_DELETE_WINDOW",
        close
    )


    redraw()

    app.mainloop()



if __name__ == "__main__":
    main()
