from LuokeCollection.main.utils import SkillInfo
from random import choice

skill_dictionary = {
}

#def attack(solver: ActionSolver, skill: SkillInfo, args: str):
class SkillEffect:
    def attack(solver, skill: SkillInfo, args: str):
        primary, secondary = solver.primary, solver.secondary
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
        solver.animate_attack(primary, secondary, damage)

    def potion(solver, skill: SkillInfo, args: str):
        heal_amount = (1+int(args)) * 50
        solver.primary.change_health(heal_amount)
        solver.animate_potion(heal_amount)