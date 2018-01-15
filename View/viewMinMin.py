from View.view import *
from tkinter import ttk

class ViewMinMin(View):
    def __init__(self, master=None):
        super().__init__(master)

    def view(self):
        super().view()

        lbl = Label(self, text="Karten werden gesucht ...")
        lbl.grid(sticky="nsew", columnspan=2, padx=10, pady=10)

        self.p = ttk.Progressbar(self, orient=HORIZONTAL, length=200, mode='determinate')
        self.p.pack