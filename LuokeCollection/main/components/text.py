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
        super(Text, self).__init__(default_text)
        self.text = text
        self.text_color = (0, 0, 0)
        if text is not None:
            self.change_text(text)
        self.align_mode = "TOPLEFT"
        self.set_pos(0, 0)

    def change_text(self, text):
        self.text = text
        self.image = fontObj.render(text, True, self.text_color)
        temp_pos = self.get_pos()
        self.rect = self.image.get_rect()
        self.set_pos(temp_pos)

    def update(self):
        self.set_pos(self.get_pos() + vec(1, 1))
        if self.get_pos().x%40==0:
            self.change_text(self.text + '!')
        pass
