import pygame
from pygame.locals import *  # noqa

from .scene import Scene
from ..components.button import Button
from LuokeCollection.settings.dev import IMAGE


class PetPositionSelectScene(Scene):
    def __init__(self, screen, model, *args, **kwargs):
        kwargs["bg"] = pygame.Surface([1, 1])
        kwargs["bg"].fill((255, 255, 255))
        kwargs["width"] = 800
        kwargs["height"] = 200
        super(PetPositionSelectScene, self).__init__(screen, model, *args, **kwargs)
        self.BUTTONS = {
            "pop": Button(text="X", x=1000, y=100, on_click=lambda: self.model.close_pop_up())
        }