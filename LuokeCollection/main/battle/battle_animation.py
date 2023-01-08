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

class TextDisplayAnimation(BaseBattleAnimation):
    def __init__(self, text, display, interval):
        super(TextDisplayAnimation, self).__init__()
        self.interval = interval
        self.display = display
        self.text = text

    def update(self, delta_time):
        if self.timer==0:
            self.display.change_text(str(self.text))
        if not super(TextDisplayAnimation, self).update(delta_time):
            self.display.change_text("")

class TextChangeAnimation(BaseBattleAnimation):
    def __init__(self, text, display):
        super(TextChangeAnimation, self).__init__()
        self.display = display
        self.text = text

    def update(self, delta_time):
        self.done = True
        self.display.change_text(str(self.text))

# exposure
class BattleAnimation:
    animations = {
        "none": NoAnimation,
        "text": TextDisplayAnimation,
        "text_change": TextChangeAnimation,
    }
    def get(name, **kwargs):
        return BattleAnimation.animations[name](**kwargs)
        