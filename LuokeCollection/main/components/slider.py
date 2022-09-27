import pygame
from pygame.locals import *  # noqa

from LuokeCollection.main.components.button import Button


class Slider(Button):
    def __init__(self, *args, **kwargs):
        kwargs["image"] = pygame.Surface([30, 30])
        kwargs["image"].fill((0, 0, 0))
        super().__init__(*args, **kwargs)
        self.dragged = False

    def update(self, mouse_pos, clicked, pressed):
        super().update(mouse_pos, clicked, pressed)
        if self.dragged:
            self.dragged = pressed
        else:
            self.dragged = pressed and self.check_collide(mouse_pos)

        if self.dragged:
            self.set_pos(mouse_pos)
