from LuokeCollection.main.scene.scene import Scene
from ..components.button import Button
from ..components.text import Text
from ..model.sound import Channel
from LuokeCollection.settings.dev import SOUND, WIDTH, HEIGHT, IMAGE


class BattlePrepScene(Scene):
    def __init__(self, screen, model, *args, **kwargs):
        kwargs["bg"] = IMAGE("skill_temp.png")
        super(BattlePrepScene, self).__init__(screen, model, *args, **kwargs)
        self.background_music = SOUND("castle.wav", Channel.BACKGROUND)
        self.BUTTONS = {
            "pop": Button(
                text="X",
                x=1000,
                y=100,
                on_click=lambda: model.close()
            ),
            "train": Button(
                image=IMAGE("battle.png"),
                x=1020,
                y=600,
                on_click=lambda: self.model.open("training"),
                width=100,
                animation="opacity",
                parameter={"factor": 0.4},
            ),
            "battle": Button(
                image=IMAGE("battle.png"),
                on_click=lambda: self.model.open("battle"),
                x=1100,
                y=600,
                width=100,
                animation="opacity",
                parameter={"factor": 0.4},
            )
        }
        self.OTHERS = {
        }
        self.init_pets()

    def side_effect(self):
        super().side_effect()
    
    def init_pets(self):
        for i in range(6):
            self.BUTTONS[f"pet_container_{i}"] = Button("opacity", text="", x=200+i*150, y = 250)
            self.TEXTS[f"pet_name_{i}"] = Text("ac", x=200 + i*150, y=250, align_mode="CENTER")

    
    def pet_circle(self, id, name, x, y):
        self.BUTTONS[f"pet_container_{id}"] = Button("opacity",image=IMAGE("placeholder.png"),width=100,x=x,y=y)
        self.TEXTS[f"pet_name_{id}"] = Text(name,x=x,y=y)

    def set_info(self, pet):
        pass
