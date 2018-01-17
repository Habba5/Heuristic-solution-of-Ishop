from Model.model import *

# Model das Nutzerinfos speichert

class ModelCredentials(Model):

    def __init__(self):
        self.username = None
        self.password = None
        super().__init__()

    def username(self):
        return self.username

    def password(self):
        return self.password

    def deck(self):
        return self.deck