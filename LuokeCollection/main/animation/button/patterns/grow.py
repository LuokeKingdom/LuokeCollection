from ...mixin import Mixin
import pygame
from pygame.locals import *


class GrowMixin(Mixin):
    def effect(self, current_time):
        self.button.set_pos(self.button.image.get_rect().center)
        self.button.image = pygame.transform.smoothscale(self.button.original_image, (self.w * self.scale, self.h * self.scale))

    def reset(self):
        self.button.image = pygame.transform.smoothscale(self.button.original_image, (self.w, self.h))