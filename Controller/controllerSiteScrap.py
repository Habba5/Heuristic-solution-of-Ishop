from Controller.controller import *
from Enum.Location import *
from queue import Queue
import threading
from requests import Session, head, codes, get
from requests.utils import quote
from math import ceil
import base64
from bs4 import BeautifulSoup
import re
import time

MAX_RECONNECT = 4
MAX_THREADS = 10
thread_lock = threading.Lock()


class ControllerSiteScrap(Controller):

    def __init__(self, model, view):
        super().__init__(model, view)
        self.collectOffers()

    def message(self, s):
        print('{}: {}'.format(threading.current_thread().name, s))

    @staticmethod
    def cardexpansion(href):
        return href and re.compile("Expansions").search(href)

    @staticmethod
    def condition(href):
        return href and re.compile("CardCondition").search(href)

    @staticmethod
    def cardlanguage(href):
        return href and re.compile("CardLanguage").search(href)

    @staticmethod
    def user(href):
        return href and re.compile("Users").search(href)

    @staticmethod
    def standort(onmouseover):
        return onmouseover and re.compile("Artikelstandort").search(onmouseover)

    @staticmethod
    def findWord(w):
        return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

    def scrapper(self, q):
        while True:
            self.message('looking for the next enclosure')
            card = q.get()
            self.message('Scrapping offers for: {}'.format(card.cardname))
            session = Session()
            session.head('https://www.cardmarket.com/')
            page = 0
            hits = 0
            max_pages = int(ceil(int(card.totaloffers)/50))
            args1 = card.jcppayload
            self.message("JCP-Payload: {}".format(args1))
            url = card.cardurl
            self.message("Url :{}".format(url))
            self.message("Entering while")
            while hits < 4000 and max_pages > page:
                self.message("Entered while")
                args2 = card.id + "," + str(page) + ","
                args = args1 + args2
                self.message("Args:{}".format(args))
                run_post = True
                while run_post:
                    try:
                        response = session.post(
                            url='https://www.cardmarket.com/iajax.php',
                            data={
                                'args': args
                            },
                            headers={
                                'Referer': url
                            }
                        )
                        run_post = False
                    except:
                        time.sleep(1)
                        pass
                string = response.text
                #remove wrapper
                string = string[67:-31]
                string = base64.b64decode(string)
                soup = BeautifulSoup(string, 'html.parser')
                items = soup.find_all('tr')
                #thread_lock.acquire()
                self.message("Found items:{}".format(response.text))
                for item in items:
                    seller = item.find(href=self.user).text
                    string = item.find(onmouseover=self.standort)["onmouseover"]
                    sellerlocation = None
                    for location in Location:
                        if location.value != 1:
                            if self.findWord(location.name)(string) is not None:
                                sellerlocation = location
                        else:
                            if self.findWord(location.name.replace("_", " "))(string) is not None:
                                sellerlocation = location
                    sellerid = (item.find("td", {"class": "st_price Price"}).div["id"])[5:]
                    price = item.find("td", {"class": "st_price Price"}).div.div.text
                    price = price.split("€", 1)[0]
                    price = price[:-1]
                    price = price.replace(",", ".")
                    price = float(price)
                    amountaviable = item.find("td", {"class": "st_ItemCount"}).text
                    amountaviable = int(amountaviable)
                    language = (item.find(href=self.cardlanguage).span["onmouseover"])
                    condition = (item.find(href=self.condition).span["onmouseover"])
                    expansion = (item.find(href=self.cardexpansion).span["onmouseover"])
                    language_hit = False
                    condition_hit = False
                    expansion_hit = False
                    for cardlanguage in card.cardlanguage:
                        if self.findWord(cardlanguage.name)(language) is not None:
                            language_hit = True
                    for cardcondition in card.cardcondition:
                        if self.findWord(cardcondition.name)(condition) is not None:
                            condition_hit = True
                    if card.expansions[0] == "Egal":
                        expansion_hit = True
                    else:
                        for cardexpansion in card.expansions:
                            if self.findWord(cardexpansion.name)(expansion) is not None:
                                expansion_hit = True
                    if condition_hit and language_hit and expansion_hit:
                        thread_lock.acquire()
                        card.addoffer(seller, price, sellerid, sellerlocation, amountaviable)
                        self.message("Currently on Hit:{}".format(hits))
                        hits += 1
                        thread_lock.release()
                #thread_lock.release()
                page +=1
            q.task_done()

    def collectOffers(self):
        queue = Queue()

        for card in self.model.deck:
            queue.put(card, self.model.sellerrating)

        for i in range(MAX_THREADS):
            worker = threading.Thread(
                target=self.scrapper,
                args=(queue,),
                name='worker-{}'.format(i),
            )
            worker.setDaemon(True)
            worker.start()

        self.message('*** main thread waiting')
        queue.join()

        for card in self.model.deck:
            print(card.offers)
        #self.MinMin()

    def MinMin(self):
        self.view.clear_frame()