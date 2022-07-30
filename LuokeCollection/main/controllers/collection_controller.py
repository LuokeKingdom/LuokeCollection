from .controller import Controller


class CollectionController(Controller):
    def __init__(self, app, view):
        super(CollectionController, self).__init__(app, view)
        self.actions = {"pop": lambda: app.pop()}
