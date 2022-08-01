from tkinter import CENTER
from ...mixin import Mixin
import pygame
from pygame.locals import *


class ScaleMixin(Mixin):
    def effect(self, current_time):
        self.button.image = pygame.transform.smoothscale(self.button.original_image, (self.w * self.scale, self.h * self.scale))
        self.button.rect = self.button.image.get_rect(center = self.button.original_rect.center)

    def reset(self):
        self.button.image = self.button.original_image
        self.button.rect = self.button.original_rect
