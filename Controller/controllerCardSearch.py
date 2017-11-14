from Controller.controller import *
from View.viewCardSearch import *
#from Main import cardListing
import io
from requests import Session, head, codes


class ControllerCardSearch(Controller):
    def __init__(self, model):
        view = ViewCardSearch()
        super().__init__(model, view)

    def exists(self, path):
        r = head(path)
        return r.status_code == codes.ok

    def replace(self, string):
        string = string.replace(' ', '+')
        string = string.replace(',', '%2C')
        string = string.replace('//', '%2F')
        string = string.replace(':', '%3A')
        string = string.replace('\'', '%27')
        return string

    def searchCards(self, cards):
        buf = io.StringIO(cards)
        wrongcards = []
        listcard = []
        for line in buf:
            listcard.append(line.split(' ', 1))

        urlcardde='https://www.cardmarket.com/de/Magic/Cards/'
        urlcarden='https://www.cardmarket.com/en/Magic/Cards/'

        for card in listcard:
            card[1] = card[1].rstrip('\n')
            cardstring = self.replace(card[1])
            if(self.exists(urlcardde + cardstring)):
                card.append(urlcardde + cardstring)
            elif(self.exists(urlcarden + cardstring)):
                card.append(urlcarden + cardstring)
            else:
                wrongcards.append(card[1])
            card.append("Deutsch")
            card.append("Excellent")

        if not wrongcards:
            print("success")
            print(listcard)
            self.model.deck = listcard
        else:
            self.view.viewError("Die folgenden Karte/n konnte/n nicht gefunden werden :", wrongcards)

    def cardListing(self):
        self.view.clear_frame()
        #cardListing()
