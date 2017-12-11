from Controller.controller import *
from queue import Queue
from queue import *
import io
import threading
from requests import Session, head, codes, get
import time
from bs4 import BeautifulSoup
import re


MAX_THREADS = 5
thread_lock = threading.Lock()


class QueueChecker(threading.Thread):
    def __init__(self, q):
        threading.Thread.__init__(self)
        self.q = q

    def run(self):
        self.q.join()

class ControllerCardSearch(Controller):

    def __init__(self, model, view):
        self.wrongcards = []
        #view = ViewCardSearch()
        super().__init__(model, view)


    def exists(self, path):
        r = head(path)
        return r.status_code == codes.ok

    def replace(self, string):
        string = string.replace(' ', '+')
        string = string.replace(',', '%2C')
        string = string.replace('//', '%2F')
        string = string.replace(':', '%3A')
        string = string.replace('\'', '%27')
        return string

    def message(self, s):
        print('{}: {}'.format(threading.current_thread().name, s))

    def testUrls(self, q):
        while True:
            self.message('looking for the next enclosure')
            card = q.get()
            self.message('Testing {}'.format(card[0]))
            if self.exists(card[0]):
                page = get(card[0])
                expansions = []
                expansions.append("Egal")
                soup = BeautifulSoup(page.text, 'html.parser')
                expansioncontainer = soup.find("div", {"class": "expansionsBox"})
                items = expansioncontainer.find_all("span")
                for item in items:
                    expansions.append('-'.join(re.compile(r"(?<=\().+?(?=\))").findall(item["title"])))
                totaloffers = soup.find("input", {"name": "totalResults"})["value"]
                result = soup.find("div", {"id": "moreDiv"})["onclick"].split("'")
                jcppayload = result[1]
                idcard = (result[3])[:-1]
                thread_lock.acquire()
                if self.model.addcard(card[1], card[2], card[0], expansions, idcard, jcppayload, totaloffers) == 0:
                    self.message('Double entry for card{}'.format(card[2]))
                    self.wrongcards.append(card[2])
                thread_lock.release()
            else:
                self.message('Card not found{}'.format(card[2]))
                thread_lock.acquire()
                self.wrongcards.append(card[2])
                thread_lock.release()
            q.task_done()


    def searchCards(self, cards):
        # wait a second so tkinter doesn´t cry
        # i have noooo idea why this even works -.-
        time.sleep(1)
        buf = io.StringIO(cards)
        # wrongcards = []
        listcard = []
        for line in buf:
            listcard.append(line.split(' ', 1))

        urlcardde='https://www.cardmarket.com/de/Magic/Cards/'
        # urlcarden='https://www.cardmarket.com/en/Magic/Cards/'

        queue = Queue()

        for card in listcard:
            card[1] = card[1].rstrip('\n')
            cardstring = self.replace(card[1])
            queue.put([(urlcardde + cardstring), card[0], card[1]])
            # if self.exists(urlcardde + cardstring):
            #     if self.model.addcard(card[0], card[1], (urlcardde + cardstring)) == 0:
            #         wrongcards.append(card[1])
            # # elif self.exists(urlcarden + cardstring):
            # #     if self.model.addcard(card[0], card[1], (urlcarden + cardstring)) == 0:
            # #         wrongcards.append(card[1])
            # else:
            #     wrongcards.append(card[1])

        queuesize = queue.qsize()

        for i in range(MAX_THREADS):
            worker = threading.Thread(
                target=self.testUrls,
                args=(queue,),
                name='worker-{}'.format(i),
            )
            worker.setDaemon(True)
            worker.start()

        manager_thread = QueueChecker(queue)
        manager_thread.start()
        self.message('*** main thread waiting')

        while manager_thread.is_alive():
            self.view.testprog(queuesize, queue.unfinished_tasks, 0)
        self.view.testprog(queuesize, queue.unfinished_tasks, 1)
        # starting tkinter lookup
        # queuelength = self.queue.qsize()
        # self.view.clear_frame()
        # self.view.frame.after(100, self.view.testprog())
        # self.testpoller(queuelength)

        #self.message('*** main thread waiting')
        #self.queue.join()

        if not self.wrongcards:
            print("success")
            self.model.printdeck()
            self.cardListing()
        else:
            try:
                self.view.viewError("Die folgenden Karte/n konnte/n nicht gefunden werden :", self.wrongcards)
                self.wrongcards.clear()
            except RuntimeError:
                pass


    def cardListing(self):
        self.view.clear_frame()
        #cardListing()
