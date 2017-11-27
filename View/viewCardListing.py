from View.view import *
from Enum.Location import *
from Enum.SellerRating import *
from Enum.Language import *
from Enum.Condition import *


class ViewCardListing(View):
    def __init__(self):
        super().__init__()
        # Variable for amounts of every card
        # can be edit by a textfield
        self.cardamount = []
        # dictionary for languages of selected card
        self.choiceslanguage = {}
        # dictionary for condition of selected card
        self.choicescondition = {}
        # Create an empty Canvas (Declaring doesn´t work here, because super.view method clears frame)
        self.canvas = NONE

    def updatelocation(self, location):
        self.controller.updateModelLocation(location)

    def updaterating(self, rating):
        self.controller.updateModelRating(rating)

    def updatecardlanguage(self, i, choice, language):
        #print("Position :" + str(i) + " Sprache:" + str(language.get()))
        #print(self.choiceslanguage.items())
        self.controller.updateModelCardLanguage(i, choice, language.get())

    def updatecardcondition(self, i, choice, condition):
        self.controller.updateModelCardCondition(i, choice, condition.get())

    def entryupdate(self, i, newamount):
        print(i)
        #print(sv, i, deck[i][0], sv.get())
        self.controller.updateModel(i, newamount.get())

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def clickedCalculate(self, location, rating):
        self.controller.calculate(location, rating)

    def view(self):
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

        # set and trace a variable for the location of the user
        variablelocation = StringVar()
        variablelocation.set((self.controller.getLocation()).name)  # default value
        variablelocation.trace("w", lambda name, index, mode: self.updatelocation(variablelocation.get()))

        # set and trace a variable for the minimum rating of the seller
        variablerating = StringVar()
        variablerating.set((self.controller.getSellerRating()).name)  # default value
        variablerating.trace("w", lambda name, index, mode: self.updaterating(variablerating.get()))

        # create a list of all options from Enum Location
        locations = []
        for location in Location:
            locations.append(location.name)

        # create a list of all options from Enum SellerRating
        ratings = []
        for rating in SellerRating:
            ratings.append(rating.name)

        # create a list of all options from Enum
        languages = []
        for language in Language:
            languages.append(language.name)

        # create a list of all options from Enum
        conditions = []
        for condition in Condition:
            conditions.append(condition.name)


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
        menulocation = OptionMenu(newframe, variablelocation, *locations)
        menulocation.grid(row=51, column=0, sticky="nsew", padx=5, pady=5)
        lbl6 = Label(newframe, text="Verkäufer Mindestbewertung")
        lbl6.grid(row=52, column=0, sticky="nsew", padx=5, pady=5)
        menurating = OptionMenu(newframe, variablerating, *ratings)
        menurating.grid(row=53, column=0, sticky="nsew", padx=5, pady=5)
        btn = Button(newframe, text="Preis berechnen", command=lambda: self.clickedCalculate(variablelocation, variablerating))
        btn.grid(row=2, sticky="w", column=0, padx=5, pady=5)

        deck = self.controller.getDeck()

        for card in deck:
            i = len(self.cardamount)

            # define menu for languages
            menubuttonlanguage = Menubutton(newframe, text="Sprache/n", indicatoron=True, borderwidth=1, relief="raised")
            menulanguage = Menu(menubuttonlanguage, tearoff=False)
            menubuttonlanguage.configure(menu=menulanguage)
            menubuttonlanguage.grid(row=i+1, column=3)

            # define menu for condition
            menubuttoncondition = Menubutton(newframe, text="Kondition/en", indicatoron=True, borderwidth=1, relief="raised")
            menucondition = Menu(menubuttoncondition, tearoff=False)
            menubuttoncondition.configure(menu=menucondition)
            menubuttoncondition.grid(row=i+1, column=4)

            # cardamount is the amount of a specific card
            # Tracer for changes in cardamount
            self.cardamount.append(StringVar())
            self.cardamount[i].set(card.cardamount)
            self.cardamount[i].trace("w", lambda name, index, mode, var=self.cardamount[i], i=i:
            self.entryupdate(i, var))

            # add choices for menulanguage
            for choice in languages:
                if Language[choice] in card.cardlanguage:
                    self.choiceslanguage[str(i)+choice] = IntVar(value=1)
                else:
                    self.choiceslanguage[str(i)+choice] = IntVar(value=0)
                menulanguage.add_checkbutton(label=choice, variable=self.choiceslanguage[str(i)+choice],
                                     onvalue=1, offvalue=0, command=lambda i=i, choice=choice: self.updatecardlanguage(i, choice, self.choiceslanguage[str(i)+choice]))

            # add choices for menucondition
            for choice in conditions:
                if Condition[choice] in card.cardcondition:
                    self.choicescondition[str(i) + choice] = IntVar(value=1)
                else:
                    self.choicescondition[str(i) + choice] = IntVar(value=0)
                menucondition.add_checkbutton(label=choice, variable=self.choicescondition[str(i) + choice],
                                     onvalue=1, offvalue=0, command=lambda i=i, choice=choice: self.updatecardcondition(i, choice, self.choicescondition[str(i) + choice]))

            # Widgets for individual card
            # contains traced cardamount and name
            label = Label(newframe, text=card.cardname)
            label.grid(row=i+1, column=0, sticky="nsew", padx=5, pady=5)
            entry = Entry(newframe, text=self.cardamount[i])
            entry.grid(row=i+1, column=1, sticky="nsew", padx=5, pady=5)
