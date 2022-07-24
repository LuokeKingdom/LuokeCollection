from ..mixin import Mixin
from .patterns.opacity import OpacityMixin


class ButtonAnimation:
    def __init__(self, button, transition=None):
        self.button = button
        self.startTime = 0
        self.is_playing = False
        self.transition = transition
    
    def update(self, current_time):
        if not self.is_playing: return 
        for cls in self.__class__.__mro__:
            if issubclass(cls, Mixin): 
                cls.effect(self, current_time)

    def play(self, start_time):
        if self.is_playing: return
        self.is_playing = True
        self.start_time = start_time 
    
    def stop(self):
        self.is_playing = False
        self.reset()

class OpacityButtonAnimation(
    ButtonAnimation,
    OpacityMixin
):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.opacity = 0.5
