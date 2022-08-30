import os
import pygame
from pygame.locals import *
from ..model.sound import Channel

from LuokeCollection.main.components.container import Container
from .scene import Scene
from ..components.button import Button
from ..components.text import Text
from ..components.sprite import Sprite
from LuokeCollection.settings.dev import SOUND, WIDTH, HEIGHT, IMAGE
from ..utils import ELEMENT_MAP

EMPTY = pygame.Surface([1, 1], pygame.SRCALPHA)


class TrainingScene(Scene):
    def __init__(self, screen, model, *args, **kwargs):
        kwargs["bg"] = IMAGE("temp_bg.png")
        super(TrainingScene, self).__init__(screen, model, *args, **kwargs)
        self.background_music = SOUND("peter_ave.wav", Channel.BACKGROUND)
        self.BUTTONS = {
            "close": Button(
                image=IMAGE("close.png"),
                x=1100,
                y=70,
                on_click=lambda: model.close(),
                animation="opacity",
                parameter={"factor": 0.2},
                width=120,
            ),
            "next_page": Button(
                image=pygame.transform.flip(IMAGE("previous.png"), True, False),
                x=421,
                y=649,
                on_click=lambda: model.next_page(),
                animation="opacity",
                parameter={"factor": 0.2},
                width=48,
            ),
            "previous_page": Button(
                image=IMAGE("previous.png"),
                x=308,
                y=649,
                on_click=lambda: model.previous_page(),
                animation="opacity",
                parameter={"factor": 0.2},
                width=48,
            ),
        }
        self.init_info()

    def side_effect(self):
        super().side_effect()
        self.model.set_info()

    def init_info(self):
        info_compoments = {
            "pet_name": Text("", x=260, y=100, size=32),
            "pet_image": Sprite(EMPTY),
            "pet_element": Sprite(EMPTY),
            "pet_secondary_element": Sprite(EMPTY),
            "talent_icon_HP": Sprite(EMPTY, width=36),
            "talent_icon_AD": Sprite(EMPTY, width=36),
            "talent_icon_DF": Sprite(EMPTY, width=36),
            "talent_icon_SP": Sprite(EMPTY, width=36),
            "talent_icon_AP": Sprite(EMPTY, width=36),
            "talent_icon_MD": Sprite(EMPTY, width=36),
            "pet_talent_HP": Text("", x=1070, y=286, size=26),
            "pet_talent_AD": Text("", x=1070, y=326, size=26),
            "pet_talent_DF": Text("", x=1070, y=366, size=26),
            "pet_talent_SP": Text("", x=1070, y=406, size=26),
            "pet_talent_AP": Text("", x=1070, y=446, size=26),
            "pet_talent_MD": Text("", x=1070, y=486, size=26),
        }
        for name, comp in info_compoments.items():
            if isinstance(comp, Button):
                self.BUTTONS[name] = comp
            elif isinstance(comp, Text):
                self.TEXTS[name] = comp
            else:
                self.OTHERS[name] = comp

    def set_info(self, pet):
        self.TEXTS["pet_name"].change_text(pet.name)
        pet_image = IMAGE(os.path.join("assets/data/", pet.path, "display.png"), False)
        max_width, max_height = 460, 700
        w, h = pet_image.get_size()
        if h / max_height < w / max_width:
            self.OTHERS["pet_image"].set_image(
                image=pet_image, width=max_width
            ).set_pos(360, 360)
        else:
            self.OTHERS["pet_image"].set_image(
                image=pet_image, height=max_height
            ).set_pos(360, 360)
        self.OTHERS["pet_image"].image.set_alpha(100)
        self.OTHERS["pet_element"].set_image(
            image=ELEMENT_MAP.get(pet.element).image, width=100
        ).set_pos(190, 110)
        if pet.secondary_element is not None:
            self.OTHERS["pet_secondary_element"].set_image(
                image=ELEMENT_MAP.get(pet.secondary_element).image, width=50
            ).set_pos(236, 124)
        else:
            self.OTHERS["pet_secondary_element"].set_image(EMPTY)

        self.OTHERS["talent_icon_HP"].set_image(
            image=IMAGE("HP.png"), width=36
        ).set_pos(1040, 300)
        self.OTHERS["talent_icon_AD"].set_image(
            image=IMAGE("AD.png"), width=36
        ).set_pos(1040, 340)
        self.OTHERS["talent_icon_DF"].set_image(
            image=IMAGE("DF.png"), width=36
        ).set_pos(1040, 380)
        self.OTHERS["talent_icon_SP"].set_image(
            image=IMAGE("SP.png"), width=36
        ).set_pos(1040, 420)
        self.OTHERS["talent_icon_AP"].set_image(
            image=IMAGE("AP.png"), width=36
        ).set_pos(1040, 460)
        self.OTHERS["talent_icon_MD"].set_image(
            image=IMAGE("MD.png"), width=36
        ).set_pos(1040, 500)
        color = tuple(map(lambda x: max(0, x - 40), ELEMENT_MAP.get(pet.element).color))
        self.TEXTS["pet_talent_HP"].color = color
        self.TEXTS["pet_talent_AD"].color = color
        self.TEXTS["pet_talent_DF"].color = color
        self.TEXTS["pet_talent_AP"].color = color
        self.TEXTS["pet_talent_MD"].color = color
        self.TEXTS["pet_talent_SP"].color = color
        self.TEXTS["pet_talent_HP"].change_text(pet.stats[0])
        self.TEXTS["pet_talent_AD"].change_text(pet.stats[1])
        self.TEXTS["pet_talent_DF"].change_text(pet.stats[2])
        self.TEXTS["pet_talent_AP"].change_text(pet.stats[3])
        self.TEXTS["pet_talent_MD"].change_text(pet.stats[4])
        self.TEXTS["pet_talent_SP"].change_text(pet.stats[5])

    def update(self, mouse_pos, clicked):
        super().update(mouse_pos, clicked)
