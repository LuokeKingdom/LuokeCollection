class Controller:
    def __init__(self, model, view):
        self.view = view
        self.model = model
        self.actions = {
            "pop": lambda: self.model.close(),
        }
        pass

    def link(self):
        for name, action in self.actions.items():
            self.view.BUTTONS[name].on_click = action

    def side_effect(self):
        pass
