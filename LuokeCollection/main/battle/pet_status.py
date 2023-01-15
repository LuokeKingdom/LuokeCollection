class PetStatus:
    def __init__(self, skill_PPs=[[0, 0] for i in range(4)]):
        self.stat_buffs = {
            "AD": 0,
            "AP": 0,
            "DF": 0,
            "MD": 0,
            "SP": 0,
            "AR": 0,
            "ER": 0,
        }
        self.skill_PPs = skill_PPs
        self.effects = {}

    def __getattr__(self, name):
        return self.stat_buffs.get(name)
