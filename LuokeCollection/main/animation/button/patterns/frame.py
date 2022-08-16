from ...mixin import Mixin
from pygame.locals import *
from settings.dev import IMAGE


class FrameMixin(Mixin):
    def effect(self, current_time):
        self.frame_image = IMAGE(self.parameter + str(self.current_frame) + ".png")
        self.button.image = self.frame_image
        if self.current_frame < self.transition:
            self.current_frame += 1

    def reset(self):
        self.button.image = self.button.original_image
        self.current_frame = 1
