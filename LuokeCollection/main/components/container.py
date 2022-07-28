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

    def set_pos(self, x, y=None):
        if y is None:
            self.rect.center = vec(x[0], x[1])
        else:
            self.rect.center = vec(x, y)

    def update(self):
        pass
