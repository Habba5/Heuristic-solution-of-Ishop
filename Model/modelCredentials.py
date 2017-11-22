from Model.model import *


class ModelCredentials(Model):

    def __init__(self):
        self.username = None
        self.password = None
        self.deck = None
        super().__init__()

    def username(self):
        return self.username

    def password(self):
        return self.password

    def deck(self):
        return self.deck