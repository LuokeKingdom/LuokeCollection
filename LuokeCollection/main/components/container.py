import pygame
from pygame.locals import *
from ..utils import vec


class Container(pygame.sprite.Sprite):
    def __init__(
        self, image, width=None, height=None, ratio=1, align_mode="CENTER", x=0, y=0
    ):
        super().__init__()
        if width and height:
            self.image = pygame.transform.smoothscale(image, (width, height))
        else:
            self.image = pygame.transform.smoothscale(
                image, (int(image.get_width() * ratio), int(image.get_height() * ratio))
            )
        self.rect = self.image.get_rect()
        self.original_image = self.image.copy()
        self.original_rect = self.original_image.get_rect()
        self.align_mode = align_mode
        self.check_collide_original_rect = False
        self.set_pos(x, y)

    def set_pos(self, x, y=None):
        pos = None
        if y is None:
            pos = (x[0], x[1])
        else:
            pos = (x, y)
        if self.align_mode == "CENTER":
            self.rect.center = pos
            self.original_rect.center = pos
        elif self.align_mode == "TOPLEFT":
            self.rect.topleft = pos
            self.original_rect.topleft = pos
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
