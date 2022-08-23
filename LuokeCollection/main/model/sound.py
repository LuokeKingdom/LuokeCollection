import imp
import pygame
from pygame.locals import *
from pygame import mixer


mixer.init()


class Sound:
    def __init__(self, music):
        self.music = music
        self.music_playing = False

    def play(self):
        if self.music_playing:
            self._stop_music()
            self._unload_music()
            self._load_music()
            self._play_music()
        else:
            self._load_music()
            self._play_music()

    def _load_music(self):
        mixer.music.load(self.music)

    def _unload_music(self):
        mixer.music.unload()

    def _play_music(self):
        mixer.music.play(-1)
        self.music_playing = True

    def _pause_music(self):
        mixer.music.pause()

    def _unpause_music(self):
        mixer.music.unpause()

    def _stop_music(self):
        mixer.music.stop()
        self.music_playing = False
