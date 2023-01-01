from LuokeCollection.main.scene.scene import Scene
from ..components.button import Button
from ..components.text import Text
from ..model.sound import Channel
from LuokeCollection.settings.dev import SOUND, WIDTH, HEIGHT, IMAGE


class BattleScene(Scene):
    def __init__(self, screen, model, *args, **kwargs):
        kwargs["bg"] = IMAGE("skill_temp.png")
        super(BattleScene, self).__init__(screen, model, *args, **kwargs)
        self.background_music = SOUND("castle.wav", Channel.BACKGROUND)
        self.BUTTONS = {
            "pop": Button(
                text="X",
                x=1000,
                y=100,
                on_click=lambda: model.close()
            ),
            
        }
        self.OTHERS = {
        }

    def side_effect(self):
        super().side_effect()
    