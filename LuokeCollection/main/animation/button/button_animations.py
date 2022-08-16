from multiprocessing.spawn import old_main_modules
from pygame.locals import *
from tkinter import CENTER
from ..mixin import Mixin
from .patterns.opacity import OpacityMixin
from .patterns.scale import ScaleMixin
from .patterns.jump import JumpMixin
from .patterns.rotate import RotateMixin
from .patterns.frame import FrameMixin


class ButtonAnimation:
    def __init__(
        self,
        button,
        transition,
        parameter,
    ):
        self.button = button
        self.transition = transition
        self.parameter = parameter
        self.startTime = 0
        self.is_playing = False

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
        self.opacity = self.parameter


class ScaleButtonAnimation(ButtonAnimation, ScaleMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scale = self.parameter
        self.w, self.h = self.button.image.get_size()


class JumpButtonAnimation(ButtonAnimation, JumpMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.button.align_mode = "TOPLEFT"
        self.jump_height = self.parameter
        self.a = self.jump_height / (self.transition / 2) / (self.transition / 2)
        self.w, self.h = self.button.image.get_size()
        self.x, self.y = self.button.get_pos()
        self.y_temp = self.y
        self.angle = 0


class RotateButtonAnimation(ButtonAnimation, RotateMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.w, self.h = self.button.image.get_size()
        self.x, self.y = self.button.get_pos()
        self.rotation = self.parameter


class FrameButtonAnimation(ButtonAnimation, FrameMixin):
    def __int__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_frame = 1
