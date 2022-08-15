from .controller import Controller


class CollectionController(Controller):
    def get_instance(*args, **kwargs):
        if __class__.INSTANCE is None:
            __class__.INSTANCE = __class__(*args, **kwargs)
        return __class__.INSTANCE

    def __init__(self, model, view):
        super(CollectionController, self).__init__(model, view)
        self.actions = {
            "close": lambda: model.close(),
            "next_page": lambda: model.next_page(),
            "previous_page": lambda: model.previous_page(),
        }
    
    def side_effect(self):
        self.model.set_page(1)
