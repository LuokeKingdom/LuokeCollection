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
            "save": Button(
                x=1100, y=700, on_click=lambda: model.save_rect(self.ratio, *self.rect)
            ),
            "previous_pet": Button(
                x=1030, y=300, on_click=lambda: model.previous_pet()
            ),
            "next_pet": Button(x=1170, y=300, on_click=lambda: model.next_pet()),
        }
        self.OTHERS = {
            "image": Container(
                image=EMPTY,
                align_mode="TOPLEFT",
            )
        }
        self.rect_side = 200
        self.rate = 1
        self.shrink_rate = False
        self.rect = None

    def set_pet_image(self, image):
        w, h = image.get_size()
        self.ratio = h / int(HEIGHT * 0.9)
        self.OTHERS["image"].set_image(image, height=int(HEIGHT * 0.9))

    def side_effect(self):
        super().side_effect()
        self.model.set_pet_select_rect(1)

    def display(self, mouse_pos, clicked):
        super().display(mouse_pos, clicked)
        pygame.draw.rect(
            self.screen,
            (0, 0, 0),
            pygame.Rect(
                mouse_pos.x - self.rect_side // 2,
                mouse_pos.y - self.rect_side // 2,
                self.rect_side,
                self.rect_side,
            ),
            2,
        )
        if self.rect is not None:
            pygame.draw.rect(
                self.screen,
                (100, 200, 100),
                pygame.Rect(*self.rect),
                2,
            )

    def update(self, mouse_pos, clicked):
        super().update(mouse_pos, clicked)
        if clicked == 5:
            self.rect_side = max(50, self.rect_side - self.rate)
            self.rate += 1
            self.shrink_rate = 1
        if clicked == 4:
            self.rect_side = min(500, self.rect_side + self.rate)
            self.rate += 1
            self.shrink_rate = 1
        self.rate = 1 if not self.shrink_rate else self.rate
        self.shrink_rate = (self.shrink_rate + 1) % 60
        if clicked == 1 and mouse_pos.x < 900:
            self.rect = [
                mouse_pos.x - self.rect_side // 2,
                mouse_pos.y - self.rect_side // 2,
                self.rect_side,
                self.rect_side,
            ]
        if clicked == 1 and mouse_pos.x > 900:
            self.rect = None
