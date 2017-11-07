from Controller.controller import *
from View.viewCardListing import *


class ControllerCardListing(Controller):
    def __init__(self, model):
        view = ViewCardListing()
        super().__init__(model, view)

    def update(self):
        self.view.sva = []
        self.view.view(self.model.deck)

    def updateModel(self, i, count):
        if(count == '0'):
            self.model.deck.pop(i)
            self.update()
            print("JOJO dadadadadaddannn")
        else:
            self.model.deck[i][0] = count
            print("Dicke Moooooes" + count)