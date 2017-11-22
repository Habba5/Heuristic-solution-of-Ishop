from Model.model import *
from Enum.Location import *
from Enum.SellerRating import *
from objects.card import *

class ModelDeck(Model):

    def __init__(self):
        self.deck = []
        self.location = Location.Deutschland
        self.sellerrating = SellerRating.Guter
        super().__init__()

    def deck(self):
        return self.deck

    def printdeck(self):
        if self.deck:
            for card in self.deck:
                print(card.cardamount + " " + card.cardname + " " + card.cardurl)
                for language in card.cardlanguage:
                    print(language)
                for condition in card.cardcondition:
                    print(condition)

    def searchcard(self, cardname):
        if not self.deck:
            for card in self.deck:
                if card.cardname == cardname:
                    return 1
        return 0

    def addcard(self, cardamount, cardname, cardurl):
        if self.searchcard(cardname) == 0:
            self.deck.append(Card(cardamount, cardname, cardurl))
            return 1
        else:
            return 0

    def location(self):
        return self.location

    def sellerrating(self):
        return self.sellerrating