import pygame
from pygame.locals import *
from ..utils import Mouse
from ..components.button import Button
from ..components.background import Background
from LuokeCollection.settings.dev import WIDTH, HEIGHT


class View:
    INSTANCE = None

    def get_instance(*args, **kwargs):
        if __class__.INSTANCE is None:
            __class__.INSTANCE = __class__(*args, **kwargs)
        return __class__.INSTANCE

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

    def display(self, mouse_pos, clicked):
        self.background.draw(self.screen)
        self.others_group.draw(self.screen)
        self.buttons_group.draw(self.screen)
        Mouse.draw(self.screen, mouse_pos, self.is_pointer)

    def update(self, mouse_pos, clicked):
        btns = self.BUTTONS.values()
        others = self.OTHERS.values()
        for button in btns:
            button.hovered = False
        for button in btns:
            button.update(mouse_pos, clicked)
        for other in others:
            other.update()

    def load_items(self):
        self.others_group.empty()
        self.buttons_group.empty()
        self.others_group.add(list(self.OTHERS.values()))
        self.buttons_group.add(list(self.BUTTONS.values()))
