from LuokeCollection.main.battle.battle_animation import BattleAnimation
from LuokeCollection.main.utils import type2element
from .pet_status import PetStatus
from random import choice


class ActionSolver:
    def __init__(self, action_index, user, taker):
        self.primary = user
        self.secondary = taker
        self.user_status_change = PetStatus()
        self.taker_status_change = PetStatus()
        self.damage_user = None
        self.damage_taker = None
        self.heal_user = 10
        self.heal_taker = None
        self.skill = None
        self.user_pet_index = None
        self.system = None

        if action_index < 4:
            self.use_skill(action_index, user, taker)
        elif action_index - 10 < 6:
            self.user_pet_index = action_index - 10
        elif action_index - 100 < 6:
            self.use_potion(action_index - 100, user)
            pass



    def use_skill(self, skill_index, user, taker):
        skill = user.skills[skill_index]
        self.skill = skill
        self.user_status_change.skill_PPs[skill_index][0] = -1
        skill_element = type2element(skill.type)
        if skill_element:
            pass
        element_ratio = 1
        critical = 1

        skill_type = skill.type[2:]
        if skill_type == "变化":
            pass
        elif skill_type == "物理":
            self.damage_taker = int(
                (
                    (user.level * 0.4 + 2) * int(skill.power) * user.AD / taker.DF / 50
                    + 2
                )
                * element_ratio
                * choice(range(217, 256))
                * critical
                / 255
            )
        elif skill_type == "魔法":
            self.damage_taker = int(
                (
                    (user.level * 0.4 + 2) * int(skill.power) * user.AP / taker.MD / 50
                    + 2
                )
                * element_ratio
                * choice(range(217, 256))
                * critical
                / 255
            )

    def get_damage(self):
        return self.damage_taker, self.damage_user

    def get_heal(self):
        return self.heal_taker, self.heal_user

    def use_potion(self, potion_index, user):
        self.heal_user = (potion_index+1) * 50

    def solve(self, system):
        self.system = system
        primary, secondary = self.primary, self.secondary
        if self.skill is not None:
            self.append_log(
                f"对{secondary.info.name}使用了<{self.skill.name}>", primary.is_self
            )
        if self.damage_taker is not None:
            secondary.change_health(-self.damage_taker)
            self.animate_attack(primary, secondary, self.damage_taker)
        if self.damage_user is not None:
            primary.change_health(-self.damage_user)
            self.animate_number(primary, -self.damage_user)
        if self.heal_user is not None:
            primary.change_health(self.heal_user)
            self.animate_heal(primary, self.heal_user)
        if self.heal_taker is not None:
            secondary.change_health(self.heal_taker)
            self.animate_heal(secondary, self.heal_taker)

        if self.user_pet_index is not None:
            if primary.is_self:
                self.animate_change_pet(primary, system.team1[self.user_pet_index])
                system.current_pet1 = self.user_pet_index
            else:
                self.animate_change_pet(secondary, system.team1[self.user_pet_index])
                system.current_pet2 = self.user_pet_index

    def append_log(self, text, is_self):
        self.push_anim(
            "stuff_change",
            on_update=self.system.on_log_update,
            stuff=f"{'你' if is_self else '对手'}" + text,
        ).next_anim()

    def animate_attack(self, primary, secondary, damage):

        pos_data1, rev_data1 = self.get_position_data(
            [
                (0, (0, 0)),
                (0.6, (200, 0)),
                (0.7, (265, 0)),
            ],
            not primary.is_self,
        )
        pos_data2, rev_data2 = self.get_position_data(
            [
                (0.1, (310, 0)),
                (0.2, (300, 0)),
            ],
            not primary.is_self,
        )

        self.push_anim(
            "position", data=pos_data1, display=primary.sprite_display
        ).next_anim()
        self.push_anim("position", data=pos_data2, display=primary.sprite_display)
        self.animate_number(secondary, -damage)
        self.push_anim(
            "position", data=rev_data2, display=primary.sprite_display
        ).next_anim()
        self.push_anim(
            "position", data=rev_data1, display=primary.sprite_display
        ).next_anim()

    def animate_number(self, pet, number):
        self.push_anim(
            "text",
            text="+" + str(number) if number > 0 else number,
            color=(255, 0, 0) if number < 0 else (0, 255, 0),
            display=pet.number_display,
            interval=1,
        )
        self.push_anim(
            "text_change", text=pet.health, display=pet.health_display
        ).next_anim()
        self.push_anim("none", interval=0.5).next_anim()

    def animate_heal(self, pet, heal):
        self.append_log("回复了体力", pet.is_self)
        pos_data1, rev_data1 = self.get_position_data(
            [
                (0.0, (0, 0)),
                (0.2, (0, -3)),
                (0.4, (0, -7)),
                (0.6, (0, -15)),
            ],
            pet.is_self,
        )
        self.push_anim(
            "position", data=pos_data1, display=pet.sprite_display
        ).next_anim()
        self.animate_number(pet, heal)
        self.push_anim(
            "position", data=rev_data1, display=pet.sprite_display
        ).next_anim()

    def animate_change_pet(self, pet, new_pet):
        scale_data, rev_data = self.get_scale_data([
            (0, 0),
            (1, -1),
        ])
        display = pet.sprite_display
        self.push_anim('scale', data=scale_data, display=display).next_anim()
        image_pos = display.get_pos()
        self.push_anim('stuff_change', on_update=lambda x: display.set_image(x).set_pos(*image_pos), stuff=new_pet.image)
        self.push_anim('scale', data=rev_data, display=display).next_anim()
        pass

    def push_anim(self, name, **kwargs):
        self.system.push_anim(name, **kwargs)
        return self

    def next_anim(self):
        self.system.next_anim()

    def get_position_data(self, data, inversed):
        data.sort()
        position_data = list(
            map(lambda x: (x[0], (-x[1][0], x[1][1])) if inversed else x, data)
        )
        reversed_data = list(
            zip(
                list(
                    reversed(
                        [
                            position_data[-1][0] - position_data[i][0]
                            for i in range(len(position_data))
                        ]
                    )
                ),
                list(reversed(list(zip(*position_data))[1])),
            )
        )
        return position_data, reversed_data

    def get_scale_data(self, data):
        scale_data = sorted(data)
        reversed_data = self.reverse_data(scale_data)
        return scale_data, reversed_data

    def reverse_data(self, data):
        return list(
                zip(
                    list(
                        reversed(
                            [
                                data[-1][0] - data[i][0]
                                for i in range(len(data))
                            ]
                        )
                    ),
                    list(reversed(list(zip(*data))[1])),
                )
            )
