from Model.modelCredentials import *
from Model.modelDeck import *
from View.viewLogin import *
from View.viewCardListing import *
from View.viewCardSearch import *
from Controller.controllerLogin import *
from Controller.controllerCardSearch import *
from Controller.controllerCardListing import *
from queue import Queue


#viewLogin = ViewLogin()
#viewCardSearch = ViewCardSearch()

#model = Model()
#cardList = [['4', 'Akroan Crusader', 'https://www.cardmarket.com/de/Magic/Cards/Akroan+Crusader'], ['1', 'Aurelia, the Warleader', 'https://www.cardmarket.com/de/Magic/Cards/Aurelia%2C+the+Warleader'], ['4', 'Champion of the Parish', 'https://www.cardmarket.com/de/Magic/Cards/Champion+of+the+Parish'], ['1', 'Gisela, Blade of Goldnight', 'https://www.cardmarket.com/de/Magic/Cards/Gisela%2C+Blade+of+Goldnight'], ['4', 'Lightning Mauler', 'https://www.cardmarket.com/de/Magic/Cards/Lightning+Mauler'], ['4', 'Master of Diversion', 'https://www.cardmarket.com/de/Magic/Cards/Master+of+Diversion'], ['1', 'Odric, Master Tactician', 'https://www.cardmarket.com/de/Magic/Cards/Odric%2C+Master+Tactician'], ['4', 'Silverblade Paladin', 'https://www.cardmarket.com/de/Magic/Cards/Silverblade+Paladin'], ['4', 'Souls of the Faultless', 'https://www.cardmarket.com/de/Magic/Cards/Souls+of+the+Faultless'], ['4', 'Vexing Devil', 'https://www.cardmarket.com/de/Magic/Cards/Vexing+Devil'], ['4', 'Zealous Conscripts', 'https://www.cardmarket.com/de/Magic/Cards/Zealous+Conscripts'], ['1', 'Tibalt, the Fiend-Blooded', 'https://www.cardmarket.com/de/Magic/Cards/Tibalt%2C+the+Fiend-Blooded'], ['2', 'Coordinated Assault', 'https://www.cardmarket.com/de/Magic/Cards/Coordinated+Assault'], ['4', 'Dauntless Onslaught', 'https://www.cardmarket.com/de/Magic/Cards/Dauntless+Onslaught'], ['4', 'Holy Mantle', 'https://www.cardmarket.com/de/Magic/Cards/Holy+Mantle'], ['1', 'Dark Depths', 'https://www.cardmarket.com/de/Magic/Cards/Dark+Depths'], ['5', 'Mountain', 'https://www.cardmarket.com/de/Magic/Cards/Mountain'], ['4', 'Orzhov Basilica', 'https://www.cardmarket.com/de/Magic/Cards/Orzhov+Basilica']]
#model.deck = cardList
viewlogin = NONE
viewcardlisting = NONE
viewcardsearch = NONE
viewSiteScrap = NONE
view = [viewlogin, viewcardsearch, viewcardlisting, viewSiteScrap]
modelDeck = ModelDeck()
modelCredentials = ModelCredentials()
modelSiteScrap = NONE
model = [modelCredentials, modelDeck, modelSiteScrap]
controllerCardSearch = NONE
controllerCardListing = NONE
controllerLogin = NONE
controllerCardBuy = NONE
controllerSiteScrap = NONE
controller = [controllerLogin, controllerCardSearch, controllerCardListing, controllerSiteScrap, controllerCardBuy]

def siteScrap():
    return

def cardSearch():
    #model[1] = ModelDeck()
    view[1] = ViewCardSearch()
    controller[1] = ControllerCardSearch(model[1], view[1])
    #controllerCardSearch = ControllerCardSearch(model)
    #view[1].frame.after(100, view[1].testprog())
    #controller[1].view.parent.protocol("WM_DELETE_WINDOW", controller[1].view.shutdown_ttk_repeat)
    controller[1].view.main_loop()
    view[1] = NONE
    controller[1] = NONE

def cardListing():
    view[2] = ViewCardListing()
    controller[2] = ControllerCardListing(model[1], view[2])
    # controllerCardListing = ControllerCardListing(model)
    controller[2].view.main_loop()
    view[2] = NONE
    controller[2] = NONE

def login():
    view[0] = ViewLogin()
    controller[0] = ControllerLogin(model[0], view[0])
    controller[0].view.main_loop()
    view[0] = NONE
    controller[0] = NONE
    #controllerLogin = ControllerLogin(model)
    #controllerCardSearch = ControllerCardSearch(model)
    #controllerLogin.view.main_loop()

if (__name__ == "__main__"):
    # model = Model()
    # start()
    login()
    cardSearch()
    cardListing()
    siteScrap()

#viewLogin.main_loop()
#viewCardSearch.main_loop()
