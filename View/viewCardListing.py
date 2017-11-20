from View.view import *


class ViewCardListing(View):
    def __init__(self):
        super().__init__()
        self.sva = []
        self.variablelanguage = []
        self.variablecondition = []
        self.choices = []
        # Create an empty Canvas (Declaring doesn´t work here, because super.view method clears frame)
        self.canvas = NONE

    def entryupdatelanguage(self, sv, i, deck):
        print(i)
        print(sv, i, deck[i][0], sv.get())
        self.controller.updateModelLanguage(i, sv.get())

    def entryupdatecondition(self, sv, i, deck):
        print(i)
        print(sv, i, deck[i][0], sv.get())
        self.controller.updateModelCondition(i, sv.get())

    def entryupdate(self, sv, i, deck):
        print(i)
        print(sv, i, deck[i][0], sv.get())
        self.controller.updateModel(i, sv.get())

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def clickedCalculate(self, location, rating):
        self.controller.calculate(location, rating)

    def printValues(self, choice):
        print(self.choices)
        for name, var in choice.items():
            print("%s: %s" % (name, var.get()))

    def view(self, deck):
        super().view()

        # Creating a Canvas inside the frame, with a scrollbar
        self.canvas = Canvas(self.frame, width=600)

        self.canvas.pack(side=LEFT)

        scrollbar = Scrollbar(self.frame, command=self.canvas.yview)
        scrollbar.pack(side=LEFT, fill='y')

        self.canvas.configure(yscrollcommand=scrollbar.set)

        # update scrollregion after starting 'mainloop'
        # when all widgets are in canvas
        self.canvas.bind('<Configure>', self.onFrameConfigure)

        # Put another frame in the Canvas

        newframe = Frame(self.canvas)
        self.canvas.create_window((0, 0), window=newframe, anchor='nw')

        # add widgets in frame

        # lbl1 = Label(self.frame, text="Kartenname")
        # lbl1.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        # lbl2 = Label(self.frame, text="Anzahl")
        # lbl2.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        # lbl3 = Label(self.frame, text="Kondition")
        # lbl3.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
        # lbl4 = Label(self.frame, text="Sprache")
        # lbl4.grid(row=0, column=3, sticky="nsew", padx=5, pady=5)

        variablelocation = StringVar()
        variablelocation.set("Deutschland")  # default value

        variablerating = StringVar()
        variablerating.set("Deutschland")  # default value

        lbl1 = Label(newframe, text="Kartenname")
        lbl1.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        lbl2 = Label(newframe, text="Anzahl")
        lbl2.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        lbl3 = Label(newframe, text="Kondition")
        lbl3.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
        lbl4 = Label(newframe, text="Sprache")
        lbl4.grid(row=0, column=3, sticky="nsew", padx=5, pady=5)
        lbl5 = Label(newframe, text="Ihr Standort")
        lbl5.grid(row=50, column=0, sticky="nsew", padx=5, pady=5)
        location = OptionMenu(newframe, variablelocation, "Deutschland", "England")
        location.grid(row=51, column=0, sticky="nsew", padx=5, pady=5)
        lbl6 = Label(newframe, text="Verkäufer Mindestbewertung")
        lbl6.grid(row=52, column=0, sticky="nsew", padx=5, pady=5)
        rating = OptionMenu(newframe, variablerating, "Deutschland", "England")
        rating.grid(row=53, column=0, sticky="nsew", padx=5, pady=5)
        btn = Button(newframe, text="Preis berechnen", command=lambda: self.clickedCalculate(variablelocation, variablerating))
        btn.grid(row=2, sticky="w", column=0, padx=5, pady=5)


        for card in deck:
            i = len(self.sva)

            menubutton = Menubutton(newframe, text="Sprache/n", indicatoron=True, borderwidth=1, relief="raised")
            menu = Menu(menubutton, tearoff=False)
            menubutton.configure(menu=menu)
            menubutton.grid(row=i+1, column=4)

            #variablelanguage = StringVar()
            #variablelanguage.set("Deutsch")  # default value

            # self.choices.append({})
            # for choice in ("Deutsch", "English"):
            #     self.choices[i][choice] = IntVar(value=1)
            #     menu.add_checkbutton(label=choice, variable=variablelanguage,
            #                          onvalue=1, offvalue=0)

            # variable=self.choices[i][choice]
            #self.choices[i][1].trace("w", lambda name, index, mode, var=self.choices[i][1], i=i:
            #self.printValues(var))


            #variablecondition = StringVar()
            #variablecondition.set("Excellent")  # default value

            self.sva.append(StringVar())
            self.sva[i].set(card[0])
            self.sva[i].trace("w", lambda name, index, mode, var=self.sva[i], i=i:
            self.entryupdate(var, i, deck))

            self.variablelanguage.append(StringVar())
            self.variablelanguage[i].set("Deutsch")
            self.variablelanguage[i].trace("w", lambda name, index, mode, var=self.variablelanguage[i], i=i:
            self.entryupdatelanguage(var, i, deck))

            self.variablecondition.append(StringVar())
            self.variablecondition[i].set("Excellent")
            self.variablecondition[i].trace("w", lambda name, index, mode, var=self.variablecondition[i], i=i:
            self.entryupdatecondition(var, i, deck))

            label = Label(newframe, text=card[1])
            label.grid(row=i+1, column=0, sticky="nsew", padx=5, pady=5)
            entry = Entry(newframe, text=self.sva[i])
            entry.grid(row=i+1, column=1, sticky="nsew", padx=5, pady=5)
            condition = OptionMenu(newframe, self.variablecondition[i], "Excellent", "Mint", "Near Mint", "Light Played", "Played")
            condition.grid(row=i+1, column=2, sticky="nsew", padx=5, pady=5)
            language = OptionMenu(newframe, self.variablelanguage[i], "Deutsch", "Englisch")
            language.grid(row=i+1, column=3, sticky="nsew", padx=5, pady=5)



