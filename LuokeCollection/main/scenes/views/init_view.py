import pygame
from pygame.locals import *
from .view import View
from .components.button import Button
from settings.dev import WIDTH, HEIGHT


class InitView(View):
    BUTTONS = {
        "collection": Button(
            image=pygame.image.load(
                "LuokeCollection/assets/images/collection_button.png"
            ),
            x=WIDTH / 5,
            y=HEIGHT / 2,
        )
    }

    def __init__(self, *args, **kwargs):
        kwargs["bg"] = pygame.image.load("LuokeCollection/assets/images/init_bg.jpg")
        super(InitView, self).__init__(*args, **kwargs)
