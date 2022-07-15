from .scenes.views.view import View
from .scenes.controllers.controller import Controller


class Scene:
    TABLE = {
        "basic": (View, Controller),
    }

    def __init__(self, scene_name, app):
        self.view = self.TABLE[scene_name][0](app.screen)
        self.controller = self.TABLE[scene_name][1](app, self.view)
