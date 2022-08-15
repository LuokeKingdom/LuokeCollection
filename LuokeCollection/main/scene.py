from .controllers.select_rect_controller import SelectRectController
from .views.select_rect_view import SelectRectView
from .views.view import View
from .controllers.controller import Controller
from .views.init_view import InitView
from .controllers.init_controller import InitController
from .views.collection_view import CollectionView
from .controllers.collection_controller import CollectionController


class Scene:
    TABLE = {
        "basic": (View, Controller),
        "init": (InitView, InitController),
        "collection": (CollectionView, CollectionController),
        "select_rect": (SelectRectView, SelectRectController),
    }

    def __init__(self, scene_name, app):
        self.view = self.TABLE[scene_name][0](app.screen)
        self.controller = self.TABLE[scene_name][1](app.model, self.view)

    def side_effect(self):
        """this will be called after Scene is initialized"""
        self.view.load_items()
        self.controller.link()
        self.controller.side_effect()
