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
        "e": "effect",  # '<AR> e<Effect><AR>[-]'
        "b": "buff",    # '<AR> b<AR><Level>#[-]'
        "d": "debuff",  # '<AR> b<AR><Level>#[-]'
        "r": "attack_reflect",  # '<AR> r#/#'
        "c": "attack_critical", # '<AR> c<Critical Ratio>
        "h": "heal",    # '<AR> h'
        "f": "fixed_damage",    # '<AR> f<Damage>'
    }

    def fixed_damage(
        primary: BattlePet,
        secondary: BattlePet,
        skill: SkillInfo,
        args: str,
        anim: Animator,
        rng: rng,
        missed: bool,
    ):
        damage = int(args)
        secondary.change_health(-damage)
        anim.animate_attack(primary, secondary, damage)

    def attack(
        primary: BattlePet,
        secondary: BattlePet,
        skill: SkillInfo,
        args: str,
        anim: Animator,
        rng: rng,
        missed: bool,
        critical_ratio = 1,
    ):
        if missed:
            anim.animate_attack(primary, secondary, "miss")
            return
        skill_element = Element(skill.type[:2])
        defender_e1, defender_e2 = Element(secondary.info.element), Element(
            secondary.info.secondary_element
        )
        element_ratio = skill_element.attack(defender_e1, defender_e2)
        critical_chance = 0.5 * primary.status.CR.factor * critical_ratio
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

        secondary.change_health(-damage)
        anim.animate_attack(primary, secondary, damage)

        if critical == 2:
            anim.append_log("暴击了！！！", primary.is_self)

        return damage

    def potion(
        primary: BattlePet,
        secondary: BattlePet,
        skill: SkillInfo,
        args: str,
        anim: Animator,
        rng: rng,
        missed: bool,
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
        missed: bool,
    ):
        if missed: return 
        effect_label = args[0]
        is_primary = args[-1]=='-'
        pet1 = primary if is_primary else secondary
        pet2 = primary if not is_primary else secondary

        accuracy_rate = int(args[1:3])
        if accuracy_rate == 0 or rng.get() * 100 < accuracy_rate:
            effect = SkillEffect.get(effect_label)(pet1, anim, args)
            if effect.immuned:
                anim.append_log(f"免疫了<{str('异常')}>", pet1.is_self)
            else:
                anim.animate_effect(pet2, pet1, effect)
                pet1.add_effect(effect_label, effect)
                if effect_label=='b':
                    SkillOutcome.debuff(pet2, pet1, None, 'AD2-', anim, rng)

    def buff(
        primary: BattlePet,
        secondary: BattlePet,
        skill: SkillInfo,
        args: str,
        anim: Animator,
        rng: rng,
        missed: bool,
    ):
        if missed:
            return
        accuracy_rate = int(args[:2])
        stat_label = args[2:4]
        change = int(args[4])
        is_primary = args[-1]!='-'
        pet = primary if is_primary else secondary
        if accuracy_rate == 0 or rng.get() * 100 < accuracy_rate:
            anim.animate_buff(pet)
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
        missed: bool,
    ):
        if missed:
            return
        accuracy_rate = int(args[:2])
        stat_label = args[2:4]
        change = int(args[4])
        is_primary = args[-1]!='-'
        pet1 = primary if is_primary else secondary
        pet2 = primary if not is_primary else secondary
        if accuracy_rate == 0 or rng.get() * 100 < accuracy_rate:
            anim.animate_move(pet2)
            anim.animate_debuff(pet1, stat_label)
            pet1.status.stat_buffs.get(stat_label).change(-change)
            anim.append_log(f"的<{stat_label}>降低了", pet1.is_self)
            pet1.update_current_stats()

    def attack_reflect(
        primary: BattlePet,
        secondary: BattlePet,
        skill: SkillInfo,
        args: str,
        anim: Animator,
        rng: rng,
        missed: bool,
    ):
        damage = SkillOutcome.attack(primary, secondary, skill, args, anim, rng, missed)
        if missed:
            return
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
        missed: bool,
    ):
        ratio = int(args)
        SkillOutcome.attack(primary, secondary, skill, args, anim, rng, missed, critical_ratio = ratio)
        if missed:
            return

    def heal(
        primary: BattlePet,
        secondary: BattlePet,
        skill: SkillInfo,
        args: str,
        anim: Animator,
        rng: rng,
        missed: bool,
    ):
        fraction = int(args.split('/')[0]) / int(args.split('/')[1])
        heal = int(primary.max_health * fraction)
        anim.animate_heal(primary, heal)