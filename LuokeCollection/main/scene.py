from .views.view import View
from .controllers.controller import Controller
from .views.init_view import InitView
from .controllers.init_controller import InitController


class Scene:
    TABLE = {
        "basic": (View, Controller),
        "init": (InitView, InitController),
    }

    def __init__(self, scene_name, app):
        self.view = self.TABLE[scene_name][0](app.screen)
        self.view.load_items()
        self.controller = self.TABLE[scene_name][1](app, self.view)
        self.controller.link()
