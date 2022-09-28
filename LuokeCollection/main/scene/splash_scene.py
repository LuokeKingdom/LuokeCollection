import pygame
from pygame.locals import *  # noqa

from .scene import Scene
from ..components.container import Container
from LuokeCollection.settings.dev import IMAGE


class SplashScene(Scene):
    def __init__(self, screen, model, *args, **kwargs):
        kwargs["bg"] = pygame.Surface([1, 1])
        kwargs["bg"].fill((255, 255, 255))
        super(SplashScene, self).__init__(screen, model, *args, **kwargs)
        self.progress = 0
        self.frame = 0
        bar = pygame.Surface([1, 1])
        bar.fill((100, 225, 100))

        self.BUTTONS = {}

        self.OTHERS = {
            "progress_pet": Container(
                image=pygame.Surface([1, 1]),
                x=100,
                y=self.screen.get_height() - 300,
                ratio=0.8,
                align_mode="TOPLEFT",
            ),
            "icon": Container(
                image=IMAGE("icon.png"),
                align_mode="CENTER",
                x=self.screen.get_width() // 2,
                y=self.screen.get_height() // 2 - 100,
                ratio=0.7,
            ),
            "subtitle": Container(
                image=IMAGE("collection_button.png"),
                align_mode="CENTER",
                x=self.screen.get_width() // 2,
                y=self.screen.get_height() // 2 + 60,
            ),
            "progress_bar": Container(
                image=bar,
                align_mode="TOPLEFT",
                x=0,
                y=self.screen.get_height() - 50,
            ),
        }
        self.TEXTS = {}

    def display(self, mouse_pos, clicked):
        super().display(mouse_pos, clicked)
        self.OTHERS["progress_pet"].image = IMAGE(
            "progress_pet/" + str(self.frame + 1) + ".png"
        )
        self.frame = (self.frame + 1) % 40
        self.OTHERS["progress_pet"].set_pos(
            self.progress * self.screen.get_width(), self.screen.get_height() - 300
        )
        self.OTHERS["progress_bar"].set_image(
            self.OTHERS["progress_bar"].original_image,
            height=100,
            width=int(self.progress * self.screen.get_width()),
        ).set_pos(x=0, y=self.screen.get_height() - 50)

    def update(self, mouse_pos, clicked, pressed):
        super().update(mouse_pos, clicked, pressed)
        self.progress = len(self.model.pet_rects) / len(self.model.PETS)
        if self.progress >= 0.99:
            self.model.close_pop_up()
