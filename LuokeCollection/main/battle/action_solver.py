from LuokeCollection.main.utils import type2element
from .pet_status import PetStatus
from random import choice


class ActionSolver:
    def __init__(self, action_index, user, taker):
        self.user_status_change = PetStatus()
        self.taker_status_change = PetStatus()
        self.damage_user = None
        self.damage_taker = None
        self.heal_user = 10
        self.heal_taker = None

        if action_index < 4:
            self.use_skill(action_index, user, taker)
        else:
            pass

    def use_skill(self, skill_index, user, taker):
        skill = user.skills[skill_index]
        self.user_status_change.skill_PPs[skill_index][0] = -1
        skill_element = type2element(skill.type)
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
