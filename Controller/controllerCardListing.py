from Controller.controller import *
from View.viewCardListing import *


class ControllerCardListing(Controller):
    def __init__(self, model):
        view = ViewCardListing()
        super().__init__(model, view)

    def update(self):
        self.view.sva = []
        self.view.variablelanguage = []
        self.view.variablecondition = []
        self.view.choices = []
        self.view.var = []
        self.view.view(self.model.deck)

    def updateModelLanguage(self, i, language):
        self.model.deck[i][3] = language
        print("Updated Language of card" + self.model.deck[i][1] + " to " + self.model.deck[i][3])

    def updateModel(self, i, count):
        if(count == '0'):
            delcard = self.model.deck.pop(i)
            self.update()
            print("Card " + delcard + "deleted")
        else:
            self.model.deck[i][0] = count
            print("Updated card count at index" + i + "to count" + count)