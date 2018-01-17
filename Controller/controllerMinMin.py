from Controller.controller import *
import math

class ControllerMinMin(Controller):

    def __init__(self, model, view):
        super().__init__(model, view)
        self.searchMinMin()
    # Fehlerhaft, wird nicht mehr verwendet
    def searchMinMin(self):
        print("Test")
        Ni = []
        N = []
        M = []
        X = []
        for card in self.model.deck:
            N.append([card.cardamount, card.cardname])
            #Ni.append(None)
            for offer in card.offers:
                if offer.distributorname not in M:
                    M.append(offer.distributorname)
                    Ni.append(None)
                    X.append(None)
        for nix, ni in enumerate(Ni):
            #ni = []
            Ni[nix] = []
            for n in N:
                #ni.append(None)
                Ni[nix].append(None)
        print(Ni)
        for card in self.model.deck:
            cardname = card.cardname
            cardamount = card.cardamount
            cardurl = card.cardurl
            for offer in card.offers:
                #if Ni[M.index(offer.distributorname)] is None:
                    Ni[M.index(offer.distributorname)][N.index([cardamount, cardname])] = [cardname, offer.amountaviable, offer.price, offer.id, cardurl, offer.distributorname]
                #else:
                    #Ni[M.index(offer.distributorname)][N.index([cardamount, cardname])].append([cardname, offer.amountaviable, offer.price, offer.id, cardurl, offer.distributorname])
                #Ni.insert(N.index(offer.distributorname), [cardname, offer.amountaviable])
        while N != [None] * len(N):
            i = 0
            min = []
            j_iter = []
            for n in N:
                #min[i] = math.inf
                min.append(math.inf)
                #j_iter[i] = None
                j_iter.append(None)
                i += 1
            #min = math.inf
            for m in M:
                i = M.index(m)
                for n in N:
                    j = N.index(n)
                    if Ni[i][j] is not None:
                        #X[i] = Ni[i][j]
                        if Ni[i][j][2] < min[j]:
                            min[j] = Ni[i][j][2]
                            j_iter[j] = Ni[i][j]
            for j in j_iter:
                index_j = j_iter.index(j)
                index_i = M.index(j[5])
                X[index_i] = j
                amount_needed = N[index_j][0]
                if (amount_needed - j_iter[1]) <= 0:
                    X[index_i][1] = amount_needed
                    N[index_j] = None
                else:
                    sub = amount_needed - j_iter[1]
                    N[index_j][0] = sub
                    X[index_i][1] = sub
        print(X)
