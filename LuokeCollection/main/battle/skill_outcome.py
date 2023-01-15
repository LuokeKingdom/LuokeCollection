from LuokeCollection.main.utils import SkillInfo
from random import choice
from .skill_effect import SkillEffect
from .animator import Animator
from .battle_pet import BattlePet


class SkillOutcome:
    labels2function = {
        'a': 'attack',
        'p': 'potion',
    }

    def attack(primary: BattlePet, secondary: BattlePet, skill: SkillInfo, args: str, anim: Animator):
        element_ratio = 1
        critical = 1
        skill_type = skill.type[2:]
        if skill_type == "变化":
            print("skill not found")
            # raise Exception("Wrong label")
        elif skill_type == "物理":
            damage = int(
                (
                    (primary.level * 0.4 + 2) * int(skill.power) * primary.AD / secondary.DF / 50
                    + 2
                )
                * element_ratio
                * choice(range(217, 256))
                * critical
                / 255
            )
        elif skill_type == "魔法":
            damage = int(
                (
                    (primary.level * 0.4 + 2) * int(skill.power) * primary.AP / secondary.MD / 50
                    + 2
                )
                * element_ratio
                * choice(range(217, 256))
                * critical
                / 255
            )

        secondary.change_health(-damage)
        anim.animate_attack(primary, secondary, damage)

    def potion(primary: BattlePet, secondary: BattlePet, skill: SkillInfo, args: str, anim: Animator):
        heal_amount = (1+int(args)) * 50
        primary.change_health(heal_amount)
        anim.animate_potion(primary, heal_amount)