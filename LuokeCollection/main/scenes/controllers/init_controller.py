from .controller import Controller


class InitController(Controller):
    def __init__(self, app, view):
        super(InitController, self).__init__(app, view)
        self.actions = {"collection": lambda: app.push_scene("basic")}
