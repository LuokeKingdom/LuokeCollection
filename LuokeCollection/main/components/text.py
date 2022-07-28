import pygame
from pygame.locals import *
from ..utils import vec
from .container import Container
from LuokeCollection.settings.dev import WIDTH, HEIGHT

pygame.font.init()
fontObj = pygame.font.Font("LuokeCollection/assets/fonts/chinese.ttf", 128)
default_text = fontObj.render("test text", True, (0, 0, 0))


class Text(Container):
    def __init__(self, image=default_text):
        super().__init__(image=image)
        self.text_color = (0, 0, 0)
        self.image = fontObj.render("test text", True, self.text_color)
        self.rect = self.image.get_rect()
        self.set_pos(WIDTH / 2, HEIGHT / 2)

    def update(self):
        pass
