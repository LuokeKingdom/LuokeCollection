from tkinter import CENTER
from ..mixin import Mixin
from .patterns.opacity import OpacityMixin
from .patterns.scale import ScaleMixin
from .patterns.jump import JumpMixin
from .patterns.rotate import RotateMixin


class ButtonAnimation:
    def __init__(self, button, transition=None):
        self.button = button
        self.startTime = 0
        self.is_playing = False
        self.transition = transition

    def update(self, current_time):
        if not self.is_playing:
            return
        for cls in self.__class__.__mro__:
            if issubclass(cls, Mixin):
                cls.effect(self, current_time)

    def play(self, start_time):
        if self.is_playing:
            return
        self.is_playing = True
        self.start_time = start_time

    def stop(self):
        self.is_playing = False
        self.reset()


class OpacityButtonAnimation(ButtonAnimation, OpacityMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.opacity = 0.5


class ScaleButtonAnimation(ButtonAnimation, ScaleMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.transition = 0.15
        self.scale = 0.8
        self.w, self.h = self.button.image.get_size()


class JumpButtonAnimation(ButtonAnimation, JumpMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.button.align_mode = "TOPLEFT"
        self.transition = 1
        self.jump_height = 25
        self.a = self.jump_height / (self.transition / 2) / (self.transition / 2)
        self.w, self.h = self.button.image.get_size()
        self.x, self.y = self.button.get_pos()
        self.y_temp = self.y
        print(self.a)

class RotateButtonAnimation(ButtonAnimation, RotateMixin):
    def __int__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
