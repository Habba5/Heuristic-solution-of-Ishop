from Enum.Language import *
from Enum.Condition import *


class Card(object):

    def __init__(self, cardamount, cardname, cardurl):
        self.cardamount = cardamount
        self.cardname = cardname
        self.cardurl = cardurl
        self.cardlanguage = [Language.Deutsch, Language.Englisch]
        self.cardcondition = [Condition.Excellent, Condition.Near_Mint, Condition.Mint]

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