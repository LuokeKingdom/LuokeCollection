import os
import pygame
from pygame.locals import *  # noqa
from ..model.sound import Channel

from .scene import Scene
from ..components.button import Button
from ..components.text import Text
from ..components.sprite import Sprite
from ..components.slider import Slider
from LuokeCollection.settings.dev import SOUND, IMAGE
from ..utils import ELEMENT_MAP, type2element

EMPTY = pygame.Surface([1, 1], pygame.SRCALPHA)


class TrainingScene(Scene):
    def __init__(self, screen, model, *args, **kwargs):
        super(TrainingScene, self).__init__(screen, model, 'training.png', *args, **kwargs)
        self.background_music = SOUND("peter_ave.wav", Channel.BACKGROUND)
        self.skill_pos_dict = {}
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
        self.skills = {}
        self.current_slots = [-1] * 4
        self.battle_skill_selected = -1
        self.factory_skill_selected = -1
        self.BUTTONS = {
            "close": Button(
                image=IMAGE("close.png"),
                x=1100,
                y=70,
                on_click=lambda: self.model.close()
                or self.model.set_battle_prep(self.model.battle_prep_offset),
                animation="opacity",
                parameter={"factor": 0.2},
                width=120,
            ),
            "next_page": Button(
                image=pygame.transform.flip(IMAGE("previous.png"), True, False),
                x=810,
                y=649,
                on_click=lambda: self.model.next_skill_page(),
                animation="opacity",
                parameter={"factor": 0.2},
                width=48,
            ),
            "previous_page": Button(
                image=IMAGE("previous.png"),
                x=690,
                y=649,
                on_click=lambda: model.previous_skill_page(),
                animation="opacity",
                parameter={"factor": 0.2},
                width=48,
            ),
            "replace_skill": Button(
                image=IMAGE("place_holder.png"),
                x=750,
                y=649,
                on_click=lambda: self.update_slots()
                and self.model.replace_skills(self.current_slots),
                animation="opacity",
                parameter={"factor": 0.2},
                width=48,
            ),
            "save_pet": Button(
                image=IMAGE("place_holder.png"),
                x=1000,
                y=649,
                on_click=lambda: self.model.save_pet_content(
                    self.talent_map, self.current_slots
                ),
                animation="opacity",
                parameter={"factor": 0.2},
                width=48,
            ),
        }
        self.init_info()
        self.init_skills()

    def side_effect(self, **kwargs):
        super().side_effect(**kwargs)
        self.model.skill_page_number = 1
        if len(kwargs):
            self.talent_map = kwargs["talent_map"]
            self.model.load_skills(kwargs["skills"])
        else:
            self.model.load_skills()
        self.model.set_info()

    def init_info(self):
        active_image_1 = IMAGE("place_holder.png")
        active_image_1.set_alpha(50)
        active_image_2 = IMAGE("place_holder.png")
        active_image_2.set_alpha(50)
        info_components = {
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
            "pet_talent_HP": Text("", x=220, y=186, size=26),
            "pet_talent_AD": Text("", x=220, y=266, size=26),
            "pet_talent_DF": Text("", x=220, y=346, size=26),
            "pet_talent_SP": Text("", x=220, y=426, size=26),
            "pet_talent_AP": Text("", x=220, y=506, size=26),
            "pet_talent_MD": Text("", x=220, y=586, size=26),
            "pet_talent_label_HP": Text("天赋：0", x=320, y=186, size=26),
            "pet_talent_label_AD": Text("天赋：0", x=320, y=266, size=26),
            "pet_talent_label_DF": Text("天赋：0", x=320, y=346, size=26),
            "pet_talent_label_SP": Text("天赋：0", x=320, y=426, size=26),
            "pet_talent_label_AP": Text("天赋：0", x=320, y=506, size=26),
            "pet_talent_label_MD": Text("天赋：0", x=320, y=586, size=26),
            "pet_talent_slider_HP": Slider(
                x=500,
                y=200,
                animation="opacity",
                on_click=lambda: 0,
                parameter={"factor": 0.5},
                on_change=lambda x: self.recalculate(HP=x),
            ),
            "pet_talent_slider_AD": Slider(
                x=500,
                y=280,
                animation="opacity",
                on_click=lambda: 0,
                parameter={"factor": 0.5},
                on_change=lambda x: self.recalculate(AD=x),
            ),
            "pet_talent_slider_DF": Slider(
                x=500,
                y=360,
                animation="opacity",
                on_click=lambda: 0,
                parameter={"factor": 0.5},
                on_change=lambda x: self.recalculate(DF=x),
            ),
            "pet_talent_slider_SP": Slider(
                x=500,
                y=440,
                animation="opacity",
                on_click=lambda: 0,
                parameter={"factor": 0.5},
                on_change=lambda x: self.recalculate(SP=x),
            ),
            "pet_talent_slider_AP": Slider(
                x=500,
                y=520,
                animation="opacity",
                on_click=lambda: 0,
                parameter={"factor": 0.5},
                on_change=lambda x: self.recalculate(AP=x),
            ),
            "pet_talent_slider_MD": Slider(
                x=500,
                y=600,
                animation="opacity",
                on_click=lambda: 0,
                parameter={"factor": 0.5},
                on_change=lambda x: self.recalculate(MD=x),
            ),
            "pet_level_label": Text("等级：1", x=450, y=60, size=26),
            "pet_level_slider": Slider(
                x=500,
                y=114,
                interval=[1, 100],
                animation="opacity",
                on_click=lambda: 0,
                parameter={"factor": 0.5},
                on_change=lambda x: self.recalculate(level=x),
            ),
            "factory_skill_selected": Sprite(
                active_image_1,
                width=180,
                height=100,
                x=-200,
                y=-200,
            ),
            "battle_skill_selected": Sprite(
                active_image_2, width=180, height=100, x=-200, y=-200
            ),
        }
        for name, comp in info_components.items():
            if isinstance(comp, Button):
                self.BUTTONS[name] = comp
            elif isinstance(comp, Text):
                self.TEXTS[name] = comp
            else:
                self.OTHERS[name] = comp

    def recalculate(self, **changes):
        for k, v in changes.items():
            self.talent_map[k] = v
        level = self.talent_map["level"]
        for k, v in self.talent_map.items():
            if k == "level":
                self.TEXTS["pet_level_label"].change_text("等级：" + str(v))
            else:
                self.TEXTS[f"pet_talent_label_{k}"].change_text("天赋：" + str(v))
                val = (self.stat_map[k] * 2 + v) * level / 100 + (
                    (level + 10) if k == "HP" else 5
                )
                self.TEXTS[f"pet_talent_{k}"].change_text(str(int(val)))

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
        self.OTHERS["pet_image"].image.set_alpha(60)
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
        ).set_pos(190, 200)
        self.OTHERS["talent_icon_AD"].set_image(
            image=IMAGE("AD.png"), width=36
        ).set_pos(190, 280)
        self.OTHERS["talent_icon_DF"].set_image(
            image=IMAGE("DF.png"), width=36
        ).set_pos(190, 360)
        self.OTHERS["talent_icon_SP"].set_image(
            image=IMAGE("SP.png"), width=36
        ).set_pos(190, 440)
        self.OTHERS["talent_icon_AP"].set_image(
            image=IMAGE("AP.png"), width=36
        ).set_pos(190, 520)
        self.OTHERS["talent_icon_MD"].set_image(
            image=IMAGE("MD.png"), width=36
        ).set_pos(190, 600)
        self.stat_map = {
            "HP": int(pet.stats[0]),
            "AD": int(pet.stats[1]),
            "DF": int(pet.stats[2]),
            "AP": int(pet.stats[3]),
            "MD": int(pet.stats[4]),
            "SP": int(pet.stats[5]),
        }
        self.recalculate()

    def init_skills(self):
        for i in range(8):
            x, y = 750, 200 + i * 120
            if i > 3:
                x, y = 1000, 200 + (i - 4) * 120
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

        def get_click_function(i):
            return lambda: self.select_skill(i)

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
                on_click=get_click_function(x),
            ),
            range(8),
        )
        for i, button in enumerate(buttons):
            self.BUTTONS[f"skill_{i}_background"] = button

    def select_skill(self, i):
        x, y = self.skill_pos_dict[i]
        if i < 4:
            if self.factory_skill_selected == i:
                self.factory_skill_selected = -1
                self.OTHERS["factory_skill_selected"].set_pos(-200, -200)
            else:
                self.factory_skill_selected = i
                self.OTHERS["factory_skill_selected"].set_pos(x, y)
        else:
            if self.battle_skill_selected == i - 4:
                self.battle_skill_selected = -1
                self.OTHERS["battle_skill_selected"].set_pos(-200, -200)
            else:
                self.battle_skill_selected = i - 4
                self.OTHERS["battle_skill_selected"].set_pos(x, y)

    def set_skill(self, index, skill_info):
        self.skills[index] = skill_info
        x, y = self.skill_pos_dict[index]
        if index > 3:
            if skill_info is None:
                self.current_slots[index - 4] = -1
            else:
                self.current_slots[index - 4] = skill_info.index
        if skill_info is None:
            self.TEXTS[f"skill_{index}_name"].change_text("")
            self.BUTTONS[f"skill_{index}_background"].set_image(
                IMAGE("skill_temp.png"), width=180, height=100
            ).set_pos(x, y)
            self.OTHERS[f"skill_{index}_element"].set_image(EMPTY)
            self.OTHERS[f"skill_{index}_damage_icon"].set_image(EMPTY)
            self.OTHERS[f"skill_{index}_pp_icon"].set_image(EMPTY)
            self.TEXTS[f"skill_{index}_damage"].change_text("")
            self.TEXTS[f"skill_{index}_pp"].change_text("")
            return
        self.TEXTS[f"skill_{index}_name"].change_text(skill_info.name)
        self.BUTTONS[f"skill_{index}_background"].set_image(
            IMAGE("skill_temp.png"), width=180, height=100
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
        self.TEXTS[f"skill_{index}_effect_1"].change_text(skill_info.effect[:12])
        self.TEXTS[f"skill_{index}_effect_2"].change_text(skill_info.effect[12:24])
        self.TEXTS[f"skill_{index}_effect_3"].change_text(skill_info.effect[24:36])
        self.TEXTS[f"skill_{index}_effect_1"].hide()
        self.TEXTS[f"skill_{index}_effect_2"].hide()
        self.TEXTS[f"skill_{index}_effect_3"].hide()

    def pop_up_effect(self, index, show):
        if index > 3 and self.current_slots[index - 4] < 0:
            return
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
            self.TEXTS[f"skill_{index}_effect_1"].hide()
            self.TEXTS[f"skill_{index}_effect_2"].hide()
            self.TEXTS[f"skill_{index}_effect_3"].hide()

    def update_slots(self):
        if self.battle_skill_selected < 0 or self.factory_skill_selected < 0:
            self.model.error_sound.play()
            return False
        if self.factory_skill_selected > 3:
            if self.current_slots[self.battle_skill_selected] != -1:
                self.current_slots[self.battle_skill_selected] = -1
                self.OTHERS["battle_skill_selected"].set_pos(-200, -200)
                return True
            else:
                self.model.error_sound.play()
                return False
        for i in range(4):
            if self.current_slots[i] == self.skills[self.factory_skill_selected].index:
                self.model.error_sound.play()
                return False
        self.current_slots[self.battle_skill_selected] = self.skills[
            self.factory_skill_selected
        ].index
        self.OTHERS["battle_skill_selected"].set_pos(-200, -200)
        self.OTHERS["factory_skill_selected"].set_pos(-200, -200)
        return True
