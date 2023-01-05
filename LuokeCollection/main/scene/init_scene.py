from LuokeCollection.main.scene.scene import Scene
from ..components.button import Button
from ..model.sound import Channel
from LuokeCollection.settings.dev import SOUND, WIDTH, HEIGHT, IMAGE


class InitScene(Scene):
    def __init__(self, screen, model, *args, **kwargs):
        super(InitScene, self).__init__(screen, model,'init_bg.jpg', *args, **kwargs)
        self.background_music = SOUND("castle.wav", Channel.BACKGROUND)
        self.BUTTONS = {
            "collection": Button(
                image=IMAGE("collection_button.png"),
                x=WIDTH / 5,
                y=HEIGHT / 2,
                on_click=lambda: model.open("collection"),
            ),
            "battle": Button(
                text="战斗",
                x=WIDTH / 5,
                y=HEIGHT / 2 + 100,
                on_click=lambda: model.open("battle_prep"),
            ),
        }
        self.OTHERS = {}
