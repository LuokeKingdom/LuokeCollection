class Controller:
    def __init__(self, app, view):
        self.view = view

        self.actions = {
            'test_button': lambda : print("test button clicked!!")
        }
        self.link()
        pass

    def link(self):
        for name, action in self.actions.items():
            self.view.BUTTONS[name].on_click = action

