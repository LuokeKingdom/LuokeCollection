from LuokeCollection.main.scene_factory import SceneFactory
from .model.model import Model


class App:
    def __init__(self, screen):
        self.scene = None
        self.stack = []
        self.screen = screen
        self.model = Model(self)
        self.factory = SceneFactory(self.screen, self.model)

    def create_scene(self, scene_name):
        return self.factory.get_scene(scene_name)

    def change_scene(self, scene_name):
        if self.stack:
            self.stack.pop()
        self.push_scene(scene_name)
        pass

    def push_scene(self, scene_name):
        self.scene = self.create_scene(scene_name)
        self.scene.side_effect()
        self.stack.append(self.scene)

    def pop_scene(self):
        self.stack.pop()
        if self.stack:
            self.scene = self.stack[len(self.stack) - 1]

    def display(self, mouse_pos, clicked):
        self.scene.display(mouse_pos, clicked)

    def update(self, mouse_pos, clicked):
        self.scene.update(mouse_pos, clicked)
