from ...mixin import Mixin
import pygame
from pygame.locals import *  # noqa


class RotateMixin(Mixin):
    def effect(self, current_time):
        self.angle = 360 * self.rotation * self.progress(current_time)
        self.button.check_collide_original_rect = True
        self.image_copy = pygame.transform.rotate(
            self.button.original_image, self.angle
        ).copy()
        self.button.rect = pygame.Rect(
            self.x - int(self.image_copy.get_width() / 2),
            self.y - int(self.image_copy.get_height() / 2),
            self.w,
            self.h,
        )
        self.button.image = pygame.transform.rotate(
            self.button.original_image, self.angle
        )

    def reset(self):
        self.button.image = self.button.original_image
        self.button.rect = self.button.original_rect
        self.angle = 0
