from .battle_pet import BattlePet
from .animator import Animator


class EffectBase:
    def __init__(self, pet: BattlePet, animator: Animator):
        self.turns = 0
        self.pet = pet
        self.anim = animator
        self.is_post_effect = True

    def solve(self): 
        raise Exception("<solve> not implemented")

class Burn(EffectBase):
    def __init__(self, pet, animator):
        super().__init__(pet, animator)
    
    def solve(self):
        self.anim.animate_burn(self.pet)
        self.pet.change_health(fraction=(1, 8))
        return True


class SkillEffect:
    label2effect = {
        'b': Burn,
    }
    def get(label):
        return SkillEffect.label2effect.get(label)
