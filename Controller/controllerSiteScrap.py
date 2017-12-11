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

MAX_THREADS = 5
thread_lock = threading.Lock()


class ControllerCardSearch(Controller):

    def __init__(self, model, view):
        super().__init__(model, view)

    def message(self, s):
        print('{}: {}'.format(threading.current_thread().name, s))

    def user(href):
        return href and re.compile("Users").search(href)

    def standort(onmouseover):
        return onmouseover and re.compile("Artikelstandort").search(onmouseover)

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
            max_pages = int(ceil(card.totaloffers/50))
            args1 = card.jcppayload
            url = card.cardurl
            while hits < 100 and max_pages > page:
                args2 = quote(card.id + "," + str(page) + ",")
                args = args1.join(args2)
                response = session.post(
                    url='https://www.cardmarket.com/iajax.php',
                    data={
                        'args': args
                    },
                    headers={
                        'Referer': url
                    }
                )
                str = response.text
                #remove wrapper
                str = str[67:-31]
                str = base64.b64decode(str)
                soup = BeautifulSoup(str, 'html.parser')
                items = soup.find_all('tr')
                for item in items:
                    seller = item.find(href=self.user).text
                    str = item.find(onmouseover=self.standort)["onmouseover"]
                    sellerlocation = None
                    for location in Location:
                        if location.value != 1:
                            if self.findWord(location.name)(str) is not None:
                                sellerlocation = location
                        else:
                            if self.findWord(location.name.replace("_", " "))(str) is not None:
                                sellerlocation = location

                    sellerid = (item.find("td", {"class": "st_price Price"}).div["id"])[5:]
                    price = item.find("td", {"class": "st_price Price"}).div.div.text
                    amountaviable = item.find("td", {"class": "st_ItemCount"}).text
                    card.addoffer(seller, price, sellerid, sellerlocation, amountaviable)
                    hits += 1
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