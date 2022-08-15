import pygame
from pygame.locals import *
from .view import View
from ..components.button import Button
from ..components.text import Text
from settings.dev import WIDTH, HEIGHT, IMAGE


class SelectRectView(View):
    def __init__(self, *args, **kwargs):
        kwargs["bg"] = pygame.Surface([1,1])
        kwargs["bg"].fill((245,245,245))
        super(SelectRectView, self).__init__(*args, **kwargs)