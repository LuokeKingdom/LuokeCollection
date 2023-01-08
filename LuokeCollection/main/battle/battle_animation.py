class BaseBattleAnimation:
    def __init__(self):
        self.timer = 0
        self.interval = 0
        self.done = False
        pass

    def update(self, delta_time):
        self.timer += delta_time
        if self.timer > self.interval:
            self.done = True
            return False
        return True


class NoAnimation(BaseBattleAnimation):
    def __init__(self, pet, interval):
        super(NoAnimation, self).__init__()
        self.interval = interval

class DamageAnimation(BaseBattleAnimation):
    def __init__(self, damage, pet, interval):
        super(DamageAnimation, self).__init__()
        self.interval = interval
        self.display = pet.display
        self.damage = damage

    def update(self, delta_time):
        if self.timer==0:
            self.display.change_text(str(self.damage))
        if not super(DamageAnimation, self).update(delta_time):
            self.display.change_text("")


# exposure
class BattleAnimation:
    animations = {
        "none": NoAnimation,
        "damage": DamageAnimation,
    }
    def get(name, **kwargs):
        return BattleAnimation.animations[name](**kwargs)
        