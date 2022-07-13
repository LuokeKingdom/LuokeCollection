class App:
    def __init__(self):
        self.scene = None
        self.stack = []

    def change_scene(self, scene):
        if self.stack:
            self.stack.pop()
        self.push_scene(scene)
        pass

    def push_scene(self, scene):
        self.scene = scene
        self.stack.append(scene)

    def pop_scene(self):
        self.stack.pop()
        if self.stack:
            self.scene = self.stack[len(self.stack) - 1]

    def display(self):
        self.scene.display()

    def update(self):
        self.scene.update()
