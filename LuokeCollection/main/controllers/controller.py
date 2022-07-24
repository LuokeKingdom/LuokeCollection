class Controller:
    def __init__(self, app, view):
        self.view = view
        self.actions = {
            "pop": lambda: app.pop_scene(),
        }
        pass

    def link(self):
        for name, action in self.actions.items():
            self.view.BUTTONS[name].on_click = action