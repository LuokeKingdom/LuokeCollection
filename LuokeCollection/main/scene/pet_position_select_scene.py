from .scene import Scene
from ..components.button import Button
from LuokeCollection.settings.dev import IMAGE


class PetPositionSelectScene(Scene):
    def __init__(self, screen, model, *args, **kwargs):
        super(PetPositionSelectScene, self).__init__(
            screen, model, "white.png", width=800, height=200
        )
        self.BUTTONS["pop"] = Button(
            text="X", x=1030, y=300, on_click=lambda: self.model.close_pop_up()
        )

        def get_save_function(i):
            return lambda: self.model.save_pet_file(i)

        for i in range(6):
            self.BUTTONS[f"position_{i}"] = Button(
                image=IMAGE("place_holder.png"),
                x=294 + 130 * i,
                y=410,
                width=100,
                on_click=get_save_function(i),
            )
