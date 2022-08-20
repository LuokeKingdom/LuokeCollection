from .scene.init_scene import InitScene
from .scene.collection_scene import CollectionScene
from .scene.select_rect_scene import SelectRectScene
class SceneFactory:
    def __init__(self, screen, model):
        self.scenes = {
            "init": InitScene(screen, model),
            "collection":CollectionScene(screen, model),
            "select_rect":SelectRectScene(screen, model),
        }
        
    def get_scene(self, name):
        return self.scenes[name]
        