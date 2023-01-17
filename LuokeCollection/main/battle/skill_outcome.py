from LuokeCollection.main.utils import SkillInfo
from .skill_effect import SkillEffect
from .animator import Animator
from .battle_pet import BattlePet
from ..utils import Element
from .rng import rng


class SkillOutcome:
    labels2function = {
        "a": "attack",
        ".": "potion",
        "e": "effect",
    }

    def attack(
        primary: BattlePet,
        secondary: BattlePet,
        skill: SkillInfo,
        args: str,
        anim: Animator,
        rng: rng
    ):
        skill_element = Element(skill.type[:2])
        defender_e1, defender_e2 = Element(secondary.info.element), Element(
            secondary.info.secondary_element
        )
        element_ratio = skill_element.attack(defender_e1, defender_e2)
        critical_chance = 0.5 * primary.status.CR.factor
        critical = 2 if rng.get() < critical_chance else 1
        skill_type = skill.type[2:]
        if skill_type == "变化":
            print("Wrong label")
            # raise Exception("Wrong label")
        elif skill_type == "物理":
            damage = int(
                (
                    (primary.level * 0.4 + 2)
                    * int(skill.power)
                    * primary.AD
                    / secondary.DF
                    / 50
                    + 2
                )
                * element_ratio
                * (int(rng.get() * (256-217)) + 217)
                * critical
                / 255
            )
        elif skill_type == "魔法":
            damage = int(
                (
                    (primary.level * 0.4 + 2)
                    * int(skill.power)
                    * primary.AP
                    / secondary.MD
                    / 50
                    + 2
                )
                * element_ratio
                * (int(rng.get() * (256-217)) + 217)
                * critical
                / 255
            )

        secondary.change_health(-damage)
        anim.animate_attack(primary, secondary, damage)
        if critical == 2:
            print(critical_chance)
            anim.append_log("暴击了！！！", primary.is_self)

    def potion(
        primary: BattlePet,
        secondary: BattlePet,
        skill: SkillInfo,
        args: str,
        anim: Animator,
        rng: rng
    ):
        heal_amount = (1 + int(args)) * 50
        primary.change_health(heal_amount)
        anim.animate_potion(primary, heal_amount)

    def effect(
        primary: BattlePet,
        secondary: BattlePet,
        skill: SkillInfo,
        args: str,
        anim: Animator,
        rng: rng
    ):
        effect_label = args[0]
        secondary.add_effect(effect_label, SkillEffect.get(effect_label)(secondary, anim, args))
        anim.append_log("有异常状态！！！", secondary.is_self)
