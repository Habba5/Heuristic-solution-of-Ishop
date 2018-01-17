from Enum.Language import *
from Enum.Condition import *
from objects.offer import *

# card simuliert Informationen über eine Karte
# jedes card object hält eine Liste von offer objecten

class Card(object):

    def __init__(self, cardamount, cardname, cardurl, expansions, id, jcppayload, totaloffers):
        self.cardamount = cardamount
        self.cardname = cardname
        self.cardurl = cardurl
        self.cardlanguage = [Language.Deutsch, Language.Englisch]
        self.cardcondition = [Condition.Excellent, Condition.Near_Mint, Condition.Mint, Condition.Played, Condition.Light_Played, Condition.Good, Condition.Poor]
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

    def addoffer(self, distributorname, price, id, location, amountaviable, playset):
        self.offers.append(Offer(distributorname, price, id, location, amountaviable, playset))