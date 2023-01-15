class PetStatus:
    def __init__(self, skill_PPs=[[0, 0] for i in range(4)]):
        stat_names = ["AD", "AP", "DF", "MD", "SP", "AR", "ER",]
        self.stat_buffs = {i:self.Level() for i in stat_names}
        self.skill_PPs = skill_PPs
        self.pre_effects = {}
        self.post_effects = {}

    def __getattr__(self, name):
        return self.stat_buffs.get(name)

    class Level:
        def __init__(self):
            self.level = 0

        def change(self, diff):
            self.level = int(max(-6, min(6, self.level + diff)))

        def clear(self):
            self.level = 0

        def __int__(self):
            return self.level

        def __getattr__(self, name):
            if name == "factor":
                return self.level/2 + 1 if self.level >= 0 else 1 / (1 - self.level/2)
