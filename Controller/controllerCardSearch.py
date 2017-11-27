from Controller.controller import *
from View.viewCardSearch import *
#from Main import cardListing
from queue import Queue
import io
import threading
from requests import Session, head, codes


MAX_THREADS = 5
thread_lock = threading.Lock()


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
                thread_lock.acquire()
                if self.model.addcard(card[1], card[2], card[0]) == 0:
                    self.message('Card not found{}'.format(card[2]))
                    self.wrongcards.append(card[2])
                thread_lock.release()
            else:
                self.message('Card not found{}'.format(card[2]))
                thread_lock.acquire()
                self.wrongcards.append(card[2])
                thread_lock.release()
            q.task_done()

    def searchCards(self, cards):
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

        for i in range(MAX_THREADS):
            worker = threading.Thread(
                target=self.testUrls,
                args=(queue,),
                name='worker-{}'.format(i),
            )
            worker.setDaemon(True)
            worker.start()

        self.message('*** main thread waiting')
        queue.join()

        if not self.wrongcards:
            print("success")
            self.model.printdeck()
        else:
            self.view.viewError("Die folgenden Karte/n konnte/n nicht gefunden werden :", self.wrongcards)
            self.wrongcards.clear()


    def cardListing(self):
        self.view.clear_frame()
        #cardListing()
