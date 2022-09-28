import pygame
from pygame.locals import *  # noqa

from LuokeCollection.main.components.button import Button


class Slider(Button):
    def __init__(self, on_change, interval=[0,31], *args, **kwargs):
        kwargs["image"] = pygame.Surface([30, 30])
        kwargs["image"].fill((0, 0, 0))
        super().__init__(*args, **kwargs)
        self.dragged = False
        self.origin = self.get_pos()
        self.on_change = on_change
        self.offset = 0
        self.interval = interval

    def update(self, mouse_pos, clicked, pressed):
        super().update(mouse_pos, clicked, pressed)
        if self.dragged:
            if not pressed:
                val = ((self.get_pos().x - self.origin.x) + 50) / 100 * (self.interval[1] - self.interval[0]) + self.interval[0]
                self.on_change(int(val))
            self.dragged = pressed
        else:
            self.dragged = pressed and self.check_collide(mouse_pos)
            self.offset = mouse_pos - self.get_pos()

        if self.dragged:
            x_pos = min(max(self.origin.x - 50, mouse_pos.x - self.offset.x), self.origin.x + 50)
            self.set_pos(x_pos, self.origin.y)
