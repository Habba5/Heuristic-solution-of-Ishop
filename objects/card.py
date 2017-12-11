from Enum.Language import *
from Enum.Condition import *
from objects.offer import *

class Card(object):

    def __init__(self, cardamount, cardname, cardurl, expansions, id, jcppayload, totaloffers):
        self.cardamount = cardamount
        self.cardname = cardname
        self.cardurl = cardurl
        self.cardlanguage = [Language.Deutsch, Language.Englisch]
        self.cardcondition = [Condition.Excellent, Condition.Near_Mint, Condition.Mint]
        self.expansions = expansions
        self.id = id
        self.jcppayload = jcppayload
        self.totaloffers = totaloffers
        self.offers = []

    def cardamount(self):
        return self.cardamount

    def cardname(self):
        return self.cardname

    def cardurl(self):
        return self.cardurl

    def cardlanguage(self):
        return self.cardlanguage

    def cardcondition(self):
        return self.cardcondition

    def offers(self):
        return self.offers

    def expansions(self):
        return self.expansions

    def id(self):
        return self.id

    def jcppayload(self):
        return self.jcppayload

    def totaloffers(self):
        return self.totaloffers

    def addoffer(self, distributorname, price, id, location, amountaviable):
        self.offers.append(Offer(distributorname, price, id, location, amountaviable))