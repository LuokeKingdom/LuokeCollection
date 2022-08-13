from .scene import Scene
from .model.model import Model


class App:
    def __init__(self, screen):
        self.scene = None
        self.stack = []
        self.screen = screen
        self.model = Model()

    def create_scene(self, scene_name):
        return Scene(scene_name, self)

    def change_scene(self, scene_name):
        if self.stack:
            self.stack.pop()
        self.push_scene(scene_name)
        pass

    def push_scene(self, scene_name):
        self.scene = self.create_scene(scene_name)
        self.stack.append(self.scene)

    def pop_scene(self):
        self.stack.pop()
        if self.stack:
            self.scene = self.stack[len(self.stack) - 1]

    def display(self, mouse_pos, clicked):
        self.scene.view.display(mouse_pos, clicked)

    def update(self, mouse_pos, clicked):
        self.scene.view.update(mouse_pos, clicked)
