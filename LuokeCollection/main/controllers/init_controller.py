from .controller import Controller


class InitController(Controller):
    def __init__(self, model, view):
        super(InitController, self).__init__(model, view)
        options = [
            "collection",
            "select_rect",
        ]
        self.actions = {option:lambda: model.open(option) for option in options}
