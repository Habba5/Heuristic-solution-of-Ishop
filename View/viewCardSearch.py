from View.view import *


class ViewCardSearch(View):
    def __init__(self):
        super().__init__()

    def view(self):
        super().view()
        # self.clear_screen()
        # self.frame.grid(sticky="nsew")

        lbl = Label(self.frame, text="Karten die bestellt werden sollen: ")
        lbl.grid(row=0, sticky="nsew", padx=5, pady=5)

        TextArea = Text()
        TextArea.grid(row=1, column=0, padx=5, pady=5)
        btn = Button(self.frame, text="Karten prüfen", command=lambda: self.clickedCardSearch(TextArea.get("1.0", 'end-1c')))
        btn.grid(row=2, sticky="w", column=0, padx=5, pady=5)

    def clickedCardSearch(self, cards):
        self.controller.searchCards(cards)

    def viewError(self, error, errorcards):
        toplevel = Toplevel()
        label1 = Label(toplevel, text=error)
        label1.pack()
        label2 = Label(toplevel, text=errorcards)
        label2.pack()
        button1 = Button(toplevel, text="Ok", command=toplevel.destroy)
        button1.pack()
        toplevel.focus_force()
