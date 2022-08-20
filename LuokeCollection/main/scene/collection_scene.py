import os
import pygame
from pygame.locals import *

from LuokeCollection.main.components.container import Container
from .scene import Scene
from ..components.button import Button
from ..components.text import Text
from ..components.sprite import Sprite
from settings.dev import WIDTH, HEIGHT, IMAGE

EMPTY = pygame.Surface([1, 1])


class CollectionScene(Scene):
    def __init__(self, screen, model, *args, **kwargs):
        kwargs["bg"] = IMAGE("temp_bg.png")
        super(CollectionScene, self).__init__(screen, model, *args, **kwargs)
        self.BUTTONS = {
            "close": Button(x=1100, y=70, on_click=lambda: model.close()),
            "next_page": Button(x=420, y=730, on_click=lambda: model.next_page()),
            "previous_page": Button(
                x=300, y=730, on_click=lambda: model.previous_page()
            ),
        }
        self.init_info()
        self.init_page()

    def side_effect(self):
        super().side_effect()
        self.model.set_page(1)

    def init_info(self):
        info_compoments = {
            "pet_name": Text("", x=750, y=130),
            "pet_image": Sprite(EMPTY, ratio=0.2, x=900, y=330),
            "pet_element": Sprite(EMPTY, x=700, y=130),
            "pet_id": Text("1"),
            "pet_description": Text("Description.....", x=700, y=200),
            "talent_icon_HP": Sprite(
                IMAGE("place_holder.png"), ratio=0.8, x=700, y=500
            ),
            "talent_icon_AD": Sprite(
                IMAGE("place_holder.png"), ratio=0.8, x=700, y=570
            ),
            "talent_icon_DF": Sprite(
                IMAGE("place_holder.png"), ratio=0.8, x=700, y=640
            ),
            "talent_icon_SP": Sprite(
                IMAGE("place_holder.png"), ratio=0.8, x=900, y=500
            ),
            "talent_icon_AP": Sprite(
                IMAGE("place_holder.png"), ratio=0.8, x=900, y=570
            ),
            "talent_icon_MD": Sprite(
                IMAGE("place_holder.png"), ratio=0.8, x=900, y=640
            ),
            "pet_talent_HP": Text("40", x=730, y=490),
            "pet_talent_AD": Text("40", x=730, y=560),
            "pet_talent_DF": Text("40", x=730, y=630),
            "pet_talent_SP": Text("40", x=930, y=490),
            "pet_talent_AP": Text("40", x=930, y=560),
            "pet_talent_MD": Text("40", x=930, y=630),
        }
        for name, comp in info_compoments.items():
            if isinstance(comp, Button): self.BUTTONS[name] = comp
            elif isinstance(comp, Text): self.TEXTS[name] = comp
            else: self.OTHERS[name] = comp

    def set_info(self, pet):
        print(self.OTHERS)
        self.TEXTS["pet_name"].change_text(pet.name)
        self.OTHERS["pet_image"]
        self.OTHERS["pet_element"]
        self.TEXTS["pet_id"].change_text(str(pet.number))
        self.TEXTS["pet_description"].change_text(pet.desc)
        self.OTHERS["talent_icon_HP"]
        self.OTHERS["talent_icon_AD"]
        self.OTHERS["talent_icon_DF"]
        self.OTHERS["talent_icon_AP"]
        self.OTHERS["talent_icon_MF"]
        self.OTHERS["talent_icon_SP"]
        self.TEXTS["pet_talent_HP"].change_text(pet.stats[0])
        self.TEXTS["pet_talent_AD"].change_text(pet.stats[1])
        self.TEXTS["pet_talent_DF"].change_text(pet.stats[2])
        self.TEXTS["pet_talent_AP"].change_text(pet.stats[3])
        self.TEXTS["pet_talent_MF"].change_text(pet.stats[4])
        self.TEXTS["pet_talent_SP"].change_text(pet.stats[5])

    def init_page(self):
        index = 0
        new_texts = {}
        new_others = {}
        new_buttons = {}
        new_on_clicks = {}
        for i in range(3):
            for j in range(3):
                offset = int(str(i*3+j+1))
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
                    image=IMAGE('tag.png'),
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
            pet_image = IMAGE(
                os.path.join(
                    "LuokeCollection/assets/data/", pet_info.path, "display.png"
                ),
                False,
            )
            rect = self.model.DATA["pet_rects"].get(pet_info.number)
            if rect:
                canvas = pygame.Surface([rect[2],rect[2]], pygame.SRCALPHA)
                canvas.blit(pet_image.subsurface(*rect), (0,0))
                pet_image = pygame.transform.smoothscale(
                    canvas, (100,100)
                )
            self.BUTTONS[f"slot_{index+1}"].image = pet_image if rect else EMPTY
            self.TEXTS[f"slot_{index+1}"].change_text(pet_info.name)
            index += 1
        for i in range(index, 9):
            self.TEXTS[f"slot_{i+1}"].change_text("")
