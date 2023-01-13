from LuokeCollection.main.scene.training_scene import TrainingScene
from .scene.splash_scene import SplashScene
from .scene.init_scene import InitScene
from .scene.collection_scene import CollectionScene
from .scene.select_rect_scene import SelectRectScene
from .scene.battle_prep_scene import BattlePrepScene
from .scene.battle_scene import BattleScene
from .scene.pet_position_select_scene import PetPositionSelectScene


class SceneFactory:
    def __init__(self, screen, model):
        init = InitScene(screen, model)
        splash = SplashScene(screen, model)
        collection = CollectionScene(screen, model)
        select_rect = SelectRectScene(screen, model)
        training = TrainingScene(screen, model)
        battle_prep = BattlePrepScene(screen, model)
        battle = BattleScene(screen, model)
        pet_position_select = PetPositionSelectScene(screen, model)
        self.scenes = {
            "splash": splash,
            "init": init,
            "collection": collection,
            "select_rect": select_rect,
            "training": training,
            "battle_prep": battle_prep,
            "battle": battle,
            "pet_position_select": pet_position_select,
        }

    def get_scene(self, name):
        return self.scenes[name]
