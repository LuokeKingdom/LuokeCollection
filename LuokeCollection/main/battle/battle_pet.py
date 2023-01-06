class BattlePet:
    def __init__(self, info, talent_map, skill_indices):
        self.level = talent_map["level"]
        self.talent_map = talent_map
        self.info = info
        self.skill_indices = skill_indices
        self.HP = 0
        self.AD = 0
        self.DF = 0
        self.AP = 0
        self.MD = 0
        self.SP = 0
    pass
