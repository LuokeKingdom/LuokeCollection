from ...mixin import Mixin
import pygame
from pygame.locals import *


class FrameMixin(Mixin):
    def effect(self, current_time):
        pass

    def reset(self):
        self.button.image = self.button.original_image

