import os
import pygame
from pygame.locals import *

from LuokeCollection.main.utils import ELEMENT_MAP  # noqa
from ..components.sprite import Sprite
from ..scene.scene import Scene
from ..components.button import Button
from ..components.text import Text
from ..model.sound import Channel
from LuokeCollection.settings.dev import SOUND, WIDTH, HEIGHT, IMAGE


EMPTY = pygame.Surface([1, 1], pygame.SRCALPHA)

class BattlePrepScene(Scene):
    def __init__(self, screen, model, *args, **kwargs):
        kwargs["bg"] = IMAGE("skill_temp.png")
        super(BattlePrepScene, self).__init__(screen, model, *args, **kwargs)
        self.background_music = SOUND("castle.wav", Channel.BACKGROUND)
        self.talent_map = {
            "level": 1,
            "HP": 0,
            "AD": 0,
            "DF": 0,
            "SP": 0,
            "AP": 0,
            "MD": 0,
        }
        self.stat_map = None
        self.BUTTONS = {
            "pop": Button(
                text="X",
                x=1100,
                y=100,
                on_click=lambda: model.close()
            ),
            "train": Button(
                image=IMAGE("battle.png"),
                x=1020,
                y=600,
                on_click=lambda: self.model.open("training"),
                width=100,
                animation="opacity",
                parameter={"factor": 0.4},
            ),
            "battle": Button(
                image=IMAGE("battle.png"),
                on_click=lambda: self.model.open("battle"),
                x=1100,
                y=600,
                width=100,
                animation="opacity",
                parameter={"factor": 0.4},
            )
        }
        self.init_pets()
        self.init_info()

    def side_effect(self):
        super().side_effect()
        self.model.set_battle_prep()

    
    def init_pets(self):
        def get_on_click(i):
            return lambda:self.model.set_battle_prep(i)
        for i in range(6):
            self.BUTTONS[f"pet_container_{i}"] = Button(
                animation="opacity", 
                image=IMAGE("place_holder.png"),
                width=100, 
                x=200+i*150, 
                y=100,
                on_click=get_on_click(i)
            )
            self.TEXTS[f"pet_name_{i}"] = Text("",x=200+i*150,y=100, align_mode="CENTER")
    
    def init_info(self):
        info_components = {
            "pet_name": Text("", x=260, y=200, size=32),
            "pet_image": Sprite(EMPTY),
            "pet_element": Sprite(EMPTY),
            "pet_secondary_element": Sprite(EMPTY),
            "talent_icon_HP": Sprite(EMPTY, width=36),
            "talent_icon_AD": Sprite(EMPTY, width=36),
            "talent_icon_DF": Sprite(EMPTY, width=36),
            "talent_icon_SP": Sprite(EMPTY, width=36),
            "talent_icon_AP": Sprite(EMPTY, width=36),
            "talent_icon_MD": Sprite(EMPTY, width=36),
            "pet_HP": Text("", x=220, y=286, size=26),
            "pet_AD": Text("", x=220, y=366, size=26),
            "pet_DF": Text("", x=220, y=446, size=26),
            "pet_SP": Text("", x=220, y=526, size=26),
            "pet_AP": Text("", x=220, y=606, size=26),
            "pet_MD": Text("", x=220, y=686, size=26),
        }

        for name, comp in info_components.items():
            if isinstance(comp, Button):
                self.BUTTONS[name] = comp
            elif isinstance(comp, Text):
                self.TEXTS[name] = comp
            else:
                self.OTHERS[name] = comp

    def set_pet_tabs(self, pets):
        for i, pet in enumerate(pets):
            self.pet_circle(i, pet["name"], pet["image"])
    
    def pet_circle(self, i, name, image=None):
        if image is None:
            image = IMAGE("place_holder.png")
        self.BUTTONS[f"pet_container_{i}"].set_image(image).set_pos(200+i*150,100)
        self.TEXTS[f"pet_name_{i}"].change_text(name)


    def set_info(self, pet):
        self.TEXTS["pet_name"].change_text(pet.name)
        pet_image = IMAGE(os.path.join("assets/data/", pet.path, "display.png"), False)
        max_width, max_height = 460, 700
        w, h = pet_image.get_size()
        if h / max_height < w / max_width:
            self.OTHERS["pet_image"].set_image(
                image=pet_image, width=max_width
            ).set_pos(360, 460)
        else:
            self.OTHERS["pet_image"].set_image(
                image=pet_image, height=max_height
            ).set_pos(360, 460)
        self.OTHERS["pet_image"].image.set_alpha(60)
        self.OTHERS["pet_element"].set_image(
            image=ELEMENT_MAP.get(pet.element).image, width=100
        ).set_pos(190, 210)
        if pet.secondary_element is not None:
            self.OTHERS["pet_secondary_element"].set_image(
                image=ELEMENT_MAP.get(pet.secondary_element).image, width=50
            ).set_pos(236, 224)
        else:
            self.OTHERS["pet_secondary_element"].set_image(EMPTY)

        self.OTHERS["talent_icon_HP"].set_image(
            image=IMAGE("HP.png"), width=36
        ).set_pos(190, 300)
        self.OTHERS["talent_icon_AD"].set_image(
            image=IMAGE("AD.png"), width=36
        ).set_pos(190, 380)
        self.OTHERS["talent_icon_DF"].set_image(
            image=IMAGE("DF.png"), width=36
        ).set_pos(190, 460)
        self.OTHERS["talent_icon_SP"].set_image(
            image=IMAGE("SP.png"), width=36
        ).set_pos(190, 540)
        self.OTHERS["talent_icon_AP"].set_image(
            image=IMAGE("AP.png"), width=36
        ).set_pos(190, 620)
        self.OTHERS["talent_icon_MD"].set_image(
            image=IMAGE("MD.png"), width=36
        ).set_pos(190, 700)
        self.stat_map = {
            "HP": int(pet.stats[0]),
            "AD": int(pet.stats[1]),
            "DF": int(pet.stats[2]),
            "AP": int(pet.stats[3]),
            "MD": int(pet.stats[4]),
            "SP": int(pet.stats[5]),
        }
        self.recalculate()

    def recalculate(self, **changes):
        for k, v in changes.items():
            self.talent_map[k] = v
        level = self.talent_map["level"]
        for k, v in self.talent_map.items():
            if k == "level":
                pass
            else:
                val = (self.stat_map[k] * 2 + v) * level / 100 + (
                    (level + 10) if k == "HP" else 5
                )
                self.TEXTS[f"pet_{k}"].change_text(str(int(val)))
