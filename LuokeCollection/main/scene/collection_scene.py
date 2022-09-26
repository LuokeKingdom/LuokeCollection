import os
import pygame
from pygame.locals import *  # noqa
from ..model.sound import Channel

from LuokeCollection.main.components.container import Container
from .scene import Scene
from ..components.button import Button
from ..components.text import Text
from ..components.sprite import Sprite
from LuokeCollection.settings.dev import SOUND, IMAGE
from ..utils import ELEMENT_MAP

EMPTY = pygame.Surface([1, 1], pygame.SRCALPHA)


class CollectionScene(Scene):
    def __init__(self, screen, model, *args, **kwargs):
        kwargs["bg"] = IMAGE("temp_bg.png")
        super(CollectionScene, self).__init__(screen, model, *args, **kwargs)
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
        self.init_page()

    def side_effect(self):
        super().side_effect()
        self.model.set_page()

    def init_info(self):
        info_compoments = {
            "pet_name": Text("", x=760, y=100, size=32),
            "pet_image": Sprite(EMPTY),
            "pet_element": Sprite(EMPTY),
            "pet_secondary_element": Sprite(EMPTY),
            "pet_id": Text(
                text="", size=150, x=780, y=60, color=(200, 150, 100), opacity=100
            ),
            "pet_description": Text("", x=750, y=160, size=20),
            "pet_weight": Text("", x=980, y=131, size=24),
            "pet_height": Text("", x=980, y=156, size=24),
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
            "page_number": Text(
                "", x=367, y=650, size=26, align_mode="CENTER", color=(231, 225, 146)
            ),
            "train": Button(
                text="train", x=900, y=700, on_click=lambda: self.model.open("training")
            ),
            "edit_avatar": Button(
                text="edit",
                x=750,
                y=700,
                on_click=lambda: self.model.open("select_rect"),
            ),
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
        max_width, max_height = 380, 320
        w, h = pet_image.get_size()
        if h / max_height < w / max_width:
            self.OTHERS["pet_image"].set_image(
                image=pet_image, width=max_width
            ).set_pos(830, 420)

        else:
            self.OTHERS["pet_image"].set_image(
                image=pet_image, height=max_height
            ).set_pos(830, 420)
        self.OTHERS["pet_element"].set_image(
            image=ELEMENT_MAP.get(pet.element).image, width=100
        ).set_pos(690, 110)
        if pet.secondary_element is not None:
            self.OTHERS["pet_secondary_element"].set_image(
                image=ELEMENT_MAP.get(pet.secondary_element).image, width=50
            ).set_pos(736, 124)
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
        self.TEXTS["pet_id"].change_text(str(pet.number))
        self.TEXTS["pet_description"].change_text(pet.desc)
        self.TEXTS["pet_talent_HP"].change_text(pet.stats[0])
        self.TEXTS["pet_talent_AD"].change_text(pet.stats[1])
        self.TEXTS["pet_talent_DF"].change_text(pet.stats[2])
        self.TEXTS["pet_talent_AP"].change_text(pet.stats[3])
        self.TEXTS["pet_talent_MD"].change_text(pet.stats[4])
        self.TEXTS["pet_talent_SP"].change_text(pet.stats[5])
        self.TEXTS["pet_weight"].change_text("体重：" + pet.weight)
        self.TEXTS["pet_height"].change_text("身高：" + pet.height)

    def init_page(self):
        index = 0
        new_texts = {}
        new_others = {}
        new_buttons = {}
        new_on_clicks = {}
        for i in range(3):
            for j in range(3):
                offset = int(str(i * 3 + j + 1))
                new_on_clicks[f"slot_{index+1}"] = offset
                new_buttons[f"slot_{index+1}"] = Button(
                    animation="none",
                    image=EMPTY,
                    x=205 + j * 161,
                    y=257 + i * 146,
                    align_mode="CENTER",
                    width=100,
                )
                new_others[f"slot_{index+1}"] = Container(
                    image=IMAGE("tag2.png"),
                    x=210 + j * 161,
                    y=313 + i * 146,
                    align_mode="CENTER",
                )
                new_texts[f"slot_{index+1}"] = Text(
                    text="",
                    x=202 + j * 163,
                    y=316 + i * 146,
                    align_mode="CENTER",
                    size=24,
                )
                index += 1
        for name, comp in new_texts.items():
            self.TEXTS[name] = comp
        for name, comp in new_buttons.items():
            self.BUTTONS[name] = comp
        for name, comp in new_others.items():
            self.OTHERS[name] = comp
        self.BUTTONS["slot_1"].on_click = lambda: self.model.set_info(1)
        self.BUTTONS["slot_2"].on_click = lambda: self.model.set_info(2)
        self.BUTTONS["slot_3"].on_click = lambda: self.model.set_info(3)
        self.BUTTONS["slot_4"].on_click = lambda: self.model.set_info(4)
        self.BUTTONS["slot_5"].on_click = lambda: self.model.set_info(5)
        self.BUTTONS["slot_6"].on_click = lambda: self.model.set_info(6)
        self.BUTTONS["slot_7"].on_click = lambda: self.model.set_info(7)
        self.BUTTONS["slot_8"].on_click = lambda: self.model.set_info(8)
        self.BUTTONS["slot_9"].on_click = lambda: self.model.set_info(9)

    def set_page(self, pet_page):
        index = 0
        for pet_info in pet_page:
            self.TEXTS[f"slot_{index+1}"].change_text(pet_info.name)
            index += 1
        for i in range(index, 9):
            self.TEXTS[f"slot_{i+1}"].change_text("")
            self.BUTTONS[f"slot_{i+1}"].image = EMPTY
        self.TEXTS["page_number"].change_text(str(self.model.pet_page_number))

    def update(self, mouse_pos, clicked):
        super().update(mouse_pos, clicked)
        for index in range(9):
            pet_number = (self.model.pet_page_number - 1) * 9 + index + 1
            pet_image = self.model.pet_rects.get(pet_number)
            self.BUTTONS[f"slot_{index+1}"].image = pet_image or EMPTY
