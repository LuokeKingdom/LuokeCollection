from ...mixin import Mixin


class OpacityMixin(Mixin):
    def effect(self, current_time):
        opacity = self.progress(current_time) * (self.end - self.start) + self.start
        self.button.image.set_alpha(255 * opacity)

    def reset(self):
        self.button.image.set_alpha(255 * self.start)
