from ...mixin import Mixin
import pygame
from pygame.locals import *


class FrameMixin(Mixin):
    def effect(self, current_time):
        self.button.image = self.frame

    def reset(self):
        self.button.image = self.button.original_image
