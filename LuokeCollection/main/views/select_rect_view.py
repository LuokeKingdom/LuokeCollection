import pygame
from pygame.locals import *
from .view import View
from ..components.button import Button
from ..components.container import Container
from ..components.text import Text
from settings.dev import WIDTH, HEIGHT, IMAGE

EMPTY = pygame.Surface([1, 1])

class SelectRectView(View):
    def get_instance(*args, **kwargs):
        if __class__.INSTANCE is None:
            __class__.INSTANCE = __class__(*args, **kwargs)
        return __class__.INSTANCE

    BUTTONS = {
        "close": Button(x=1100, y=70),
        "save": Button(x=1100, y=700),
    }
    OTHERS = {
        'image':Container(
            image=EMPTY,
            align_mode='TOPLEFT',
        )
    }
    def __init__(self, *args, **kwargs):
        kwargs["bg"] = pygame.Surface([1,1])
        kwargs["bg"].fill((200,200,245))
        super(SelectRectView, self).__init__(*args, **kwargs)

    def set_pet_image(self, image):
        self.OTHERS['image'].set_image(image, height=int(HEIGHT*0.9))

    def display(self, mouse_pos, clicked):
        super().display(mouse_pos, clicked)
        pygame.draw.rect(self.screen, (0,0,0),pygame.Rect(mouse_pos.x, mouse_pos.y, 200,200), 2)

    def update(self, mouse_pos, clicked):
        super().update(mouse_pos, clicked)