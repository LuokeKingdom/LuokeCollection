from LuokeCollection.main.scene.scene import Scene
from pygame.locals import *
from ..components.button import Button
from ..components.text import Text
from settings.dev import WIDTH, HEIGHT, IMAGE


class InitScene(Scene):
    def __init__(self, screen, model, *args, **kwargs):
        kwargs["bg"] = IMAGE("init_bg.jpg")
        super(InitScene, self).__init__(screen, model, *args, **kwargs)
        self.BUTTONS = {
            "collection": Button(
                image=IMAGE("collection_button.png"),
                x=WIDTH / 5,
                y=HEIGHT / 2,
                on_click=lambda: model.open("collection"),
            ),
            "select_rect": Button(
                x=WIDTH / 5,
                y=HEIGHT / 2 + 100,
                on_click=lambda: model.open("select_rect"),
            ),
        }

        self.OTHERS = {}