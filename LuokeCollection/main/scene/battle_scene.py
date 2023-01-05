import os
import pygame
from pygame.locals import *  # noqa
from LuokeCollection.main.scene.scene import Scene
from ..components.button import Button
from ..model.sound import Channel
from ...main.utils import ELEMENT_MAP, type2element
from ...settings.dev import SOUND, IMAGE

from ..components.sprite import Sprite
from ..scene.scene import Scene
from ..components.button import Button
from ..components.text import Text

EMPTY = pygame.Surface([1, 1], pygame.SRCALPHA)

class BattleScene(Scene):
    def __init__(self, screen, model, *args, **kwargs):
        super(BattleScene, self).__init__(screen, model, *args, **kwargs)
        self.background_music = SOUND("castle.wav", Channel.BACKGROUND)
        self.BUTTONS = {
            "pop": Button(text="X", x=1000, y=100, on_click=lambda: model.close()),
        }
        self.OTHERS = {}

        self.skill_pos_dict = {}
        self.skills = [None] * 4

        self.init_info()
        self.init_skills()

    def side_effect(self):
        super().side_effect()
        self.model.set_battle_display()

    def init_info(self):
        info_components = {
            "pet_name": Text("", x=200, y=200, size=32),
            "pet_image": Sprite(EMPTY),
            "pet_element": Sprite(EMPTY),
            "pet_secondary_element": Sprite(EMPTY),
            "talent_icon_HP": Sprite(EMPTY, width=36),
            "pet_HP": Text("", x=160, y=286, size=26),
            "pet_level_label": Text("等级：1", x=390, y=230, size=26),
        }

        for name, comp in info_components.items():
            if isinstance(comp, Button):
                self.BUTTONS[name] = comp
            elif isinstance(comp, Text):
                self.TEXTS[name] = comp
            else:
                self.OTHERS[name] = comp

    def set_info(self, pet):
        self.TEXTS["pet_name"].change_text(pet.name)
        pet_image = IMAGE(os.path.join("assets/data/", pet.path, "display.png"), False)
        max_width, max_height = 400, 600
        w, h = pet_image.get_size()
        if h / max_height < w / max_width:
            self.OTHERS["pet_image"].set_image(
                image=pet_image, width=max_width
            ).set_pos(300, 460)
        else:
            self.OTHERS["pet_image"].set_image(
                image=pet_image, height=max_height
            ).set_pos(300, 460)
        self.OTHERS["pet_element"].set_image(
            image=ELEMENT_MAP.get(pet.element).image, width=100
        ).set_pos(130, 210)
        if pet.secondary_element is not None:
            self.OTHERS["pet_secondary_element"].set_image(
                image=ELEMENT_MAP.get(pet.secondary_element).image, width=50
            ).set_pos(176, 224)
        else:
            self.OTHERS["pet_secondary_element"].set_image(EMPTY)

        self.OTHERS["talent_icon_HP"].set_image(
            image=IMAGE("HP.png"), width=36
        ).set_pos(130, 300)
        self.TEXTS["pet_level_label"].change_text("等级：100")
        self.TEXTS["pet_HP"].change_text("200")


    def init_skills(self):
        for i in range(4):
            y, x = 750, 350 + i * 190
            self.skill_pos_dict[i] = (x, y)
            self.TEXTS[f"skill_{i}_name"] = Text("", x=x - 40, y=y - 36, size=22)
            self.OTHERS[f"skill_{i}_element"] = Sprite(EMPTY)
            self.OTHERS[f"skill_{i}_damage_icon"] = Sprite(EMPTY)
            self.OTHERS[f"skill_{i}_pp_icon"] = Sprite(EMPTY)
            self.TEXTS[f"skill_{i}_damage"] = Text("", x=x - 30, y=y + 10, size=20)
            self.TEXTS[f"skill_{i}_pp"] = Text("", x=x + 45, y=y + 10, size=20)
            # self.TEXTS[f"skill_{i}_effect_1"] = Text("", x=x - 82, y=y - 32, size=18)
            # self.TEXTS[f"skill_{i}_effect_2"] = Text("", x=x - 82, y=y - 8, size=18)
            # self.TEXTS[f"skill_{i}_effect_3"] = Text("", x=x - 82, y=y + 16, size=18)

        buttons = map(
            lambda x: Button(
                image=EMPTY,
                x=-1000,
                y=-1000,
                # animation="custom",
                # parameter={
                #     "on_hover": lambda: self.pop_up_effect(x, True),
                #     "not_hover": lambda: self.pop_up_effect(x, False),
                # },
                animation="none",
                on_click=lambda: print("Skill clicked!"),
            ),
            range(4),
        )
        for i, button in enumerate(buttons):
            self.BUTTONS[f"skill_{i}_background"] = button

    def pop_up_effect(self, index, show):
        if show:
            self.TEXTS[f"skill_{index}_name"].hide()
            self.OTHERS[f"skill_{index}_element"].set_image(EMPTY)
            self.OTHERS[f"skill_{index}_damage_icon"].set_image(EMPTY)
            self.OTHERS[f"skill_{index}_pp_icon"].set_image(EMPTY)
            self.TEXTS[f"skill_{index}_damage"].hide()
            self.TEXTS[f"skill_{index}_pp"].hide()
            # self.TEXTS[f"skill_{index}_effect_1"].show()
            # self.TEXTS[f"skill_{index}_effect_2"].show()
            # self.TEXTS[f"skill_{index}_effect_3"].show()
        else:
            x, y = self.skill_pos_dict[index]
            self.TEXTS[f"skill_{index}_name"].show()
            self.OTHERS[f"skill_{index}_element"].set_image(
                image=ELEMENT_MAP.get(type2element(self.skills[index].type)).image,
                width=56,
            ).set_pos(x - 65, y - 26)
            self.OTHERS[f"skill_{index}_damage_icon"].set_image(
                IMAGE("damage.png"), width=30
            ).set_pos(x - 50, y + 20)
            self.OTHERS[f"skill_{index}_pp_icon"].set_image(
                IMAGE("pp.png"), width=30
            ).set_pos(x + 25, y + 20)
            self.TEXTS[f"skill_{index}_damage"].show()
            self.TEXTS[f"skill_{index}_pp"].show()
            # self.TEXTS[f"skill_{index}_effect_1"].hide()
            # self.TEXTS[f"skill_{index}_effect_2"].hide()
            # self.TEXTS[f"skill_{index}_effect_3"].hide()

    def set_skill(self, index, skill_info):
        self.skills[index] = skill_info
        if skill_info is None:
            self.TEXTS[f"skill_{index}_name"].change_text("")
            self.BUTTONS[f"skill_{index}_background"].set_image(EMPTY)
            self.OTHERS[f"skill_{index}_element"].set_image(EMPTY)
            self.OTHERS[f"skill_{index}_damage_icon"].set_image(EMPTY)
            self.OTHERS[f"skill_{index}_pp_icon"].set_image(EMPTY)
            self.TEXTS[f"skill_{index}_damage"].change_text("")
            self.TEXTS[f"skill_{index}_pp"].change_text("")
            return
        self.TEXTS[f"skill_{index}_name"].change_text(skill_info.name)
        x, y = self.skill_pos_dict[index]
        skill_bg = IMAGE("place_holder.png")
        skill_bg.set_alpha(50)
        self.BUTTONS[f"skill_{index}_background"].set_image(
            skill_bg, width=180, height=100
        ).set_pos(x, y)
        self.OTHERS[f"skill_{index}_element"].set_image(
            image=ELEMENT_MAP.get(type2element(skill_info.type)).image, width=56
        ).set_pos(x - 65, y - 26)
        self.OTHERS[f"skill_{index}_damage_icon"].set_image(
            IMAGE("damage.png"), width=30
        ).set_pos(x - 50, y + 20)
        self.OTHERS[f"skill_{index}_pp_icon"].set_image(
            IMAGE("pp.png"), width=30
        ).set_pos(x + 25, y + 20)
        self.TEXTS[f"skill_{index}_damage"].change_text(str(skill_info.power))
        self.TEXTS[f"skill_{index}_pp"].change_text(str(skill_info.PP))
        # self.TEXTS[f"skill_{index}_effect_1"].change_text(skill_info.effect[:12])
        # self.TEXTS[f"skill_{index}_effect_2"].change_text(skill_info.effect[12:24])
        # self.TEXTS[f"skill_{index}_effect_3"].change_text(skill_info.effect[24:36])
        # self.TEXTS[f"skill_{index}_effect_1"].hide()
        # self.TEXTS[f"skill_{index}_effect_2"].hide()
        # self.TEXTS[f"skill_{index}_effect_3"].hide()

