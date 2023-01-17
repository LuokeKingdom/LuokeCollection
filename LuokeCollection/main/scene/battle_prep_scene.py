import os
import pygame
from pygame.locals import *  # noqa

from ...main.utils import ELEMENT_MAP, str2element
from ...settings.dev import SOUND, IMAGE
from ..components.sprite import Sprite
from ..scene.scene import Scene
from ..components.button import Button
from ..components.text import Text
from ..model.sound import Channel


EMPTY = pygame.Surface([1, 1], pygame.SRCALPHA)


class BattlePrepScene(Scene):
    def __init__(self, screen, model, *args, **kwargs):
        super(BattlePrepScene, self).__init__(
            screen, model, "light_orange.png", *args, **kwargs
        )
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
        self.skill_pos_dict = {}
        self.skills = [None] * 4
        self.BUTTONS["pop"] = Button(
            text="X", x=1100, y=100, on_click=lambda: model.close()
        )
        self.BUTTONS["train"] = Button(
            image=IMAGE("edit.png"),
            x=1000,
            y=600,
            on_click=lambda: self.model.open(
                "training",
                talent_map=self.talent_map,
                skills=[
                    (-1 if skill is None else skill.index) for skill in self.skills
                ],
            ),
            width=100,
            animation="opacity",
            parameter={"factor": 0.4},
        )
        self.BUTTONS["battle"] = Button(
            image=IMAGE("battle.png"),
            on_click=lambda: self.model.ready_for_battle(),
            x=1100,
            y=600,
            width=100,
            animation="opacity",
            parameter={"factor": 0.4},
        )
        self.init_pets()
        self.init_info()
        self.init_skills()

    def side_effect(self):
        super().side_effect()
        self.model.set_battle_prep(0)
        self.model.client_init()

    def init_pets(self):
        def get_on_click(i):
            return lambda: self.model.set_battle_prep(i)

        for i in range(6):
            self.BUTTONS[f"pet_container_{i}"] = Button(
                animation="opacity",
                image=IMAGE("place_holder.png"),
                width=100,
                x=200 + i * 150,
                y=100,
                on_click=get_on_click(i),
            )
            self.TEXTS[f"pet_name_{i}"] = Text(
                "", x=200 + i * 150, y=100, align_mode="CENTER"
            )

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
            "pet_level_label": Text("等级：1", x=450, y=230, size=26),
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
        self.BUTTONS[f"pet_container_{i}"].set_image(image).set_pos(200 + i * 150, 100)
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

    def recalculate(self):
        level = self.talent_map["level"]
        for k, v in self.talent_map.items():
            if k == "level":
                self.TEXTS["pet_level_label"].change_text("等级：" + str(v))
            else:
                val = (self.stat_map[k] * 2 + v) * level / 100 + (
                    (level + 10) if k == "HP" else 5
                )
                self.TEXTS[f"pet_{k}"].change_text(str(int(val)))

    def init_skills(self):
        for i in range(4):
            x, y = 750, 300 + i * 120
            self.skill_pos_dict[i] = (x, y)
            self.TEXTS[f"skill_{i}_name"] = Text("", x=x - 40, y=y - 36, size=22)
            self.OTHERS[f"skill_{i}_element"] = Sprite(EMPTY)
            self.OTHERS[f"skill_{i}_damage_icon"] = Sprite(EMPTY)
            self.OTHERS[f"skill_{i}_pp_icon"] = Sprite(EMPTY)
            self.TEXTS[f"skill_{i}_damage"] = Text("", x=x - 30, y=y + 10, size=20)
            self.TEXTS[f"skill_{i}_pp"] = Text("", x=x + 45, y=y + 10, size=20)
            self.TEXTS[f"skill_{i}_effect_1"] = Text("", x=x - 82, y=y - 32, size=18)
            self.TEXTS[f"skill_{i}_effect_2"] = Text("", x=x - 82, y=y - 8, size=18)
            self.TEXTS[f"skill_{i}_effect_3"] = Text("", x=x - 82, y=y + 16, size=18)

        buttons = map(
            lambda x: Button(
                image=EMPTY,
                x=-1000,
                y=-1000,
                animation="custom",
                parameter={
                    "on_hover": lambda: self.pop_up_effect(x, True),
                    "not_hover": lambda: self.pop_up_effect(x, False),
                },
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
            self.TEXTS[f"skill_{index}_effect_1"].show()
            self.TEXTS[f"skill_{index}_effect_2"].show()
            self.TEXTS[f"skill_{index}_effect_3"].show()
        else:
            x, y = self.skill_pos_dict[index]
            self.TEXTS[f"skill_{index}_name"].show()
            self.OTHERS[f"skill_{index}_element"].set_image(
                image=ELEMENT_MAP.get(str2element(self.skills[index].type)).image,
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
            self.TEXTS[f"skill_{index}_effect_1"].hide()
            self.TEXTS[f"skill_{index}_effect_2"].hide()
            self.TEXTS[f"skill_{index}_effect_3"].hide()

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
        self.BUTTONS[f"skill_{index}_background"].set_image(
            IMAGE("skill_temp.png"), width=180, height=100
        ).set_pos(x, y)
        self.OTHERS[f"skill_{index}_element"].set_image(
            image=ELEMENT_MAP.get(str2element(skill_info.type)).image, width=56
        ).set_pos(x - 65, y - 26)
        self.OTHERS[f"skill_{index}_damage_icon"].set_image(
            IMAGE("damage.png"), width=30
        ).set_pos(x - 50, y + 20)
        self.OTHERS[f"skill_{index}_pp_icon"].set_image(
            IMAGE("pp.png"), width=30
        ).set_pos(x + 25, y + 20)
        self.TEXTS[f"skill_{index}_damage"].change_text(str(skill_info.power))
        self.TEXTS[f"skill_{index}_pp"].change_text(str(skill_info.PP))
        self.TEXTS[f"skill_{index}_effect_1"].change_text(skill_info.effect[:12])
        self.TEXTS[f"skill_{index}_effect_2"].change_text(skill_info.effect[12:24])
        self.TEXTS[f"skill_{index}_effect_3"].change_text(skill_info.effect[24:36])
        self.TEXTS[f"skill_{index}_effect_1"].hide()
        self.TEXTS[f"skill_{index}_effect_2"].hide()
        self.TEXTS[f"skill_{index}_effect_3"].hide()

    def update(self, delta_time, mouse_pos, clicked, pressed):
        super().update(delta_time, mouse_pos, clicked, pressed)
        # self.model.client_update()
