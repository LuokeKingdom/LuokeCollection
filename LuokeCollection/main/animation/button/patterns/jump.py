from ...mixin import Mixin
import pygame
from pygame.locals import *


class JumpMixin(Mixin):
    def effect(self, current_time):
        self.button.check_collide_original_rect = True
        if self.progress(current_time) < 0.5:
            self.y_temp -= self.jump_height * self.progress(current_time) * 2
        else:
            self.y_temp = (self.y - self.jump_height) - self.jump_height * (1 - self.progress(current_time) * 2)
        self.button.rect = pygame.Rect(
            self.x,
            self.y_temp,
            self.w,
            self.h,
        )
        self.y_temp = self.y
        print(self.button.rect)

    def reset(self):
        self.button.rect = self.button.original_rect
        self.y_temp = self.y
        print(self.button.rect)
