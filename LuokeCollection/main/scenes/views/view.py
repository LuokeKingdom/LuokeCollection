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
    BUTTONS = {
        'test_button': Button(x=100,y=100)
    }
    OTHERS = {}

    def __init__(self):
        bg = pygame.Surface([WIDTH,HEIGHT])
        bg.fill(0,0,0)
        self.background = Background(bg)
        self.buttons_group = pygame.sprite.Group()
        self.others_group = pygame.sprite.Group()

    def display(self, screen):
        self.background.draw(screen)
        self.others_group.draw(screen)
        self.buttons_group.draw(screen)
    
    def update(self, click_pos):
        for button in self.BUTTONS.values():
            if button.is_click(click_pos):
                button.click()

    def load_items(self):
        self.others_group.empty()
        self.buttons_group.empty()
        self.others_group.add(list(self.others.values()))
        self.buttons_group.add(list(self.buttons.values()))
    