

class Controller(object):
    def __init__(self, model, view):
        self.model = model
        self.view = view

        self.view.register(self)
        self.update()

    def update(self):
        self.view.view()
