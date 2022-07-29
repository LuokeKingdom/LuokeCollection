import pygame
from pygame.locals import *
from ..utils import vec
from .container import Container
from LuokeCollection.settings.dev import WIDTH, HEIGHT

pygame.font.init()
fontObj = pygame.font.Font("LuokeCollection/assets/fonts/chinese.ttf", 64)
default_text = fontObj.render("test text", True, (0, 0, 0))


class Text(Container):
    def __init__(self, text=None):
        self.text_color = (0, 0, 0)
        if text is not None:
            self.change_text(text)

    def change_text(self, text):
        self.image = fontObj.render(text, True, self.text_color)
        self.rect = self.image.get_rect()

    def update(self):
        pass
