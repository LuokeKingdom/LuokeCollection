import pygame
from pygame.locals import *
from ..utils import vec
from .container import Container
from LuokeCollection.settings.dev import WIDTH, HEIGHT

pygame.font.init()

DEFAULT_SIZE = 32


class Text(Container):
    fontsizes = {}
    pygame.font.Font("assets/fonts/chinese.ttf", DEFAULT_SIZE)

    def __init__(
        self,
        text="test text",
        size=DEFAULT_SIZE,
        align_mode="TOPLEFT",
        color=(0, 0, 0),
        opacity=255,
        *args,
        **kwargs
    ):
        super(Text, self).__init__(
            image=pygame.Surface([1, 1]), align_mode=align_mode, *args, **kwargs
        )
        self.text = text
        self.size = size
        self.color = color
        self.opacity = opacity
        self.change_text(text)
        self.align_mode = align_mode

    def change_text(self, text):
        self.text = text
        self.image = Text.get_font(self.size).render(text, True, self.color)
        self.image.set_alpha(self.opacity)
        temp_pos = self.get_pos()
        self.rect = self.image.get_rect()
        self.set_pos(temp_pos)

    def update(self):
        pass

    def get_font(size):
        return __class__.fontsizes.get(
            size,
            pygame.font.Font("assets/fonts/chinese.ttf", size),
        )
