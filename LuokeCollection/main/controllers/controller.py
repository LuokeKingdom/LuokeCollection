class Controller:
    INSTANCE = None
    def get_instance(*args, **kwargs):
        if __class__.INSTANCE is None:
            __class__.INSTANCE = __class__(*args, **kwargs)
        return __class__.INSTANCE

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
