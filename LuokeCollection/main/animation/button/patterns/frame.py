from ...mixin import Mixin
import pygame
from pygame.locals import *


class FrameMixin(Mixin):
    def effect(self, current_time):
        self.frame_path = self.parameter + str(self.current_frame) + ".png"
        self.frame_image = pygame.image.load(self.frame_path)
        self.button.image = self.frame_image
        if self.current_frame < self.transition:
            self.current_frame += 1

    def reset(self):
        self.button.image = self.button.original_image
        self.current_frame = 1
