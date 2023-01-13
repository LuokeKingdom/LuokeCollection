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
    def __init__(self, interval):
        super(NoAnimation, self).__init__()
        self.interval = interval


class TextDisplay(BaseBattleAnimation):
    def __init__(self, text, display, color=None, interval=1):
        super(TextDisplay, self).__init__()
        self.interval = interval
        self.display = display
        self.text = text
        self.color = color
        if color is None:
            self.color = display.color

    def update(self, delta_time):
        if self.timer == 0:
            self.display.change_text(str(self.text), self.color)
        if not super(TextDisplay, self).update(delta_time):
            self.display.change_text("")


class TextChange(BaseBattleAnimation):
    def __init__(self, text, display):
        super(TextChange, self).__init__()
        self.display = display
        self.text = text

    def update(self, delta_time):
        if self.done: return
        self.done = True
        self.display.change_text(str(self.text))


class KeyframePosition(BaseBattleAnimation):
    def __init__(self, data, display):
        super(KeyframePosition, self).__init__()
        self.display = display
        self.opx, self.opy = display.get_pos()

        self.data = data
        self.data.sort()
        self.index = 0
        self.end = len(data) - 1
        self.interval = self.data[-1][0]

    def update(self, delta_time):
        while self.index != self.end and self.data[self.index + 1][0] < self.timer:
            self.index += 1
        if not super(KeyframePosition, self).update(delta_time):
            self.display.set_pos(
                self.opx + self.data[self.end][1][0],
                self.opy + self.data[self.end][1][1],
            )
        else:
            t1, t2 = self.data[self.index][0], self.data[self.index + 1][0]
            progress = (self.timer - t1) / (t2 - t1)
            x1 = self.data[self.index][1][0]
            x2 = self.data[self.index + 1][1][0] - x1
            y1 = self.data[self.index][1][1]
            y2 = self.data[self.index + 1][1][1] - y1
            self.display.set_pos(
                self.opx + x1 + x2 * progress, self.opy + y1 + y2 * progress
            )

class LogChange(BaseBattleAnimation):
    def __init__(self, on_update, text):
        super(LogChange, self).__init__()
        self.on_update = on_update
        self.text = text

    def update(self, delta_time):
        if self.done: return
        self.done = True
        self.on_update(self.text)

# exposure
class BattleAnimation:
    animations = {
        "none": NoAnimation,
        "text": TextDisplay,
        "text_change": TextChange,
        "position": KeyframePosition,
        "log": LogChange,
    }

    def get(name, **kwargs):
        return BattleAnimation.animations[name](**kwargs)
