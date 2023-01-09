class BattlePet:
    def __init__(self, info, talent_map, skill_indices):
        self.level = talent_map["level"]
        self.is_self = False
        self.talent_map = talent_map
        self.info = info
        self.skill_indices = skill_indices
        self.damage_display = None
        self.health_display = None
        self.sprite_display = None
        self.skills = [self.info.skills[i] for i in skill_indices]
        self.init_stat_map = {
            "HP": int(info.stats[0]),
            "AD": int(info.stats[1]),
            "DF": int(info.stats[2]),
            "AP": int(info.stats[3]),
            "MD": int(info.stats[4]),
            "SP": int(info.stats[5]),
        }
        self.final_stat_map = {k:v for k, v in self.init_stat_map.items()}
        self.recalculate()
        self.health = self.final_stat_map["HP"]

    def recalculate(self):
        for k, v in self.talent_map.items():
            if k != "level":
                self.final_stat_map[k] = (self.init_stat_map[k] * 2 + v) * self.level // 100 + (
                    (self.level + 10) if k == "HP" else 5
                )
                
    def __getattr__(self, name):
        return self.final_stat_map.get(name)