import pygame
from pygame.locals import *  # noqa

from ..model.sound import Channel
from .scene import Scene
from ..components.button import Button
from ..components.container import Container
from ..components.text import Text
from LuokeCollection.settings.dev import SOUND, HEIGHT

EMPTY = pygame.Surface([1, 1], pygame.SRCALPHA)


class SelectRectScene(Scene):
    def __init__(self, screen, model, *args, **kwargs):
        super(SelectRectScene, self).__init__(
            screen, model, "light_blue.png", *args, **kwargs
        )
        self.background_music = SOUND("sky_gym.wav", Channel.BACKGROUND)
        self.BUTTONS["close"] = Button(
            x=1100, y=70, on_click=lambda: model.close(), text="X", text_fontsize=80
        )
        self.BUTTONS["save"] = Button(
            x=1100,
            y=700,
            on_click=lambda: self.save_rect(),
            text="保存",
        )
        self.OTHERS["image"] = Container(image=EMPTY, align_mode="TOPLEFT")

        self.TEXTS["warning"] = Text(x=1100, y=600, align_mode="CENTER", text="")
        self.rect_side = 200
        self.rate = 1
        self.shrink_rate = False
        self.rect = None

    def side_effect(self):
        super().side_effect()
        self.model.set_pet_select_rect()
        self.rect = None

    def set_pet_image(self, image):
        w, h = image.get_size()
        self.ratio = h / int(HEIGHT * 0.9)
        self.OTHERS["image"].set_image(image, height=int(HEIGHT * 0.9))
        (
            self.image_rect_x,
            self.image_rect_y,
            self.image_rect_w,
            self.image_rect_h,
        ) = self.OTHERS["image"].image.get_rect()

    def display(self, mouse_pos, clicked):
        super().display(mouse_pos, clicked)

        if mouse_pos.x < self.rect_side // 2:
            if mouse_pos.y < self.rect_side // 2:  # when mouse_pos is at top left
                self.rect_x = 0
                self.rect_y = 0
            elif (
                mouse_pos.y > self.image_rect_h - self.rect_side // 2
            ):  # when mouse_pos is at bottom left
                self.rect_x = 0
                self.rect_y = self.image_rect_h - self.rect_side
            else:  # when mouse_pos is along left edge
                self.rect_x = 0
                self.rect_y = mouse_pos.y - self.rect_side // 2
        elif mouse_pos.x > self.image_rect_w - self.rect_side // 2:
            if mouse_pos.y < self.rect_side // 2:  # when mouse_pos is at top right
                self.rect_x = self.image_rect_w - self.rect_side
                self.rect_y = 0
            elif (
                mouse_pos.y > self.image_rect_h - self.rect_side // 2
            ):  # when mouse_pos is at bottom right
                self.rect_x = self.image_rect_w - self.rect_side
                self.rect_y = self.image_rect_h - self.rect_side
            else:  # when mouse_pos is along right edge
                self.rect_x = self.image_rect_w - self.rect_side
                self.rect_y = mouse_pos.y - self.rect_side // 2
        elif mouse_pos.y < self.rect_side // 2:  # when mouse_pos is along top edge
            self.rect_x = mouse_pos.x - self.rect_side // 2
            self.rect_y = 0
        elif (
            mouse_pos.y > self.image_rect_h - self.rect_side // 2
        ):  # when mouse_pos is along bottom edge
            self.rect_x = mouse_pos.x - self.rect_side // 2
            self.rect_y = self.image_rect_h - self.rect_side
        else:  # when mouse_pos is not touching any edge
            self.rect_x = mouse_pos.x - self.rect_side // 2
            self.rect_y = mouse_pos.y - self.rect_side // 2

        pygame.draw.rect(
            self.screen,
            (0, 0, 0),
            pygame.Rect(
                self.rect_x,
                self.rect_y,
                self.rect_side,
                self.rect_side,
            ),
            2,
        )

        if self.rect is not None:
            pygame.draw.rect(
                self.screen,
                (100, 200, 100),
                pygame.Rect(*list(map(lambda x: x // self.ratio, self.rect))),
                2,
            )

    def update(self, delta_time, mouse_pos, clicked, pressed):
        super().update(delta_time, mouse_pos, clicked, pressed)
        if clicked == 5:
            self.rect_side = max(50, self.rect_side - self.rate)
            self.rate += 1
            self.shrink_rate = 1
        if clicked == 4:
            self.rect_side = min(
                self.image_rect_h, self.image_rect_w, self.rect_side + self.rate
            )
            self.rate += 1
            self.shrink_rate = 1
        self.rate = 1 if not self.shrink_rate else self.rate
        self.shrink_rate = (self.shrink_rate + 1) % 60
        if clicked == 1 and mouse_pos.x < 900:
            self.rect = list(
                map(
                    lambda x: int(x * self.ratio),
                    [self.rect_x, self.rect_y, self.rect_side, self.rect_side],
                )
            )

    def save_rect(self):
        if self.rect is not None:
            self.model.save_rect(*self.rect)
            self.model.saved_sound.play()
            self.TEXTS["warning"].color = (100, 200, 100)
            self.TEXTS["warning"].change_text("已保存！")
        else:
            self.model.error_sound.play()
            self.TEXTS["warning"].color = (240, 50, 50)
            self.TEXTS["warning"].change_text("未保存! 請先選擇新頭像")
