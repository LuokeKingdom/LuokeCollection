from tkinter import CENTER
from ...mixin import Mixin
import pygame
from pygame.locals import *


class BounceMixin(Mixin):
    def effect(self, current_time):
        print(self.button.rect)

    def reset(self):
        self.button.image = self.button.original_image
        self.button.rect = self.button.original_rect
