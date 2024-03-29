from LuokeCollection.main.components.text import Text
from ...mixin import Mixin
import pygame
from pygame.locals import *  # noqa


class ScaleMixin(Mixin):
    def effect(self, current_time=0.5):
        x_grow = self.w * self.scale - self.w
        y_grow = self.h * self.scale - self.h

        if self.scale < 1:
            self.button.check_collide_original_rect = True

        if self.button.text is None:
            self.button.image = pygame.transform.smoothscale(
                self.button.original_image,
                (
                    int(self.w + x_grow * self.progress(current_time)),
                    int(self.h + y_grow * self.progress(current_time)),
                ),
            )
        else:
            self.button.image = pygame.transform.smoothscale(
                pygame.Surface([100, 100]),
                (
                    int(self.w + x_grow * self.progress(current_time)),
                    int(self.h + y_grow * self.progress(current_time)),
                ),
            )
            self.button.image.fill(self.button.color)
            temp = Text.get_font(self.button.text_fontsize).render(
                self.button.text, True, self.button.text_color
            )
            rect = temp.get_rect(center=self.button.image.get_rect().center)
            self.button.image.blit(temp, rect)
        self.button.rect = self.button.image.get_rect(
            center=self.button.original_rect.center
        )
        pass

    def reset(self):
        self.button.image = self.button.original_image
        self.button.rect = self.button.original_rect
