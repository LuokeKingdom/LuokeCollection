import pygame
from pygame.locals import *  # noqa
from .container import Container

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

    def change_text(self, text, color=None):
        self.text = text
        if color is None:
            color = self.color
        self.image = Text.get_font(self.size).render(text, True, color)
        self.image.set_alpha(self.opacity)
        temp_pos = self.get_pos()
        self.rect = self.image.get_rect()
        self.set_pos(temp_pos)

    def hide(self):
        self.image = Text.get_font(self.size).render(self.text, True, self.color)
        self.image.set_alpha(0)
        temp_pos = self.get_pos()
        self.rect = self.image.get_rect()
        self.set_pos(temp_pos)

    def show(self):
        self.change_text(self.text)

    def update(self):
        pass

    def get_font(size):
        return __class__.fontsizes.get(
            size,
            pygame.font.Font("assets/fonts/chinese.ttf", size),
        )
