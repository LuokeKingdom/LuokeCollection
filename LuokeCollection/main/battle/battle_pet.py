from LuokeCollection.settings.dev import IMAGE
from .pet_status import PetStatus
import os
import pygame
from pygame.locals import *  # noqa


class BattlePet:
    def __init__(self, info, talent_map, skill_indices):
        self.level = int(talent_map["level"])
        self.is_self = False
        self.status = PetStatus()
        self.talent_map = talent_map
        self.info = info
        self.image = None
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
            for k, v in self.talent_map.items()
            if k != "level"
        }
        self.max_health = self.final_stat_map["HP"]
        self.health = self.max_health
        self.current_stat_map = None
        self.update_current_stats()

    def update_current_stats(self):
        self.current_stat_map = {
            k: int(v * self.status.stat_buffs[k].factor)
            for k, v in self.final_stat_map.items()
            if k != "HP"
        }

    def change_health(self, change=None, fraction=None):
        if change is None:
            change = int(self.max_health * fraction[0] / fraction[1])
        self.health = min(self.max_health, max(0, self.health + change))
        return change

    def get_image(self):
        image = pygame.transform.flip(
            IMAGE(os.path.join("assets/data/", self.info.path, "display.png"), False),
            self.is_self,
            False,
        )
        max_width, max_height = 400, 600
        width, height = image.get_size()
        if height / max_height < width / max_width:
            return pygame.transform.smoothscale(
                image, (max_width, int(height * max_width / width))
            )
        else:
            return pygame.transform.smoothscale(
                image, (int(width * max_height / height, max_height))
            )

    def add_effect(self, label, effect):
        if effect.is_post_effect:
            self.status.post_effects[label] = effect
        else:
            self.status.pre_effects[label] = effect

    def trigger_pre_effects(self, secondary):
        if self.health == 0:
            return True
        flag = True
        for k, v in self.status.pre_effects.items():
            flag &= v.solve(secondary)
            if v.turns == 0:
                del self.status.pre_effects[k]
        return flag

    def trigger_post_effects(self, secondary):
        if self.health == 0:
            return
        for k, v in self.status.post_effects.items():
            v.solve(secondary)
            if v.turns == 0:
                del self.status.pre_effects[k]

    def __getattr__(self, name):
        return self.current_stat_map.get(name)
