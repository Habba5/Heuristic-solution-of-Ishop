from Controller.controller import *
from Enum.Location import *
from Enum.SellerRating import *
from Enum.Language import *
from Enum.Condition import *


class ControllerCardListing(Controller):
    def __init__(self, model, view):
        super().__init__(model, view)
        self.expansions = []
        for card in self.model.deck:
            self.expansions.append(["Egal"])

    def getSellerRating(self):
        return self.model.sellerrating

    def getLocation(self):
        return self.model.location

    def getDeck(self):
        return self.model.deck

    def update(self):
        self.view.cardamount = []
        self.view.choiceslanguage = {}
        self.view.choicescondition = {}
        self.view.view()

    def updateModelLanguage(self, i, language):
        self.model.deck[i][3] = language
        print("Updated Language of card" + self.model.deck[i][1] + " to " + self.model.deck[i][3])

    def updateModelLocation(self, location):
        self.model.location = Location[location]
        print(self.model.location.name)

    def updateModelRating(self, rating):
        self.model.sellerrating = SellerRating[rating]
        print(self.model.sellerrating.name)

    def updateModelCardLanguage(self, i, choice, language):
        #print(self.model.deck[i].cardlanguage)
        if(language == 0):
            self.model.deck[i].cardlanguage.remove(Language[choice])
        else:
            self.model.deck[i].cardlanguage.append(Language[choice])
        #print(self.model.deck[i].cardlanguage)

    def updateModelCardCondition(self, i, choice, condition):
        print(self.model.deck[i].cardcondition)
        if(condition == 0):
            self.model.deck[i].cardcondition.remove(Condition[choice])
        else:
            self.model.deck[i].cardcondition.append(Condition[choice])
        print(self.model.deck[i].cardcondition)

    def updateModelCardExpansion(self, i, choice, expansion):
        #print(self.model.deck[i].cardcondition)
        if(expansion == 0):
            self.expansions[i].remove(choice)
        else:
            if choice != "Egal":
                self.expansions[i].append(choice)
            else:
                self.expansions[i] = ["Egal"]
            #self.model.deck[i].cardcondition.append(Condition[choice])
        print(self.expansions[i])


    def updateModel(self, i, count):
        if(count == '0'):
            delcard = self.model.deck.pop(i)
            self.update()
            print("Card " + delcard.cardname + "deleted")
        else:
            self.model.deck[i].cardamount = count
            print("Updated card count at index" + str(i) + "to count" + str(count))

    def calculate(self):
        i = 0
        for expansion in self.expansions:
            self.model.deck[i].expansions = expansion
            i += 1
        self.view.clear_frame()