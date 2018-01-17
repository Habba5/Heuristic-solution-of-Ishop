from Model.modelCredentials import *
from Model.modelDeck import *
from View.viewLogin import *
from View.viewCardListing import *
from View.viewCardSearch import *
from View.viewSiteScrap import *
from View.viewAlgorithm import *
from View.viewBuy import *
from Controller.controllerLogin import *
from Controller.controllerCardSearch import *
from Controller.controllerCardListing import *
from Controller.controllerSiteScrap import *
from Controller.controllerMinMin import *
from Controller.controllerAlgorithm import *
from Controller.controllerBuy import *

# Lists of all Modules
viewlogin = NONE
viewcardlisting = NONE
viewcardsearch = NONE
viewSiteScrap = NONE
viewMinMin = NONE
viewBuy = NONE
view = [viewlogin, viewcardsearch, viewcardlisting, viewSiteScrap, viewMinMin, viewBuy]
modelDeck = ModelDeck()
modelCredentials = ModelCredentials()
modelSiteScrap = NONE
model = [modelCredentials, modelDeck, modelSiteScrap]
controllerCardSearch = NONE
controllerCardListing = NONE
controllerLogin = NONE
controllerCardBuy = NONE
controllerSiteScrap = NONE
controllerAlgorithm = NONE
controller = [controllerLogin, controllerCardSearch, controllerCardListing, controllerSiteScrap, controllerAlgorithm, controllerCardBuy]



def buying(tk):
    view[5] = ViewBuy(master=tk)
    controller[5] = ControllerBuy(model[0], model[1], view[5])
    controller[5].view.main_loop()
    view[5] = NONE
    controller[5] = NONE

def algorithm(tk):
    view[4] = ViewAlgorithm(master=tk)
    controller[4] = ControllerAlgorithm(model[1], view[4])
    view[4] = NONE
    controller[4] = NONE

def siteScrap(tk):
    view[3] = ViewSiteScrap(master=tk)
    controller[3] = ControllerSiteScrap(model[1], view[3])
    view[3] = NONE
    controller[3] = NONE

def cardSearch(tk):
    view[1] = ViewCardSearch(master=tk)
    controller[1] = ControllerCardSearch(model[1], view[1])
    controller[1].view.main_loop()
    view[1] = NONE
    controller[1] = NONE

def cardListing(tk):
    view[2] = ViewCardListing(master=tk)
    controller[2] = ControllerCardListing(model[1], view[2])
    controller[2].view.main_loop()
    view[2] = NONE
    controller[2] = NONE

def login(tk):
    view[0] = ViewLogin(master=tk)
    controller[0] = ControllerLogin(model[0], view[0])
    controller[0].view.main_loop()
    view[0] = NONE
    controller[0] = NONE

if (__name__ == "__main__"):
    tk = Tk()
    try:
        login(tk)
        cardSearch(tk)
        cardListing(tk)
        siteScrap(tk)
        print("Jo")
        algorithm(tk)
        buying(tk)
    except TclError:
        pass
