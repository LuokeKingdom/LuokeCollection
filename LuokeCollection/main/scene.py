from .scenes.views.view import View
from .scenes.controllers.controller import Controller


class Scene:
    VIEWS = {
        'basic': View,
    }

    CONTROLLERS = {
        'basic': Controller,
    }

    def __init__(self, scene_name=None):
        self.view = self.VIEWS.get(scene_name)
        self.controller = self.CONTROLLERS.get(scene_name)
        print("scene!!!!!")

    def display(self):
        self.view.display()

    def update(self):
        self.controller.update(self.view)