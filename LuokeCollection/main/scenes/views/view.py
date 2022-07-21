import pygame
from pygame.locals import *
from ..utils import vec
from .components.button import Button
from .components.background import Background
from LuokeCollection.settings.dev import WIDTH, HEIGHT
from ..mouse import Mouse

class View:
    BUTTONS = {
        "pop": Button(x=700, y=100),
    }
    OTHERS = {}

    def __init__(self, screen, bg=None):
        if not bg:
            bg = pygame.Surface([WIDTH, HEIGHT])
            bg.fill((0, 0, 0))
        self.background = Background(bg)
        self.screen = screen
        self.is_pointer = False
        self.buttons_group = pygame.sprite.Group()
        self.others_group = pygame.sprite.Group()

    def display(self, mouse_pos, click_pos):
        self.background.draw(self.screen)
        self.others_group.draw(self.screen)
        self.buttons_group.draw(self.screen)
        Mouse.draw(self.screen, mouse_pos, self.is_pointer)

    def update(self, mouse_pos, click_pos):
        for button in self.BUTTONS.values():
            if button.is_click(click_pos):
                button.click()

    def load_items(self):
        self.others_group.empty()
        self.buttons_group.empty()
        self.others_group.add(list(self.OTHERS.values()))
        self.buttons_group.add(list(self.BUTTONS.values()))
