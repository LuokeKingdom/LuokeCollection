from .controller import Controller


class InitController(Controller):
    def __init__(self, model, view):
        super(InitController, self).__init__(model, view)
        self.actions = {"collection": lambda: model.open("collection")}
