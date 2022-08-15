from ...mixin import Mixin
import pygame
from pygame.locals import *


class FrameMixin(Mixin):
    def effect(self, current_time):
        self.button.image = self.frame_path
        if self.current_frame < self.transition:
            self.current_frame += 1

    def reset(self):
        self.button.image = self.button.original_image
