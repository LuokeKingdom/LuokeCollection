from LuokeCollection.settings.dev import IMAGE
from ...mixin import Mixin
import pygame
from pygame.locals import *


class FrameMixin(Mixin):
    def effect(self, current_time):
        self.frame_image = IMAGE(
            self.path + str(self.current_frame) + ".png", False
        )
        self.button.image = self.frame_image
        if self.current_frame < self.transition:
            self.current_frame += 1

    def reset(self):
        self.button.image = self.button.original_image
        self.current_frame = 1
