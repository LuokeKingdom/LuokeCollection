from ...mixin import Mixin
import pygame
from pygame.locals import *


class JumpMixin(Mixin):
    def effect(self, current_time):
        self.button.check_collide_original_rect = True
        self.y_temp = (
            self.a
            * ((self.progress(current_time) * self.transition))
            * ((self.progress(current_time) * self.transition - self.transition))
        )
        self.button.rect = pygame.Rect(
            self.x,
            self.y + self.y_temp,
            self.w,
            self.h,
        )
        print(self.y_temp)

    def reset(self):
        self.button.rect = self.button.original_rect
