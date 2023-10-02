from LuokeCollection.main.utils import str2element
from .skill_dictionary import skill_dictionary
from .skill_outcome import SkillOutcome
from .animator import Animator
from .rng import rng


class ActionSolver:
    def __init__(self, action_index, user, taker):
        self.primary = user
        self.secondary = taker
        self.action_index = action_index
        self.skill_outcomes = {
            k: SkillOutcome.__dict__.get(v)
            for k, v in SkillOutcome.labels2function.items()
        }
        self.anim = None
        self.rng = None

    def solve(self, animator: Animator, rng: rng):
        self.anim = animator
        self.rng = rng
        index = self.action_index
        if index < 4:
            if self.primary.health == 0 or self.secondary.health == 0:
                return
            self.use_skill(index)
        elif index - 10 < 6:
            if self.primary.is_self:
                animator.system.current_pet1 = index - 10
            else:
                animator.system.current_pet2 = index - 10
            self.anim.animate_change_pet(self.primary, index - 10)
        elif index - 100 < 6:
            self.skill_outcomes.get(".")(
                self.primary, self.secondary, None, str(index - 100), animator, rng, False
            )

    def use_skill(self, skill_index):
        skill = self.primary.skills[skill_index]
        self.anim.append_log(f"使用了<{skill.name}>", self.primary.is_self)
        if self.primary.status.has('c'):
            if self.rng.get()<0.5:
                self.anim.append_log("混乱了", self.primary.is_self)
                self.secondary = self.primary
        skill_element = str2element(skill.type)
        if skill_element:
            pass
        labels = skill_dictionary.get(skill.name,"").split(" ")
        if len(labels)==0:
            raise Exception("Skill not found in dictionary")

        accuracy_rate = int(labels[0])
        missed = accuracy_rate!=0 and self.rng.get() * 100 > accuracy_rate
        skill_arg = skill
        for label in labels[1:]:
            identifier = label[0]
            args = label[1:]
            self.skill_outcomes.get(identifier)(
                self.primary, self.secondary, skill_arg, args, self.anim, self.rng, missed
            )
            skill_arg = None

