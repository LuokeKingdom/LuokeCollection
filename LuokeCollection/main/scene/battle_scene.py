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
        super(BattleScene, self).__init__(screen, model, 'skill_temp.png', *args, **kwargs)
        self.background_music = SOUND("castle.wav", Channel.BACKGROUND)
        self.BUTTONS["pop"] = Button(text="X", x=1000, y=100, on_click=lambda: model.close())

        self.skill_pos_dict = {}
        self.skills = [None] * 4
        self.system = None

        self.init_info()
        self.init_skills()

        self.is_preparing = False
        self.timer = 0
        self.max_wait_time = 10
        self.done = False

    def side_effect(self):
        super().side_effect()
        self.done = False
        self.system = self.model.get_battle_system()
        self.system.set_damage_display(
            self.TEXTS["pet_battle_damage_1"],
            self.TEXTS["pet_battle_damage_2"]
        )
        self.system.set_health_display(
            self.TEXTS["pet_HP_1"],
            self.TEXTS["pet_HP_2"]
        )
        self.display_pets()
        self.system.push_anim("text", text="战斗开始", display=self.TEXTS["hint_display"], interval=1).next_anim()
        self.system.push_anim("text", text="准备阶段", display=self.TEXTS["hint_display"], interval=1).next_anim()

    def update(self, delta_time, mouse_pos, clicked, pressed):
        super().update(delta_time, mouse_pos, clicked, pressed)
        if self.done:
            self.TEXTS["timer_display"].change_text("")
            if self.system.has_animation():
                self.system.update_animation(delta_time)
            return
        if self.system.done:
            text = "胜利" if self.system.win else "失败"
            self.system.push_anim("text_change", text=text, display=self.TEXTS["hint_display"]).next_anim()
            self.done = True
            return
        if self.is_preparing:
            prev = int(self.timer)
            self.timer += delta_time
            curr = int(self.timer)
            if curr > prev:
                self.TEXTS["timer_display"].change_text(str(self.max_wait_time - curr))
            if self.timer > self.max_wait_time:
                self.choose_action(0)
        else:
            self.TEXTS["timer_display"].change_text("")
            if self.system.has_animation():
                self.system.update_animation(delta_time)
            else:
                self.is_preparing = True
                self.timer = 0
                self.display_pets()

    def choose_action(self, i):
        if self.is_preparing and not self.system.done:
            self.is_preparing = False
            self.system.prepare(i, 0)
            self.system.act()
            if not self.system.done:
                self.system.push_anim("text", text="准备阶段", display=self.TEXTS["hint_display"], interval=1).next_anim()


    def display_pets(self):
        pet1, pet2 = self.system.get_pets()
        self.update_info(pet1, pet2)
        for i in range(4):
            if pet1.skill_indices[i] == -1:
                self.set_skill(i, None)
            else:
                self.set_skill(i, pet1.info.skills[pet1.skill_indices[i]],)

    def init_info(self):
        info_components = {
            "pet_name_1": Text("", x=200, y=100, size=32),
            "pet_image_1": Sprite(EMPTY),
            "pet_element_1": Sprite(EMPTY),
            "pet_secondary_element_1": Sprite(EMPTY),
            "talent_icon_HP_1": Sprite(EMPTY, width=36),
            "pet_HP_1": Text("", x=160, y=186, size=26),
            "pet_level_label_1": Text("", x=390, y=130, size=26),
            "pet_battle_damage_1": Text("", x=200, y=200, size=50, color=(255,255,255)),
            "pet_name_2": Text("", x=1179, y=100, size=32),
            "pet_image_2": Sprite(EMPTY),
            "pet_element_2": Sprite(EMPTY),
            "pet_secondary_element_2": Sprite(EMPTY),
            "talent_icon_HP_2": Sprite(EMPTY, width=36),
            "pet_HP_2": Text("", x=1079, y=186, size=26),
            "pet_level_label_2": Text("", x=849, y=130, size=26),
            "pet_battle_damage_2": Text("", x=939, y=200, size=50, color=(255,255,255)),
            "hint_display": Text("", align_mode="CENTER", x=620, y=413, size=60),
            "timer_display": Text("", align_mode="CENTER", x=620, y=313, size=60),
        }

        for name, comp in info_components.items():
            if isinstance(comp, Button):
                self.BUTTONS[name] = comp
            elif isinstance(comp, Text):
                self.TEXTS[name] = comp
            else:
                self.OTHERS[name] = comp

    def update_info(self, pet1, pet2):
        # 1
        self.TEXTS["pet_name_1"].change_text(pet1.info.name)
        pet_image = pygame.transform.flip(IMAGE(os.path.join("assets/data/", pet1.info.path, "display.png"), False), True, False)
        max_width, max_height = 400, 600
        w, h = pet_image.get_size()
        if h / max_height < w / max_width:
            self.OTHERS["pet_image_1"].set_image(
                image=pet_image, width=max_width
            ).set_pos(300, 360)
        else:
            self.OTHERS["pet_image_1"].set_image(
                image=pet_image, height=max_height
            ).set_pos(300, 360)
        self.OTHERS["pet_element_1"].set_image(
            image=ELEMENT_MAP.get(pet1.info.element).image, width=100
        ).set_pos(130, 110)
        if pet1.info.secondary_element is not None:
            self.OTHERS["pet_secondary_element_1"].set_image(
                image=ELEMENT_MAP.get(pet1.info.secondary_element).image, width=50
            ).set_pos(176, 124)
        else:
            self.OTHERS["pet_secondary_element_1"].set_image(EMPTY)

        self.OTHERS["talent_icon_HP_1"].set_image(
            image=IMAGE("HP.png"), width=36
        ).set_pos(130, 200)
        self.TEXTS["pet_level_label_1"].change_text(f"等级：{pet1.level}")
        self.TEXTS["pet_HP_1"].change_text(str(pet1.health))

        # 2
        self.TEXTS["pet_name_2"].change_text(pet2.info.name)
        pet_image = IMAGE(os.path.join("assets/data/", pet2.info.path, "display.png"), False)
        max_width, max_height = 400, 600
        w, h = pet_image.get_size()
        if h / max_height < w / max_width:
            self.OTHERS["pet_image_2"].set_image(
                image=pet_image, width=max_width
            ).set_pos(939, 360)
        else:
            self.OTHERS["pet_image_2"].set_image(
                image=pet_image, height=max_height
            ).set_pos(939, 360)
        self.OTHERS["pet_element_2"].set_image(
            image=ELEMENT_MAP.get(pet2.info.element).image, width=100
        ).set_pos(1109, 110)
        if pet2.info.secondary_element is not None:
            self.OTHERS["pet_secondary_element_2"].set_image(
                image=ELEMENT_MAP.get(pet2.info.secondary_element).image, width=50
            ).set_pos(1155, 124)
        else:
            self.OTHERS["pet_secondary_element_2"].set_image(EMPTY)

        self.OTHERS["talent_icon_HP_2"].set_image(
            image=IMAGE("HP.png"), width=36
        ).set_pos(1049, 200)
        self.TEXTS["pet_level_label_2"].change_text(f"等级：{pet2.level}")
        self.TEXTS["pet_HP_2"].change_text(str(pet2.health))


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
        
        def get_click_function(i):
            return lambda: self.choose_action(i)

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
                on_click=get_click_function(x),
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

