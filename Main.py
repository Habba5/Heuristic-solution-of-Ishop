from Model.model import *
from Controller.controllerLogin import *
from Controller.controllerCardSearch import *
from Controller.controllerCardListing import *


#viewLogin = ViewLogin()
#viewCardSearch = ViewCardSearch()

model = Model()
cardList = [['4', 'Akroan Crusader', 'https://www.cardmarket.com/de/Magic/Cards/Akroan+Crusader'], ['1', 'Aurelia, the Warleader', 'https://www.cardmarket.com/de/Magic/Cards/Aurelia%2C+the+Warleader'], ['4', 'Champion of the Parish', 'https://www.cardmarket.com/de/Magic/Cards/Champion+of+the+Parish'], ['1', 'Gisela, Blade of Goldnight', 'https://www.cardmarket.com/de/Magic/Cards/Gisela%2C+Blade+of+Goldnight'], ['4', 'Lightning Mauler', 'https://www.cardmarket.com/de/Magic/Cards/Lightning+Mauler'], ['4', 'Master of Diversion', 'https://www.cardmarket.com/de/Magic/Cards/Master+of+Diversion'], ['1', 'Odric, Master Tactician', 'https://www.cardmarket.com/de/Magic/Cards/Odric%2C+Master+Tactician'], ['4', 'Silverblade Paladin', 'https://www.cardmarket.com/de/Magic/Cards/Silverblade+Paladin'], ['4', 'Souls of the Faultless', 'https://www.cardmarket.com/de/Magic/Cards/Souls+of+the+Faultless'], ['4', 'Vexing Devil', 'https://www.cardmarket.com/de/Magic/Cards/Vexing+Devil'], ['4', 'Zealous Conscripts', 'https://www.cardmarket.com/de/Magic/Cards/Zealous+Conscripts'], ['1', 'Tibalt, the Fiend-Blooded', 'https://www.cardmarket.com/de/Magic/Cards/Tibalt%2C+the+Fiend-Blooded'], ['2', 'Coordinated Assault', 'https://www.cardmarket.com/de/Magic/Cards/Coordinated+Assault'], ['4', 'Dauntless Onslaught', 'https://www.cardmarket.com/de/Magic/Cards/Dauntless+Onslaught'], ['4', 'Holy Mantle', 'https://www.cardmarket.com/de/Magic/Cards/Holy+Mantle'], ['1', 'Dark Depths', 'https://www.cardmarket.com/de/Magic/Cards/Dark+Depths'], ['5', 'Mountain', 'https://www.cardmarket.com/de/Magic/Cards/Mountain'], ['4', 'Orzhov Basilica', 'https://www.cardmarket.com/de/Magic/Cards/Orzhov+Basilica']]
model.deck = cardList

def cardSearch():
    controllerCardSearch = ControllerCardSearch(model)
    controllerCardSearch.view.main_loop()

def cardListing():
    controllerCardListing = ControllerCardListing(model)
    controllerCardListing.view.main_loop()

def start():
    controllerLogin = ControllerLogin(model)
    #controllerCardSearch = ControllerCardSearch(model)
    controllerLogin.view.main_loop()

if (__name__ == "__main__"):
    # model = Model()
    # start()
    # cardSearch()
    cardListing()

#viewLogin.main_loop()
#viewCardSearch.main_loop()
