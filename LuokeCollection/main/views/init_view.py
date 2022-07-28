import pygame
from pygame.locals import *
from .view import View
from ..components.button import Button
from ..components.text import Text
from settings.dev import WIDTH, HEIGHT, IMAGE


class InitView(View):
    BUTTONS = {
        "collection": Button(
            image=IMAGE("collection_button.png"),
            x=WIDTH / 5,
            y=HEIGHT / 2,
        )
    }

    OTHERS = {"test": Text()}

    def __init__(self, *args, **kwargs):
        kwargs["bg"] = IMAGE("init_bg.jpg")
        super(InitView, self).__init__(*args, **kwargs)
