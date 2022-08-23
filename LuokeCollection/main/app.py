from LuokeCollection.main.scene_factory import SceneFactory
from .model.model import Model


class App:
    def __init__(self, screen):
        self.scene = None
        self.pop_up = None
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
        self.on_scene_change()
        self.scene.side_effect()
        self.stack.append(self.scene)

    def pop_scene(self):
        self.stack.pop()
        if self.stack:
            self.scene = self.stack[len(self.stack) - 1]
            self.on_scene_change()

    def open_pop_up(self, scene_name):
        self.pop_up = self.create_scene(scene_name)
        self.pop_up.side_effect()

    def close_pop_up(self):
        self.pop_up = None

    def display(self, mouse_pos, clicked):
        if self.pop_up is not None:
            self.pop_up.display(mouse_pos, clicked)
        else:
            self.scene.display(mouse_pos, clicked)

    def update(self, mouse_pos, clicked):
        if self.pop_up is not None:
            self.pop_up.update(mouse_pos, clicked)
        else:
            self.scene.update(mouse_pos, clicked)

    def on_scene_change(self):
        if self.scene.background_music is not None:
            self.scene.background_music.play()
