import imp
import pygame
from pygame.locals import *
from pygame import mixer


mixer.init()

class BackgroundMusic():
    def __init__(self, music):
        self.music = music
        if self.music is not None:
            self.unload_music()
        else:
            self.load_music(music)

    def load_music(self, music):
        mixer.music.load(music)

    def unload_music(self):
        mixer.music.unload()
    
    def play_music(self):
        mixer.music.play()

    def pause_music(self):
        mixer.music.pause()
    
    def unpause_music(self):
        mixer.music.unpause()

    def stop_music(self):
        mixer.music.stop()

    