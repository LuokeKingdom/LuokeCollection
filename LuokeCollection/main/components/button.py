import pygame
from pygame.locals import *  # noqa

from ..animation.button.button_animations import (
    CustomButtonAnimation,
    OpacityButtonAnimation,
    ScaleButtonAnimation,
    JumpButtonAnimation,
    RotateButtonAnimation,
    FrameButtonAnimation,
)
from .container import Container
from .text import Text
from ...settings.dev import SOUND
from ..model.sound import Channel
import time


class Button(Container):
    ANIMATIONS = {
        "opacity": OpacityButtonAnimation,
        "scale": ScaleButtonAnimation,
        "rotate": RotateButtonAnimation,
        "jump": JumpButtonAnimation,
        "frame": FrameButtonAnimation,
        "custom": CustomButtonAnimation,
        "none": lambda *args, **kwargs: None,
    }

    def __init__(
        self,
        animation="scale",
        transition=0.2,
        parameter={"factor": 1.2},
        on_click=None,
        can_hover=None,
        text=None,
        text_fontsize=24,
        text_color=(0, 0, 0),
        color=(150, 200, 100),
        sound=SOUND("mouse-click.wav", Channel.UI),
        *args,
        **kwargs
    ):
        self.text = text
        self.text_color = text_color
        self.text_fontsize = text_fontsize
        self.color = color
        self.sound = sound
        # default button
        if len(args) < 1 and not kwargs.get("image"):
            image = pygame.Surface([100, 100])
            image.fill(self.color)
            if text is None:
                self.text = "button"
            temp = Text.get_font(self.text_fontsize).render(
                self.text, True, self.text_color
            )
            rect = temp.get_rect(center=(50, 50))
            image.blit(temp, rect)
            kwargs["image"] = image
        super().__init__(*args, **kwargs)
        self.on_click = on_click
        self.can_hover = can_hover
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
            self.sound.play()
            self.on_click()
        else:
            raise NotImplementedError("Function: <on_click> not implemented!!")

    def update(self, mouse_pos, clicked, pressed):
        if not super(Button, self).update(mouse_pos, clicked, pressed): return
        current_time = time.time()
        if self.check_collide(mouse_pos):
            self.hovered = True
            if clicked:
                self.click()
        if self.animation is None:
            return
        if self.can_hover is not None and not self.can_hover():
            self.animation.stop()
            return
        if self.hovered:
            self.animation.play(current_time)
        else:
            self.animation.stop()
        self.animation.update(current_time)

