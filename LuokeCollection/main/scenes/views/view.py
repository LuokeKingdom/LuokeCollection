from re import S
from tkinter import W
import pygame
from pygame.locals import *
from ..utils import vec
from .components.button import Button
from .components.background import Background
from LuokeCollection.settings.dev import (
    WIDTH,
    HEIGHT
)

class View:
    def __init__(self):
        bg = pygame.Surface([WIDTH,HEIGHT])
        bg.fill(0,0,0)
        self.background = Background(bg)
        self.items = {
            'test_button': Button(x=100,y=100)
        }
        self.entities = pygame.sprite.Group()

    def display(self, screen):
        self.background.draw(screen)
        self.entities.draw(screen)

    def load_items(self):
        self.entities.empty()
        self.entities.add(list(self.items.values()))
    