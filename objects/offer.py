#Angebot eines Händler

class Offer(object):

    def __init__(self, distributorname, price, id, location, amountaviable, playset):
        self.distributorname = distributorname
        self.price = price
        self.id = id
        self.location = location
        self.amountaviable = amountaviable
        self.playset = playset

    def distributorname(self):
        return self.distributorname

    def price(self):
        return self.price

    def id(self):
        return self.id

    def location(self):
        return self.location