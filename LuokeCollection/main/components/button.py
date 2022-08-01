import pygame
from pygame.locals import *

from ..animation.button.button_animations import OpacityButtonAnimation, ScaleButtonAnimation
from ..utils import vec
from .container import Container

import time


class Button(Container):
    ANIMATIONS = {
        "opacity": OpacityButtonAnimation,
        "scale": ScaleButtonAnimation
    }

    def __init__(self, animation="scale", *args, **kwargs):
        # Default button
        if len(args) < 1 and not kwargs.get("image"):
            image = pygame.Surface([100, 100])
            image.fill((255, 255, 255))
            kwargs["image"] = image
        super().__init__(*args, **kwargs)
        self.on_click = None
        self.hovered = False
        self.animation = self.ANIMATIONS[animation](self)

    def is_click(self, click_pos):
        return self.rect.collidepoint(click_pos)

    def check_collide(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def click(self):
        if self.on_click:
            self.on_click()
        else:
            raise NotImplementedError("Function: <on_click> not implemented!!")

    def update(self, mouse_pos, clicked):
        current_time = time.time()
        if self.check_collide(mouse_pos):
            self.hovered = True
            if clicked:
                self.click()
        if self.hovered:
            self.animation.play(current_time)
        else:
            self.animation.stop()
        self.animation.update(current_time)
