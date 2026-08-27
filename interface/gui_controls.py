#!/usr/bin/env python3


class PlayerControls:

    def __init__(self, player):

        self.player = player
        self.volume_level = 70


    def pause(self):

        return self.player.pause()



    def volume_up(self):

        self.volume_level = min(
            100,
            self.volume_level + 10
        )

        return self.player.volume(
            self.volume_level
        )



    def volume_down(self):

        self.volume_level = max(
            0,
            self.volume_level - 10
        )

        return self.player.volume(
            self.volume_level
        )



    def mute(self):

        return self.player.mute()
