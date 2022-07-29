import pygame
from pygame.locals import *
from ..utils import vec


class Container(pygame.sprite.Sprite):
    def __init__(self, image, width=None, height=None, ratio=1, x=0, y=0):
        super().__init__()
        if width and height:
            self.image = pygame.transform.scale(image, (width, height))
        else:
            self.image = pygame.transform.scale(
                image, (int(image.get_width() * ratio), int(image.get_height() * ratio))
            )
        self.original_image = self.image.copy()
        self.rect = self.image.get_rect()
        self.rect.center = vec(x, y)
        self.align_mode = "CENTER"

    def set_pos(self, x, y=None):
        pos = None
        if y is None:
            pos = vec(x[0], x[1])
        else:
            pos = vec(x, y)
        if self.align_mode == "CENTER":
            self.rect.center = pos
        elif self.align_mode == "TOPLEFT":
            self.rect.topleft = pos
        else:
            raise Exception("align_mode not found")

    def get_pos(self):
        if self.align_mode == "CENTER":
            return vec(self.rect.center)
        elif self.align_mode == "TOPLEFT":
            return vec(self.rect.topleft)
        else:
            raise Exception("align_mode not found")

    def update(self):
        pass
