import pygame
from pygame.locals import *
from .scene import Scene
from ..components.button import Button
from ..components.container import Container
from ..components.text import Text
from settings.dev import WIDTH, HEIGHT, IMAGE

EMPTY = pygame.Surface([1, 1])


class SelectRectScene(Scene):
    def __init__(self, screen, model, *args, **kwargs):
        kwargs["bg"] = pygame.Surface([1, 1])
        kwargs["bg"].fill((200, 200, 245))
        super(SelectRectScene, self).__init__(screen, model, *args, **kwargs)
        self.BUTTONS = {
            "close": Button(x=1100, y=70, on_click=lambda: model.close()),
            "save": Button(x=1100, y=700),
        }
        self.OTHERS = {
            "image": Container(
                image=EMPTY,
                align_mode="TOPLEFT",
            )
        }

    def set_pet_image(self, image):
        self.OTHERS["image"].set_image(image, height=int(HEIGHT * 0.9))

    def side_effect(self):
        super().side_effect()
        self.model.set_pet_select_rect(1)

    def display(self, mouse_pos, clicked):
        super().display(mouse_pos, clicked)
        pygame.draw.rect(
            self.screen, (0, 0, 0), pygame.Rect(mouse_pos.x, mouse_pos.y, 200, 200), 2
        )

    def update(self, mouse_pos, clicked):
        super().update(mouse_pos, clicked)
