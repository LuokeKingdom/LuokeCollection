class PetStatus:
    def __init__(self, skill_PPs=[[0, 0] for i in range(4)]):
        stat_names = ["AD", "AP", "DF", "MD", "SP", "AR", "ER", "CR"]
        self.stat_buffs = {
            i: self.Level(6) if i != "CR" else self.Level(2) for i in stat_names
        }
        self.skill_PPs = skill_PPs
        self.pre_effects = {}
        self.post_effects = {}

    def __getattr__(self, name):
        return self.stat_buffs.get(name)

    class Level:
        def __init__(self, limit):
            self.level = 0
            self.max_level = limit
            self.min_level = -limit

        def change(self, diff):
            self.level = int(
                max(-self.min_level, min(self.max_level, self.level + diff))
            )

        def clear(self):
            self.level = 0

        def __int__(self):
            return self.level

        def __getattr__(self, name):
            if name == "factor":
                return (
                    self.level / 2 + 1 if self.level >= 0 else 1 / (1 - self.level / 2)
                )
