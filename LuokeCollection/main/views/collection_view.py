import pygame
from pygame.locals import *
from .view import View
from ..components.button import Button
from ..components.text import Text
from ..components.sprite import Sprite
from settings.dev import WIDTH, HEIGHT, IMAGE


class CollectionView(View):
    BUTTONS = {}

    OTHERS = {}

    def __init__(self, *args, **kwargs):
        kwargs["bg"] = IMAGE("temp_bg.png")
        super(CollectionView, self).__init__(*args, **kwargs)
        new_buttons = {"pop": Button(x=1057, y=85)}
        new_others = {}
        info_compoments = {
            "pet_name": Text("Name",x=750,y=130),
            "pet_image": Sprite(IMAGE("display.png"),ratio=0.2,x=900,y=330),
            "pet_element": Sprite(IMAGE("place_holder.png"),x=700,y=130),
            "pet_id": Text("1"),
            "pet_description": Text("It is too lazy to leave anything.",x=700,y=200),
            "talent_icon_AD": Sprite(IMAGE("place_holder.png")),
            "talent_icon_AP": Sprite(IMAGE("place_holder.png")),
            "talent_icon_DF": Sprite(IMAGE("place_holder.png")),
            "talent_icon_MF": Sprite(IMAGE("place_holder.png")),
            "talent_icon_HP": Sprite(IMAGE("place_holder.png")),
            "talent_icon_SP": Sprite(IMAGE("place_holder.png")),
            "pet_talent_AD": Text("40"),
            "pet_talent_AP": Text("40"),
            "pet_talent_DF": Text("40"),
            "pet_talent_MF": Text("40"),
            "pet_talent_HP": Text("40"),
            "pet_talent_SP": Text("40"),
        }
        for name, comp in info_compoments.items():
            (new_buttons if comp is Button else new_others)[name] = comp
        for name, comp in new_buttons.items():
            self.BUTTONS[name] = comp
        for name, comp in new_others.items():
            self.OTHERS[name] = comp
