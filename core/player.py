#!/usr/bin/env python3

import subprocess
import shutil
import os
import json
import socket
import time


IPC_SOCKET = "/tmp/radikodeck.sock"


class Player:

    def __init__(self):

        self.process = None
        self.current_station = None



    def play(self, name, url):

        self.stop()


        mpv = shutil.which(
            "mpv"
        )


        if not mpv:

            raise RuntimeError(
                "mpv not found"
            )


        if os.path.exists(
            IPC_SOCKET
        ):

            os.remove(
                IPC_SOCKET
            )


        self.current_station = name


        self.process = subprocess.Popen(
            [
                mpv,
                "--no-video",
                f"--input-ipc-server={IPC_SOCKET}",
                url
            ]
        )


        time.sleep(0.3)



    def command(self, cmd):

        if not os.path.exists(
            IPC_SOCKET
        ):

            return None


        try:

            with socket.socket(
                socket.AF_UNIX,
                socket.SOCK_STREAM
            ) as s:

                s.connect(
                    IPC_SOCKET
                )


                s.send(
                    (
                        json.dumps(
                            {
                                "command": cmd
                            }
                        )
                        + "\n"
                    ).encode()
                )


                return json.loads(
                    s.recv(
                        4096
                    ).decode()
                )


        except Exception:

            return None



    def get_property(self, name):

        result = self.command(
            [
                "get_property",
                name
            ]
        )

        if result:

            return result.get(
                "data"
            )

        return None



    def status(self):

        return {

            "station":
                self.current_station,

            "volume":
                self.get_property(
                    "volume"
                ),

            "pause":
                self.get_property(
                    "pause"
                ),

            "mute":
                self.get_property(
                    "mute"
                )

        }



    def pause(self):

        return self.command(
            [
                "cycle",
                "pause"
            ]
        )



    def volume(self, value):

        return self.command(
            [
                "set_property",
                "volume",
                value
            ]
        )



    def mute(self):

        return self.command(
            [
                "cycle",
                "mute"
            ]
        )



    def current(self):

        return self.current_station



    def stop(self):

        if self.process:

            self.process.terminate()

            self.process = None


        if os.path.exists(
            IPC_SOCKET
        ):

            os.remove(
                IPC_SOCKET
            )


        self.current_station = None
