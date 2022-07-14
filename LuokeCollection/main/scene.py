from .scenes.views.view import View
from .scenes.controllers.controller import Controller


class Scene:
    VIEWS = {
        "basic": View,
    }

    CONTROLLERS = {
        "basic": Controller,
    }

    def __init__(self, scene_name, app):
        self.view = self.VIEWS[scene_name]()
        self.controller = self.CONTROLLERS[scene_name](app, self.view)

    def display(self):
        self.view.display()

    def update(self):
        self.controller.update()
