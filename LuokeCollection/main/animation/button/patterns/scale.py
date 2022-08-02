from tkinter import CENTER
from ...mixin import Mixin
import pygame
from pygame.locals import *


class ScaleMixin(Mixin):
    def effect(self, current_time):
        x_grow = self.w * self.scale - self.w
        y_grow = self.h * self.scale - self.h
        
        if self.scale < 1:
            self.button.check_collide_original_rect = True

        self.button.image = pygame.transform.smoothscale(self.button.original_image, (self.w + x_grow * self.progress(current_time), self.h + y_grow * self.progress(current_time)))
        self.button.rect = self.button.image.get_rect(center = self.button.original_rect.center)

    def reset(self):
        self.button.image = self.button.original_image
        self.button.rect = self.button.original_rect
