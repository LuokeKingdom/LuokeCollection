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
        "b": "buff",
        "d": "debuff",
        "r": "attack_reflect",
        "c": "attack_critical",
        "h": "heal",
    }

    def attack(
        primary: BattlePet,
        secondary: BattlePet,
        skill: SkillInfo,
        args: str,
        anim: Animator,
        rng: rng,
        critical_ratio = 0
    ):
        skill_element = Element(skill.type[:2])
        defender_e1, defender_e2 = Element(secondary.info.element), Element(
            secondary.info.secondary_element
        )
        element_ratio = skill_element.attack(defender_e1, defender_e2)
        critical_chance = 0.5 * primary.status.CR.factor * critical_ratio
        print(critical_chance)
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
                * (int(rng.get() * (256 - 217)) + 217)
                * critical
                / 255
            )
            print("物理")
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
                * (int(rng.get() * (256 - 217)) + 217)
                * critical
                / 255
            )
            print("魔法")

        secondary.change_health(-damage)
        anim.animate_attack(primary, secondary, damage)
        if critical == 2:
            # print(critical_chance)
            anim.append_log("暴击了！！！", primary.is_self)

        return damage

    def potion(
        primary: BattlePet,
        secondary: BattlePet,
        skill: SkillInfo,
        args: str,
        anim: Animator,
        rng: rng,
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
        rng: rng,
    ):
        effect_label = args[0]
        accuracy_rate = int(args[1:3])
        if accuracy_rate == 0 or rng.get() * 100 < accuracy_rate:
            secondary.add_effect(
                effect_label, SkillEffect.get(effect_label)(secondary, anim, args)
            )
            if effect_label=='b':
                SkillOutcome.debuff(primary, secondary, None, 'AD2-', anim, rng)
            anim.append_log("有异常状态！！！", secondary.is_self)

    def buff(
        primary: BattlePet,
        secondary: BattlePet,
        skill: SkillInfo,
        args: str,
        anim: Animator,
        rng: rng,
    ):
        stat_label = args[:2]
        change = int(args[2])
        is_primary = args[-1]!='-'
        pet = primary if is_primary else secondary
        pet.status.stat_buffs.get(stat_label).change(change)
        pet.update_current_stats()
        anim.append_log(f"的<{stat_label}>提升了", pet.is_self)

    def debuff(
        primary: BattlePet,
        secondary: BattlePet,
        skill: SkillInfo,
        args: str,
        anim: Animator,
        rng: rng,
    ):
        stat_label = args[:2]
        change = int(args[2])
        is_primary = args[-1]!='-'
        pet = primary if is_primary else secondary
        pet.status.stat_buffs.get(stat_label).change(-change)
        pet.update_current_stats()
        anim.append_log(f"的<{stat_label}>降低了", pet.is_self)

    def attack_reflect(
        primary: BattlePet,
        secondary: BattlePet,
        skill: SkillInfo,
        args: str,
        anim: Animator,
        rng: rng,
    ):
        damage = SkillOutcome.attack(primary, secondary, skill, args, anim, rng)
        fraction = int(args.split('/')[0]) / int(args.split('/')[1])
        self_damage = int(fraction * damage)
        primary.change_health(-self_damage)
        anim.animate_number(primary, -self_damage)

    def attack_critical(
        primary: BattlePet,
        secondary: BattlePet,
        skill: SkillInfo,
        args: str,
        anim: Animator,
        rng: rng,
    ):
        ratio = int(args)
        print(ratio)
        SkillOutcome.attack(primary, secondary, skill, args, anim, rng, critical_ratio = ratio)

    def heal(
        primary: BattlePet,
        secondary: BattlePet,
        skill: SkillInfo,
        args: str,
        anim: Animator,
        rng: rng,
    ):
        fraction = int(args.split('/')[0]) / int(args.split('/')[1])
        heal = int(primary.max_health * fraction)
        anim.animate_heal(primary, heal)