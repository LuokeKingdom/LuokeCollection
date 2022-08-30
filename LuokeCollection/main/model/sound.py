from enum import Enum
import pygame
from pygame.locals import *  # noqa
from pygame import mixer


mixer.init()
mixer.set_num_channels(3)


class Channel(Enum):
    BACKGROUND = 0
    UI = 1
    GAME = 2


class Sound:
    def __init__(self, music, channel):
        self.sound = pygame.mixer.Sound(music)
        self.channel = channel

    def play(self):
        mixer.Channel(self.channel.value).play(
            self.sound, -1 if self.channel.value == 0 else 0
        )
