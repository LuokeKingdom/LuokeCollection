from .controller import Controller


class InitController(Controller):
    def get_instance(*args, **kwargs):
        if __class__.INSTANCE is None:
            __class__.INSTANCE = __class__(*args, **kwargs)
        return __class__.INSTANCE

    def __init__(self, model, view):
        super(InitController, self).__init__(model, view)

        def f(s):
            return lambda: model.open(s)

        options = [
            "collection",
            "select_rect",
        ]
        self.actions = {}
        for option in options:
            self.actions[option] = f(option)

    def side_effect(self):
        pass
