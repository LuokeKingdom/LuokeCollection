from .controller import Controller


class InitController(Controller):
    def __init__(self, model, view):
        super(InitController, self).__init__(model, view)
        def f(s): return lambda: model.open(s)
        options = [
            "collection",
            "select_rect",
        ]
        self.actions = {}
        for option in options: self.actions[option] = f(option)
            
            
