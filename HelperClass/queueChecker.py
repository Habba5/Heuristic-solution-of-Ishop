from queue import Queue
import threading

# Queuchecker Klasse
# Orignal : https://stackoverflow.com/questions/29290681/can-you-join-a-python-queue-without-blocking

class QueueChecker(threading.Thread):
    def __init__(self, q):
        threading.Thread.__init__(self)
        self.q = q

    def run(self):
        self.q.join()