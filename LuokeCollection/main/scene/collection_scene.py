import os
import pygame
from pygame.locals import *
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
        new_buttons = {}
        new_others = {}
        info_compoments = {
            "pet_name": Text("", x=750, y=130),
            "pet_image": Sprite(EMPTY, ratio=0.2, x=900, y=330),
            "pet_element": Sprite(EMPTY, x=700, y=130),
            "pet_id": Text("1"),
            "pet_description": Text("Description.....", x=700, y=200),
            "talent_icon_AD": Sprite(
                IMAGE("place_holder.png"), ratio=0.8, x=700, y=500
            ),
            "talent_icon_AP": Sprite(
                IMAGE("place_holder.png"), ratio=0.8, x=700, y=570
            ),
            "talent_icon_DF": Sprite(
                IMAGE("place_holder.png"), ratio=0.8, x=700, y=640
            ),
            "talent_icon_MF": Sprite(
                IMAGE("place_holder.png"), ratio=0.8, x=900, y=500
            ),
            "talent_icon_HP": Sprite(
                IMAGE("place_holder.png"), ratio=0.8, x=900, y=570
            ),
            "talent_icon_SP": Sprite(
                IMAGE("place_holder.png"), ratio=0.8, x=900, y=640
            ),
            "pet_talent_AD": Text("40", x=730, y=490),
            "pet_talent_AP": Text("40", x=730, y=560),
            "pet_talent_DF": Text("40", x=730, y=630),
            "pet_talent_MF": Text("40", x=930, y=490),
            "pet_talent_HP": Text("40", x=930, y=560),
            "pet_talent_SP": Text("40", x=930, y=630),
        }
        for name, comp in info_compoments.items():
            (new_buttons if comp is Button else new_others)[name] = comp
        for name, comp in new_buttons.items():
            self.BUTTONS[name] = comp
        for name, comp in new_others.items():
            self.OTHERS[name] = comp

    def init_page(self):
        index = 0
        new_others = {}
        new_buttons = {}
        for i in range(3):
            for j in range(3):
                new_buttons[f"slot_{index+1}"] = Button(
                    'none',EMPTY, x=202 + j * 163, y=290 + i * 146, align_mode="CENTER", width=100
                )
                new_others[f"slot_{index+1}"] = Text(
                    "", x=202 + j * 163, y=316 + i * 146, align_mode="CENTER", size=24
                )
                index += 1
        for name, comp in new_others.items():
            self.OTHERS[name] = comp

    def set_page(self, pet_page):
        index = 0
        for pet_info in pet_page:
            pet_image = IMAGE(os.path.join('LuokeCollection/assets/data/',pet_info.path,'display.png'), False)
            self.BUTTONS[f"slot_{index+1}"].set_image(pet_image, width=100)
            self.OTHERS[f"slot_{index+1}"].change_text(pet_info.name)
            index += 1
        for i in range(index, 9):
            self.OTHERS[f"slot_{i+1}"].change_text("")
