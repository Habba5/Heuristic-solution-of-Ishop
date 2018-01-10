from Controller.controller import *

class ControllerAlgorithm(Controller):

    def __init__(self, model, view):
        super().__init__(model, view)
        self.searchAlgorithm()

    def amountofdistributor(self, list, name):
        hits = 0
        for item in list:
            if item.distributorname == name:
                hits += 1
        return hits

    def calculateShipping(self, locationSeller, locationBuyer, amount, totalprice):
        #Default für Versand von und nach Deutschland
        default_price_20g = 1
        default_price_50g = 1.15
        default_price_500g = 1.95
        between25_50_price = 3.5
        between50_100_price = 3.95
        between100_500price = 6
        between500_2500price = 12
        #Durchschnittliche Versandkosten in Europa(irgendwie ist innerhalb Deutschland Konkurenzlos günstig)
        if locationBuyer != "Deutschland" or locationSeller != "Deutschland":
            default_price_20g = 4
            default_price_50g = 4.8
            default_price_500g = 8
            between25_50_price = 14
            between50_100_price = 16
            between100_500price = 32
            between500_2500price = 48

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

    def searchAlgorithm(self):
        # deck variable
        deck = self.model.deck
        # standort
        location = self.model.location
        # alle besten ergebisse
        shopping_list = []
        # Gehe alle Karten durch
        for card in deck:
            # Sequenz für die momentanen Karten
            current_sequence_card = []
            # Menge an Karten, die von dieser Karte benötigt werden
            amount_to_Satisfy = int(card.cardamount)
            # Menge die bereits gefunden wurde
            currently_at_amount = 0
            # Alle Angebote für die Karte
            offers = card.offers
            # Sortiere Angebote nach Preis
            offers.sort(key=lambda x: x.price, reverse=False)
            # Gehe alle Angebote durch
            for offer in offers:
                # Menge an verfügbaren Karten in sequence
                amount_in_sequence = 0
                # Wenn am Anfang, füge einfach hinzu
                if current_sequence_card.__len__() == 0:
                    current_sequence_card.append(offer)
                # Wenn schon ein Element gefunden
                else:
                    # Setze wieviele Karten eines Typs ich schon hab
                    for seq in current_sequence_card:
                        amount_in_sequence += seq.amountaviable
                    # Vergleiche ob Anzahl der Karten reicht
                    # Wenn nicht dann füge Angebot hinzu
                    if amount_in_sequence < amount_to_Satisfy:
                        current_sequence_card.append(offer)
                    # Wenn schon erfüllt, dann Vergleiche
                    else:
                        # Erstes Element das untersucht wird
                        if shopping_list.__len__() == 0:
                            # Wenn der Händler schon in der Sequence ist
                            if any(x.distributorname == offer.distributorname for x in current_sequence_card):
                                for seq in current_sequence_card:
                                    # Kein Vergleich mit Angebot des Händlers, da es eine sortierte Liste war
                                    # Angebot kann nicht günstiger werden
                                    if seq.distributorname != offer.distributorname:
                                        # Falls dieser Distributor nicht auch schon einmal vorkam, so wird verglichen, ansonsten wird es wahscheinlich nicht günstiger
                                        if not any(x.distributorname == seq.distributorname for x in current_sequence_card):
                                            max_amount_for_seq = 0
                                            if(seq.amountaviable < amount_to_Satisfy):
                                                max_amount_for_seq = seq.amountaviable
                                            else:
                                                max_amount_for_seq = amount_to_Satisfy
                                            total_price_distributor = max_amount_for_seq * seq.price
                                            if offer.price < self.calculateShipping(seq.location, location, max_amount_for_seq, total_price_distributor):
                                                amount_without_seq = amount_in_sequence - seq.amountaviable
                                                # Wenn nach theoretischem entfernen und hinzufügen des neuen Angebots die Anzahl die benötigt wird erreicht wird
                                                # , so entferne das Angebot aus seq und tausche es durch das neue aus
                                                if amount_without_seq + offer.amountaviable >= amount_to_Satisfy:
                                                    current_sequence_card.remove(seq)
                                                    current_sequence_card.append(offer)
                                                    # Unschön, aber nach dem Austausch brauch man nicht mehr weiter suchen
                                                    break
                                                # Andernfalls füge einfach nur hinzu
                                                else:
                                                    current_sequence_card.append(offer)
                                                    # Unschön, aber man weiß nun, das etwas besseres vorhanden ist und hat das hinzugefügt
                                                    break
                            # Wenn der Händler nicht in der sequence ist
                            else:
                                for seq in current_sequence_card:
                                    # Falls dieser Distributor nicht auch schon einmal vorkam, so wird verglichen, ansonsten wird es wahscheinlich nicht günstiger
                                    if not any(x.distributorname == seq.distributorname for x in current_sequence_card):
                                        max_amount_for_seq = 0
                                        if (seq.amountaviable < amount_to_Satisfy):
                                            max_amount_for_seq = seq.amountaviable
                                        else:
                                            max_amount_for_seq = amount_to_Satisfy
                                        max_amount_for_offer = 0
                                        if (offer.amountaviable < amount_to_Satisfy):
                                            max_amount_for_seq = offer.amountaviable
                                        else:
                                            max_amount_for_seq = amount_to_Satisfy
                                        total_price_seq = max_amount_for_seq * seq.price
                                        total_price_offer = max_amount_for_offer * offer.price
                                        if self.calculateShipping(offer.location, location, max_amount_for_offer, total_price_offer) < self.calculateShipping(seq.location, location, max_amount_for_seq, total_price_seq):
                                            amount_without_seq = amount_in_sequence - seq.amountaviable
                                            # Wenn nach theoretischem entfernen und hinzufügen des neuen Angebots die Anzahl die benötigt wird erreicht wird
                                            # , so entferne das Angebot aus seq und tausche es durch das neue aus
                                            if amount_without_seq + offer.amountaviable >= amount_to_Satisfy:
                                                current_sequence_card.remove(seq)
                                                current_sequence_card.append(offer)
                                                # Unschön, aber nach dem Austausch brauch man nicht mehr weiter suchen
                                                break
                                            # Andernfalls füge einfach nur hinzu
                                            else:
                                                current_sequence_card.append(offer)
                                                # Unschön, aber man weiß nun, das etwas besseres vorhanden ist und hat das hinzugefügt
                                                break
                        else:
                            # Vergleich muss auch mit der shopping_list geschehen
                            # Falls Händler dieses Angebotes schon in der sequence oder der shopping liste ist
                            if any(x.distributorname == offer.distributorname for x in shopping_list) or any(x.distributorname == offer.distributorname for x in current_sequence_card):
                                for seq in current_sequence_card:
                                    # Kein Vergleich mit Angebot des Händlers, da es eine sortierte Liste war
                                    # Angebot kann nicht günstiger werden
                                    if seq.distributorname != offer.distributorname:
                                        # Falls dieser Distributor nicht auch schon einmal vorkam, so wird verglichen, ansonsten wird es wahscheinlich nicht günstiger
                                        if not (any(x.distributorname == seq.distributorname for x in current_sequence_card) or any(x.distributorname == seq.distributorname for x in shopping_list)):
                                            max_amount_for_seq = 0
                                            if (seq.amountaviable < amount_to_Satisfy):
                                                max_amount_for_seq = seq.amountaviable
                                            else:
                                                max_amount_for_seq = amount_to_Satisfy
                                            total_price_distributor = max_amount_for_seq * seq.price
                                            if offer.price < self.calculateShipping(seq.location, location, max_amount_for_seq, total_price_distributor):
                                                amount_without_seq = amount_in_sequence - seq.amountaviable
                                                # Wenn nach theoretischem entfernen und hinzufügen des neuen Angebots die Anzahl die benötigt wird erreicht wird
                                                # , so entferne das Angebot aus seq und tausche es durch das neue aus
                                                if amount_without_seq + offer.amountaviable >= amount_to_Satisfy:
                                                    current_sequence_card.remove(seq)
                                                    current_sequence_card.append(offer)
                                                    # Unschön, aber nach dem Austausch brauch man nicht mehr weiter suchen
                                                    break
                                                # Andernfalls füge einfach nur hinzu
                                                else:
                                                    current_sequence_card.append(offer)
                                                    # Unschön, aber man weiß nun, das etwas besseres vorhanden ist und hat das hinzugefügt
                                                    break
                            # Falls der Händler noch nicht in der sequence oder shopping_list ist
                            else:
                                for seq in current_sequence_card:
                                    # Nur Vergleiche mit Händlern die noch nicht in der Sequenz oder shoppinglist waren
                                    if not (any(x.distributorname == seq.distributorname for x in current_sequence_card) or any(x.distributorname == seq.distributorname for x in shopping_list)):
                                        max_amount_for_seq = 0
                                        if (seq.amountaviable < amount_to_Satisfy):
                                            max_amount_for_seq = seq.amountaviable
                                        else:
                                            max_amount_for_seq = amount_to_Satisfy
                                        max_amount_for_offer = 0
                                        if (offer.amountaviable < amount_to_Satisfy):
                                            max_amount_for_seq = offer.amountaviable
                                        else:
                                            max_amount_for_seq = amount_to_Satisfy
                                        total_price_seq = max_amount_for_seq * seq.price
                                        total_price_offer = max_amount_for_offer * offer.price
                                        if self.calculateShipping(offer.location, location, max_amount_for_offer, total_price_offer) < self.calculateShipping(seq.location, location, max_amount_for_seq, total_price_seq):
                                            amount_without_seq = amount_in_sequence - seq.amountaviable
                                            # Wenn nach theoretischem entfernen und hinzufügen des neuen Angebots die Anzahl die benötigt wird erreicht wird
                                            # , so entferne das Angebot aus seq und tausche es durch das neue aus
                                            if amount_without_seq + offer.amountaviable >= amount_to_Satisfy:
                                                current_sequence_card.remove(seq)
                                                current_sequence_card.append(offer)
                                                # Unschön, aber nach dem Austausch brauch man nicht mehr weiter suchen
                                                break
                                            # Andernfalls füge einfach nur hinzu
                                            else:
                                                current_sequence_card.append(offer)
                                                # Unschön, aber man weiß nun, das etwas besseres vorhanden ist und hat das hinzugefügt
                                                break
            # Variable die später übergeben wird
            usable_sequence = []
            # Variable die Angiebt, wieviel schon in usable_sequence ist
            amount_satisfied = 0

            if shopping_list.__len__() == 0:
                for index, item in enumerate(current_sequence_card):
                    hits = self.amountofdistributor(current_sequence_card, item.distributorname)
                    if item.amountaviable < amount_to_Satisfy:
                        mutator = 1
                        if hits > 0:
                            mutator = float(1) / float((1 + hits))
                        price_per_card = 0
                        shipping = self.calculateShipping(item.location, location, item.amountaviable, (item.amountaviable * item.price)) * mutator
                        price_per_card = (float(shipping)/float(item.amountaviable)) + item.price
                        current_sequence_card[index].overall_price_per_card = price_per_card
                    else:
                        mutator = 1
                        if hits > 0:
                            mutator = float(1) / float((1 + hits))
                        price_per_card = 0
                        shipping = self.calculateShipping(item.location, location, amount_to_Satisfy, (amount_to_Satisfy * item.price)) * mutator
                        price_per_card = (float(shipping)/float(amount_to_Satisfy)) + item.price
                        current_sequence_card[index].overall_price_per_card = price_per_card
            else:
                for index, item in enumerate(current_sequence_card):
                    hits = self.amountofdistributor(current_sequence_card, item.distributorname)
                    if item.amountaviable < amount_to_Satisfy:
                        if any(x.distributorname == item.distributorname for x in shopping_list):
                            current_sequence_card[index].overall_price_per_card = current_sequence_card[index].price
                        else:
                            mutator = 1
                            if hits > 0:
                                mutator = float(1) / float((1 + hits))
                            price_per_card = 0
                            shipping = self.calculateShipping(item.location, location, item.amountaviable, (item.amountaviable * item.price)) * mutator
                            price_per_card = (shipping/item.amountaviable) + item.price
                            current_sequence_card[index].overall_price_per_card = price_per_card
                    else:
                        if any(x.distributorname == item.distributorname for x in shopping_list):
                            current_sequence_card[index].overall_price_per_card = current_sequence_card[index].price
                        else:
                            mutator = 1
                            if hits > 0:
                                mutator = float(1) / float((1 + hits))
                            price_per_card = 0
                            shipping = self.calculateShipping(item.location, location, amount_to_Satisfy, (amount_to_Satisfy * item.price)) * mutator
                            price_per_card = (float(shipping)/float(amount_to_Satisfy)) + item.price
                            current_sequence_card[index].overall_price_per_card = price_per_card
            #Sortiere die Liste nach overall_price_per_card
            current_sequence_card.sort(key=lambda x: x.overall_price_per_card, reverse=False)
            for usable_item in current_sequence_card:
                if amount_satisfied == amount_to_Satisfy:
                    break
                else:
                    if (amount_satisfied + usable_item.amountaviable) < amount_to_Satisfy:
                        usable_sequence.append(usable_item)
                        amount_satisfied += usable_item.amountaviable
                    else:
                        usable_item.amountaviable = amount_to_Satisfy - amount_satisfied
                        amount_satisfied = amount_to_Satisfy
                        usable_sequence.append(usable_item)
            shopping_list.extend(usable_sequence)

        shopping_list.sort(key=lambda x: x.distributorname, reverse=False)
        price_overall = 0
        shipping_overall = 0
        amount_temp = 0
        shipping_temp = 0
        price_temp = 0
        last_distributor = ""
        for item in shopping_list:
            #if last_distributor == "":
                #last_distributor = item.distributorname
            #if last_distributor != item.distributorname:
                #shipping_temp = 0
            price_overall += item.overall_price_per_card
            print("Händler: " + item.distributorname + " Preis pro Karte: " + str(item.price) + " Anzahl der Karten: " + str(item.amountaviable))
        print(price_overall)
        self.model.shopping_list = shopping_list