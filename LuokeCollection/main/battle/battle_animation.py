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
        if self.done:
            return
        self.done = True
        self.display.change_text(str(self.text))


class KeyframeBase(BaseBattleAnimation):
    def __init__(self, data, display):
        super(KeyframeBase, self).__init__()
        self.display = display
        self.original = None
        self.data = data
        self.data.sort()
        self.index = 0
        self.end = len(data) - 1
        self.interval = self.data[-1][0]

    def update(self, delta_time):
        while self.index != self.end and self.data[self.index + 1][0] < self.timer:
            self.index += 1
        if super(KeyframeBase, self).update(delta_time):
            self.set_change()
        else:
            self.end_change()

    def interpolate(self, get_val):
        t1, t2 = self.data[self.index][0], self.data[self.index + 1][0]
        progress = (self.timer - t1) / (t2 - t1)
        x1 = get_val(self.data[self.index][1])
        x2 = get_val(self.data[self.index + 1][1]) - x1
        return x1 + x2 * progress

    def set_change(self):
        raise Exception("<set_change> not implemented")

    def end_change(self):
        raise Exception("<end_change> not implemented")
    
class Position(KeyframeBase):
    def __init__(self, data, display):
        super(Position, self).__init__(data, display)
        self.original = self.display.get_pos()
    
    def set_change(self):
        cx = self.interpolate(lambda x: x[0])
        cy = self.interpolate(lambda x: x[1])
        ox, oy = self.original
        self.display.set_pos(ox + cx, oy + cy)

    def end_change(self):
        ox, oy = self.original
        self.display.set_pos(
            ox + self.data[self.end][1][0],
            oy + self.data[self.end][1][1],
        )

class Scale(KeyframeBase):
    def __init__(self, data, display):
        super(Scale, self).__init__(data, display)
        self.original = 1
        self.display = display
        self.ox, self.oy = display.get_pos()
    
    def set_change(self):
        cx = self.interpolate(lambda x: x)
        ox = self.original
        oi = self.display.original_image
        self.display.set_temp_image(oi, ratio=ox+cx).set_pos(self.ox, self.oy)

    def end_change(self):
        oi = self.display.original_image
        self.display.set_temp_image(oi, ratio=self.original+self.data[-1][1]).set_pos(self.ox, self.oy)

class StuffChange(BaseBattleAnimation):
    def __init__(self, on_update, stuff):
        super(StuffChange, self).__init__()
        self.on_update = on_update
        self.stuff = stuff

    def update(self, delta_time):
        if self.done:
            return
        self.on_update(self.stuff)
        self.done = True


# exposure
class BattleAnimation:
    animations = {
        "none": NoAnimation,
        "text": TextDisplay,
        "text_change": TextChange,
        "position": Position,
        "scale": Scale,
        "stuff_change": StuffChange,
    }

    def get(name, **kwargs):
        return BattleAnimation.animations[name](**kwargs)
