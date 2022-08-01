from tkinter import CENTER
from ...mixin import Mixin
import pygame
from pygame.locals import *


class JumpMixin(Mixin):
    def effect(self, current_time):
        self.button.check_collide_original_rect = True
        self.button.image.rect[1] -= self.jump_height
        print(self.button.rect)

    def reset(self):
        self.button.image = self.button.original_image
        self.button.rect = self.button.original_rect
        print(self.button.original_rect)
