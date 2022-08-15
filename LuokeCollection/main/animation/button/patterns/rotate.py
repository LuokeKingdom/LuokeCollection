from ...mixin import Mixin
import pygame
from pygame.locals import *


class RotateMixin(Mixin):
    def effect(self, current_time):
        pass

    def reset(self):
        self.button.rect = self.button.original_rect
