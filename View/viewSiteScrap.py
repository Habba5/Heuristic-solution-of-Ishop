from View.view import *
from tkinter import ttk

class ViewSiteScrap(View):
    def __init__(self):
        super().__init__()

    def view(self):
        super().view()

        lbl = Label(self.frame, text="Karten werden gesucht ...")
        lbl.grid(sticky="nsew", columnspan=2, padx=10, pady=10)

        self.p = ttk.Progressbar(self.frame, orient=HORIZONTAL, length=200, mode='determinate')
        self.p.pack