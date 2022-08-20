import pygame
from pygame.locals import *

from ..animation.button.button_animations import (
    JumpButtonAnimation,
    OpacityButtonAnimation,
    ScaleButtonAnimation,
    JumpButtonAnimation,
    RotateButtonAnimation,
    FrameButtonAnimation,
)
from ..utils import vec
from .container import Container

import time


class Button(Container):
    ANIMATIONS = {
        "opacity": OpacityButtonAnimation,
        "scale": ScaleButtonAnimation,
        "rotate": RotateButtonAnimation,
        "jump": JumpButtonAnimation,
        "frame": FrameButtonAnimation,
        "none": lambda *args, **kwargs:None,
    }

    def __init__(
        self,
        animation="scale",
        transition=0.2,
        parameter=1.2,
        on_click=None,
        *args,
        **kwargs
    ):
        # default button
        if len(args) < 1 and not kwargs.get("image"):
            image = pygame.Surface([100, 100])
            image.fill((255, 255, 255))
            kwargs["image"] = image
        super().__init__(*args, **kwargs)
        self.on_click = on_click
        self.hovered = False
        self.transition = transition
        self.parameter = parameter
        self.animation = self.ANIMATIONS[animation](self, transition, parameter)

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
        if self.animation is None:
            return
        if self.hovered:
            self.animation.play(current_time)
        else:
            self.animation.stop()
        self.animation.update(current_time)
