from .controller import Controller


class SelectRectController(Controller):
    def get_instance(*args, **kwargs):
        if __class__.INSTANCE is None:
            __class__.INSTANCE = __class__(*args, **kwargs)
        return __class__.INSTANCE

    def __init__(self, model, view):
        super(SelectRectController, self).__init__(model, view)
        self.actions = {
            "close": lambda: model.close(),
        }

    def side_effect(self):
        self.model.set_pet_select_rect(1)
