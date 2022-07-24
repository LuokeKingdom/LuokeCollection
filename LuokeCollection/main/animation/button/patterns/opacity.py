from ...mixin import Mixin
import pygame
from pygame.locals import *


class OpacityMixin(Mixin):
    def effect(self, current_time):
        self.button.image.set_alpha(
            255 * (1 - self.progress(current_time) * self.opacity)
        )

    def reset(self):
        self.button.image.set_alpha(255)
