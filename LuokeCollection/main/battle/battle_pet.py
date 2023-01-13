from .pet_status import PetStatus


class BattlePet:
    def __init__(self, info, talent_map, skill_indices):
        self.level = int(talent_map["level"])
        self.is_self = False
        self.status = PetStatus()
        self.talent_map = talent_map
        self.info = info
        self.skill_indices = skill_indices
        self.number_display = None
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
        self.final_stat_map = {
            k: int(
                (self.init_stat_map[k] * 2 + v) * self.level // 100
                + ((self.level + 10) if k == "HP" else 5)
            )
            for k, v in self.init_stat_map.items()
        }
        self.max_health = self.final_stat_map["HP"]
        self.health = self.max_health
        self.current_stat_map = self.get_current_stats()

    def get_current_stats(self):
        return {
            k: int(
                v
                * (
                    1 + 0.5 * self.status.stat_buffs[k]
                    if self.status.stat_buffs[k] >= 0
                    else 1 / (1 + self.status.stat_buffs[k])
                )
            )
            for k, v in self.final_stat_map.items()
            if k != "HP"
        }

    def change_health(self, change):
        self.health = min(self.max_health, max(0, self.health + change))

    def __getattr__(self, name):
        return self.current_stat_map.get(name)
