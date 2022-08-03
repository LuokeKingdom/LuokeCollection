import pygame
from pygame.locals import *

from ..animation.button.button_animations import (
    JumpButtonAnimation,
    OpacityButtonAnimation,
    ScaleButtonAnimation,
    JumpButtonAnimation,
)
from ..utils import vec
from .container import Container

import time


class Button(Container):
    ANIMATIONS = {
        "opacity": OpacityButtonAnimation,
        "scale": ScaleButtonAnimation,
        "jump": JumpButtonAnimation,
    }

    def __init__(self, animation="jump", *args, **kwargs):
        # default button
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
        if self.check_collide_original_rect:
            return self.original_rect.collidepoint(mouse_pos)
        else:
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
