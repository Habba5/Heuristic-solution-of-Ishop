from View.view import *


class ViewCardListing(View):
    def __init__(self):
        super().__init__()
        self.sva = []

    def entryupdate(self, sv, i, deck):
        print(i)
        print(sv, i, deck[i][0], sv.get())
        self.controller.updateModel(i, sv.get())

    def view(self, deck):
        super().view()

        lbl1 = Label(self.frame, text="Kartenname")
        lbl1.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        lbl2 = Label(self.frame, text="Anzahl")
        lbl2.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        lbl3 = Label(self.frame, text="Kondition")
        lbl3.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
        lbl4 = Label(self.frame, text="Sprache")
        lbl4.grid(row=0, column=3, sticky="nsew", padx=5, pady=5)

        for card in deck:
            i = len(self.sva)
            self.sva.append(StringVar())
            self.sva[i].set(card[0])
            self.sva[i].trace("w", lambda name, index, mode, var=self.sva[i], i=i:
            self.entryupdate(var, i, deck))
            label = Label(self.frame, text=card[1])
            label.grid(row=i+1, column=0, sticky="nsew", padx=5, pady=5)
            entry = Entry(self.frame, text=self.sva[i])
            entry.grid(row=i+1, column=1, sticky="nsew", padx=5, pady=5)
