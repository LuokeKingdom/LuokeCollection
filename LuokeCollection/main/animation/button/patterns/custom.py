from ...mixin import Mixin


class CustomMixin(Mixin):
    def effect(self, current_time):
        if self.done:
            return
        self.on_hover()
        self.done = True

    def reset(self):
        if not self.done:
            return
        self.not_hover()
        self.done = False
