class BaseBattleAnimation:
    def __init__(self, pet):
        self.timer = 0
        self.interval = 0
        self.pet = pet
        self.done = False
        pass

    def update(self, delta_time):
        self.timer += delta_time
        if self.timer > self.interval:
            self.done = True


class NoAnimation(BaseBattleAnimation):
    def __init__(self, pet, interval):
        super(NoAnimation, self).__init__(pet)
        self.interval = interval



# exposure
class BattleAnimation:
    animations = {
        "none": NoAnimation,
    }
    def get(name, pet, **kwargs):
        return BattleAnimation.animations[name](pet, **kwargs)
        