from pydoc import ModuleScanner
import pygame
from pygame.locals import *

from ..model.sound import Channel
from .scene import Scene
from ..components.button import Button
from ..components.container import Container
from ..components.text import Text
from LuokeCollection.settings.dev import SOUND, WIDTH, HEIGHT, IMAGE



class SplashScene(Scene):
    def __init__(self, screen, model, *args, **kwargs):
        kwargs["bg"] = pygame.Surface([1, 1])
        kwargs["bg"].fill((255, 255, 255))
        super(SplashScene, self).__init__(screen, model, *args, **kwargs)
        self.BUTTONS = {}
        self.OTHERS = {
            "icon": Container(
                image=IMAGE("icon.png"),
                align_mode="CENTER",
                x=self.screen.get_width() // 2,
                y=self.screen.get_height() // 2 - 100,
                ratio=0.7
            ),
            "subtitle": Container(
                image=IMAGE("collection_button.png"),
                align_mode="CENTER",
                x=self.screen.get_width() // 2,
                y=self.screen.get_height() // 2 + 60,
            ),
        }
        self.TEXTS = {}

    def display(self, mouse_pos, clicked):
        super().display(mouse_pos, clicked)

    def update(self, mouse_pos, clicked):
        super().update(mouse_pos, clicked)