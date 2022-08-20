from pygame.locals import *
from .view import View
from ..components.button import Button
from ..components.text import Text
from settings.dev import WIDTH, HEIGHT, IMAGE


class InitView(View):
    def get_instance(*args, **kwargs):
        if __class__.INSTANCE is None:
            __class__.INSTANCE = __class__(*args, **kwargs)
        return __class__.INSTANCE

    BUTTONS = {
        "collection": Button(
            image=IMAGE("collection_button.png"),
            x=WIDTH / 5,
            y=HEIGHT / 2,
        ),
        "select_rect": Button(
            x=WIDTH / 5,
            y=HEIGHT / 2 + 100
        )
    }

    OTHERS = {}

    def __init__(self, *args, **kwargs):
        kwargs["bg"] = IMAGE("init_bg.jpg")
        super(InitView, self).__init__(*args, **kwargs)
