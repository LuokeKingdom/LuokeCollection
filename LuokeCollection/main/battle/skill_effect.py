from .battle_pet import BattlePet
from .animator import Animator


class EffectBase:
    def __init__(self, pet: BattlePet, animator: Animator, rng):
        self.name = None
        self.turns = -1
        self.done = False
        self.pet = pet
        self.anim = animator
        self.rng = rng
        self.is_post_effect = True
        self.immuned = False

    def solve(self, secondary: BattlePet):
        if self.turns > 0:
            self.turns-=1
            if self.turns == 0:
                self.done = True
                self.anim.append_log(f"<{self.name}>状态解除了", self.pet.is_self)

class Burn(EffectBase):
    def __init__(self, pet, animator, rng, args):
        super(Burn, self).__init__(pet, animator, rng)
        self.name = "烧伤"

    def solve(self, secondary: BattlePet, skill_outcome):
        self.anim.animate_burn(self.pet)
        damage = self.pet.change_health(fraction=(-1, 8))
        self.anim.animate_number(self.pet, damage)
        super().solve(secondary)
        return True

class JiSheng(EffectBase):
    def __init__(self, pet, animator, rng, args):
        super().__init__(pet, animator, rng)
        self.name = "寄生"

    def solve(self, secondary: BattlePet, skill_outcome):
        self.anim.animate_jisheng(self.pet)
        damage = self.pet.change_health(fraction=(-1, 8))
        self.anim.animate_number(self.pet, damage)
        secondary.change_health(-damage)
        self.anim.animate_heal(secondary, -damage)
        super().solve(secondary)
        return True

class Poison(EffectBase):
    def __init__(self, pet, animator, rng, args):
        super().__init__(pet, animator, rng)
        self.name = "中毒"

    def solve(self, secondary: BattlePet, skill_outcome):
        self.anim.animate_poison(self.pet)
        damage = self.pet.change_health(fraction=(-1, 8))
        self.anim.animate_number(self.pet, damage)
        super().solve(secondary)
        return True

class Sleep(EffectBase):
    def __init__(self, pet, animator, rng, args):
        super().__init__(pet, animator, rng)
        self.name = "催眠"
        self.is_post_effect = False
        self.immuned = self.pet.status.has('w')

    def solve(self, secondary: BattlePet, skill_outcome):
        self.anim.animate_sleep(self.pet)
        super().solve(secondary)
        return False

class ImmuneSleep(EffectBase):
    def __init__(self, pet, animator, rng, args):
        super().__init__(pet, animator, rng)
        self.name = "免疫催眠"
        self.turns = 5

    def solve(self, secondary: BattlePet, skill_outcome):
        super().solve(secondary)
        return True

class NextTurnAttack(EffectBase):
    def __init__(self, pet, animator, rng, args):
        super().__init__(pet, animator, rng)
        self.is_post_effect = False
        self.name = "下回合攻击"
        self.turns = 1
        self.skill = args

    def solve(self, secondary: BattlePet, skill_outcome):
        skill_outcome.attack(self.pet, secondary, self.skill, "", self.anim, self.rng, False)
        super().solve(secondary)
        return False

class SkillEffect:
    label2effect = {
        "b": Burn,
        "j": JiSheng,
        "p": Poison,
        "s": Sleep,
        "w": ImmuneSleep,
        "n": NextTurnAttack,
    }

    def get(label):
        return SkillEffect.label2effect.get(label)
