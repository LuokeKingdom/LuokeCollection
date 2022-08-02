from tkinter import CENTER
from ...mixin import Mixin
import pygame
from pygame.locals import *


class JumpMixin(Mixin):
    def effect(self, current_time):
        self.button.check_collide_original_rect = True
        self.button.set_pos(self.x, self.y - self.jump_height * self.progress(current_time))
        self.button.original_rect = self.og_rect
        print(self.button.original_rect)

    def reset(self):
        self.button.set_pos(self.x ,self.y)
        print(self.button.original_rect)
