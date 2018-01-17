from View.view import *


class ViewBuy(View):
    def __init__(self, master=None):
        super().__init__(master)

    def calculateShipping(self, locationSeller, locationBuyer, amount, totalprice):
        #Default für Versand von und nach Deutschland
        default_price_20g = 1.0
        default_price_50g = 1.15
        default_price_500g = 1.95
        between25_50_price = 3.5
        between50_100_price = 3.95
        between100_500price = 6.0
        between500_2500price = 12.0
        #Durchschnittliche Versandkosten in Europa(irgendwie ist innerhalb Deutschland Konkurenzlos günstig)
        if locationBuyer != "Deutschland" or locationSeller != "Deutschland":
            default_price_20g = 2.0
            default_price_50g = 2.3
            default_price_500g = 4.5
            between25_50_price = 8.0
            between50_100_price = 10.0
            between100_500price = 12.0
            between500_2500price = 24.0

        # bei höheren Preisen ist Gewicht vernachlässigbar
        if totalprice <= 25:
            if amount <= 4:
                return default_price_20g
            elif amount < 18:
                return default_price_50g
            else:
                return default_price_500g
        elif totalprice <= 50:
            return between25_50_price
        elif totalprice <= 100:
            return between50_100_price
        elif totalprice <= 500:
            return between100_500price
        else:
            return between500_2500price

    def onFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def view(self):
        super().view()

        # Erstelle ein Canvas mit einer Scrollbar, im Frame
        self.canvas = Canvas(self, width=450)

        self.canvas.pack(side=LEFT)

        scrollbar = Scrollbar(self, command=self.canvas.yview)
        scrollbar.pack(side=LEFT, fill='y')

        self.canvas.configure(yscrollcommand=scrollbar.set)

        # aktualisiere die mögliche Scroll-Region nach dem alle Elemente im Canvas sind
        # nach der Mainloop
        self.canvas.bind('<Configure>', self.onFrameConfigure)

        # Erstelle ein Frame im Canvas

        newframe = Frame(self.canvas)
        self.canvas.create_window((0, 0), window=newframe, anchor='nw')

        location = self.controller.get_location()
        # Erstelle Überschrift
        lbl = Label(newframe, text="Einkaufswagen")
        lbl.grid(sticky="nsew", columnspan=3, padx=10, pady=10)

        shopping_list = self.controller.get_shopping_list()
        i = 1
        # Iteriere durch Einträge der Shopping-Liste und geb wichtige Daten zu ihnen an
        # Die Liste enthält Listen von Artikeln je Anbieter
        # Wie Name, Preis, Menge und Versandkosten bei diesem Händler
        for item in shopping_list:
            lbl_distr = Label(newframe, text="Verkäufer: " + item[0].distributorname)
            lbl_distr.grid(row=i, column=0, sticky="nsew", padx=5, pady=5)
            loc_seller = item[0].location
            amount = 0
            price = 0
            i_el = 0
            for elemen in item:
                if elemen.playset:
                    amount += elemen.amountaviable_used * 4
                    price += (elemen.amountaviable_used * 4) * elemen.price
                else:
                    amount += elemen.amountaviable_used
                    price += elemen.amountaviable_used * elemen.price
                lbl_item1 = Label(newframe, text="Karte: " + elemen.cardname)
                lbl_item1.grid(row=i+1+i_el, column=1, sticky="nsew", padx=5, pady=5)
                lbl_item2 = Label(newframe, text="Menge: " + str(elemen.amountaviable_used))
                lbl_item2.grid(row=i+2+i_el, column=1, sticky="nsew", padx=5, pady=5)
                lbl_item3 = Label(newframe, text="Playset: " + str(elemen.playset))
                lbl_item3.grid(row=i+2+i_el, column=2, sticky="nsew", padx=5, pady=5)
                lbl_item4 = Label(newframe, text="Preis: " + str(elemen.price))
                lbl_item4.grid(row=i+3+i_el, column=1, sticky="nsew", padx=5, pady=5)
                i_el += 3
            overall_price = self.calculateShipping(loc_seller, location, amount, price)
            lbl_item5 = Label(newframe, text="Versandkosten: " + str(overall_price))
            lbl_item5.grid(row=i + i_el + 1, column=0, sticky="nsew", padx=5, pady=5)
            i =i + 2 + i_el

        # Erstelle Button
        btn = Button(newframe, text="In den Warenkorb", command=lambda: self.clickedLogin())
        btn.grid(row=1000, column=0, sticky="nsew", padx=5, pady=5)

    def clickedLogin(self):
        self.controller.buy()