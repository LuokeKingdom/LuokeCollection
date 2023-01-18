import os
import pygame
from pygame.locals import *  # noqa
from ..model.sound import Channel
from ...main.utils import ELEMENT_MAP, str2element
from ...settings.dev import SOUND, IMAGE

from ..components.button import Button
from ..components.sprite import Sprite
from ..scene.scene import Scene
from ..components.text import Text

EMPTY = pygame.Surface([1, 1], pygame.SRCALPHA)


class BattleScene(Scene):
    def __init__(self, screen, model, *args, **kwargs):
        super(BattleScene, self).__init__(
            screen, model, "skill_temp.png", *args, **kwargs
        )
        self.background_music = SOUND("castle.wav", Channel.BACKGROUND)
        self.BUTTONS["pop"] = Button(
            text="X", x=1000, y=100, on_click=lambda: model.close()
        )
        self.logs = []

        self.skill_pos_dict = {}
        self.skills = [None] * 4
        self.system = None

        self.options_pos_dict = {}

        self.init_info()
        self.init_skills()
        self.init_battle_log()
        self.init_menu()

        self.is_preparing = False
        self.timer = 0
        self.max_wait_time = 11
        self.done = False
        self.turn_begun = False

    def side_effect(self):
        super().side_effect()
        self.done = False
        self.append_battle_log(log="", clear=True)
        self.timer = 0
        self.is_preparing = False
        self.system = self.model.get_battle_system()
        self.system.set_number_display(
            self.TEXTS["pet_battle_damage_1"], self.TEXTS["pet_battle_damage_2"]
        )
        self.system.set_health_display(self.TEXTS["pet_HP_1"], self.TEXTS["pet_HP_2"])
        self.system.set_sprite_display(
            self.OTHERS["pet_image_1"],
            self.OTHERS["pet_image_2"],
        )
        self.system.on_log_update = self.append_battle_log
        self.fight_menu()
        self.system.push_anim(
            "text", text="战斗开始", display=self.TEXTS["hint_display"], interval=1
        ).next_anim()
        self.system.push_anim(
            "text", text="准备阶段", display=self.TEXTS["hint_display"], interval=1
        ).next_anim()

    def update(self, delta_time, mouse_pos, clicked, pressed):
        super().update(delta_time, mouse_pos, clicked, pressed)
        # self.model.client_update()
        if self.turn_ready() and not self.turn_begun:
            self.turn_begun = True
            self.begin_turn()
        if self.done:
            self.TEXTS["timer_display"].change_text("")
            if self.system.has_animation():
                self.system.update_animation(delta_time)
            return
        if self.system.done:
            text = "胜利" if self.system.win else "失败"
            self.system.push_anim(
                "text_change", text=text, display=self.TEXTS["hint_display"]
            ).next_anim()
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
        elif self.waiting_for_opponent():
            self.TEXTS["timer_display"].change_text("等待对手出招")
        else:
            self.TEXTS["timer_display"].change_text("")
            if self.system.has_animation():
                self.system.update_animation(delta_time)
                if not self.system.has_animation():
                    self.model.reset_turn()

    def turn_ready(self):
        return self.model.self_action_chosen > -1 and self.model.oppo_action_chosen > -1

    def waiting_for_opponent(self):
        return self.model.self_action_chosen > -1 and self.model.oppo_action_chosen < 0

    def begin_turn(self):
        if not self.system.done:
            self.system.prepare(
                self.model.self_action_chosen, self.model.oppo_action_chosen
            )
            self.system.act()
            if not self.system.done:
                self.system.push_anim(
                    "text", text="准备阶段", display=self.TEXTS["hint_display"], interval=1
                ).next_anim()

    def choose_action(self, i):
        self.is_preparing = False
        self.model.self_action_chosen = i

    def display_pets(self):
        pet1, pet2 = self.system.get_pets()
        self.update_info(pet1, pet2)
        for i in range(4):
            if pet1.skill_indices[i] == -1:
                self.set_skill(i, None)
            else:
                self.set_skill(
                    i,
                    pet1.info.skills[pet1.skill_indices[i]],
                )

    def init_info(self):
        info_components = {
            "pet_name_1": Text("", x=200, y=100, size=32),
            "pet_image_1": Sprite(EMPTY),
            "pet_element_1": Sprite(EMPTY),
            "pet_secondary_element_1": Sprite(EMPTY),
            "talent_icon_HP_1": Sprite(EMPTY, width=36),
            "pet_HP_1": Text("", x=160, y=186, size=26),
            "pet_level_label_1": Text("", x=390, y=130, size=26),
            "pet_battle_damage_1": Text(
                "", x=400, y=200, size=50, color=(255, 255, 255), align_mode="CENTER"
            ),
            "pet_name_2": Text("", x=1179, y=100, size=32),
            "pet_image_2": Sprite(EMPTY),
            "pet_element_2": Sprite(EMPTY),
            "pet_secondary_element_2": Sprite(EMPTY),
            "talent_icon_HP_2": Sprite(EMPTY, width=36),
            "pet_HP_2": Text("", x=1079, y=186, size=26),
            "pet_level_label_2": Text("", x=849, y=130, size=26),
            "pet_battle_damage_2": Text(
                "", x=829, y=200, size=50, color=(255, 255, 255), align_mode="CENTER"
            ),
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
        pet_image = pygame.transform.flip(
            IMAGE(os.path.join("assets/data/", pet1.info.path, "display.png"), False),
            True,
            False,
        )
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
        pet_image = IMAGE(
            os.path.join("assets/data/", pet2.info.path, "display.png"), False
        )
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

        buttons = map(
            lambda x: Button(
                image=EMPTY,
                x=-1000,
                y=-1000,
                animation="opacity",
                opacity=0.2,
                parameter={"factor": 0.3},
                on_click=(lambda a: lambda: self.choose_action(a))(x),
                can_hover=lambda: self.is_preparing,
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
        # self.TEXTS[f"skill_{index}_effect_1"].change_text(skill_info.effect[:12])
        # self.TEXTS[f"skill_{index}_effect_2"].change_text(skill_info.effect[12:24])
        # self.TEXTS[f"skill_{index}_effect_3"].change_text(skill_info.effect[24:36])
        # self.TEXTS[f"skill_{index}_effect_1"].hide()
        # self.TEXTS[f"skill_{index}_effect_2"].hide()
        # self.TEXTS[f"skill_{index}_effect_3"].hide()

    def init_battle_log(self):
        log_components = {
            f"log_line_{i}": Text("", size=15, x=9, y=691 + i * 17) for i in range(7)
        }
        log_components["log_background"] = Sprite(
            image=IMAGE("light_blue.png"), width=250, height=120, x=130, y=750
        )

        for name, comp in log_components.items():
            if isinstance(comp, Button):
                self.BUTTONS[name] = comp
            elif isinstance(comp, Text):
                self.TEXTS[name] = comp
            else:
                self.OTHERS[name] = comp

    def append_battle_log(self, log, clear=False):
        if clear:
            self.logs.clear()
        else:
            self.logs.append(log)
        content = self.logs
        if len(content) > 7:
            content = self.logs[-7:]
        else:
            for i in range(len(content), 7):
                self.TEXTS[f"log_line_{i}"].change_text("")

        for i, v in enumerate(content):
            self.TEXTS[f"log_line_{i}"].change_text(v)

    def init_menu(self):
        log_components = {
            "fight": Button(
                text="战斗", x=1124, y=683, on_click=lambda: self.fight_menu()
            ),
            "pets": Button(text="换宠", x=1063, y=769, on_click=lambda: self.pets_menu()),
            "potion": Button(
                text="恢复", x=1189, y=769, on_click=lambda: self.potion_menu()
            ),
        }

        self.LAYERS[4]["option_background"] = Sprite(
            image=IMAGE("light_blue.png"), x=635, y=750, width=750, height=120
        )
        self.LAYERS[4]["option_background"].hide()
        for i in range(6):
            x, y = 334 + i * 120, 750
            self.options_pos_dict[i] = (x, y)
            self.LAYERS[5][f"option_{i}"] = Button(
                text="+"+str(i*50+50), x=x, y=y, can_hover=lambda: self.is_preparing
            )
            self.LAYERS[5][f"option_{i}"].hide()

        for name, comp in log_components.items():
            if isinstance(comp, Button):
                self.BUTTONS[name] = comp
            elif isinstance(comp, Text):
                self.TEXTS[name] = comp
            else:
                self.OTHERS[name] = comp

    def fight_menu(self):
        for i in range(4):
            self.BUTTONS[f"skill_{i}_background"].show()
        self.LAYERS[4]["option_background"].hide()
        for i in range(6):
            self.LAYERS[5][f"option_{i}"].hide()
        self.display_pets()

    def pets_menu(self):
        for i in range(4):
            self.BUTTONS[f"skill_{i}_background"].hide()
        self.LAYERS[4]["option_background"].show()
        for i in range(6):
            x, y = self.options_pos_dict[i]
            self.LAYERS[5][f"option_{i}"].show()
            pet = self.system.team1[i]
            if pet is None:
                self.LAYERS[5][f"option_{i}"].set_image(
                    EMPTY, width=100, height=100
                ).set_pos(x, y)
                self.LAYERS[5][f"option_{i}"].can_hover = lambda: False
            else:
                self.LAYERS[5][f"option_{i}"].set_image(
                    self.model.pet_rects[pet.info.number], width=100, height=100
                ).set_pos(x, y)
                self.LAYERS[5][f"option_{i}"].on_click = (
                    lambda a: lambda: self.choose_action(a)
                )(i + 10)
                self.LAYERS[5][f"option_{i}"].can_hover = (lambda a: lambda:self.system.team1[a].health > 0)(i)

    def potion_menu(self):
        for i in range(4):
            self.BUTTONS[f"skill_{i}_background"].hide()
        self.LAYERS[4]["option_background"].show()
        for i in range(6):
            x, y = self.options_pos_dict[i]
            self.LAYERS[5][f"option_{i}"].show()
            self.LAYERS[5][f"option_{i}"].set_image(
                IMAGE("light_orange.png"), width=100, height=100
            ).set_pos(x, y)
            self.LAYERS[5][f"option_{i}"].on_click = (
                lambda a: lambda: self.choose_action(a)
            )(i + 100)
