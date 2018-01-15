from Controller.controller import *
import math
from queue import *
import threading
import random
import copy

MAX_NO_IMPROVE = 10
CHANGE_VALUE = 0.5
MAX_THREADS = 8
thread_lock = threading.Lock()

class ControllerAlgorithm(Controller):

    def __init__(self, model, view):
        super().__init__(model, view)
        self.best_solution = []
        self.searchAlgorithm()

    def message(self, s):
        print('{}: {}'.format(threading.current_thread().name, s))

    def mutator(self, q, deck_orig, location):
        #shopping_list = q
        while True:
            deck = deck_orig
            self.message('looking for the next enclosure')
            shopping_list = q.get()
            no_improve = 0
            while no_improve < MAX_NO_IMPROVE:
                #thread_lock.acquire()
                random.shuffle(deck)
                new_shopping_list = self.random_order(shopping_list, deck, int(len(shopping_list) * CHANGE_VALUE))
                #thread_lock.release()
                new_shopping_list = self.local_search(deck, location, copy.deepcopy(new_shopping_list))
                if self.eval_cost(new_shopping_list, location) < self.eval_cost(shopping_list, location):
                    self.message('Found better Solution')
                    shopping_list = new_shopping_list
                    no_improve = 0
                else:
                    no_improve += 1
            thread_lock.acquire()
            if self.eval_cost(shopping_list, location) < self.eval_cost(self.best_solution, location):
                self.best_solution = shopping_list
            thread_lock.release()
            q.task_done()

    def random_order(self, shopping_list, deck, change_value):
        random.seed()
        shopping_list_new = []
        length = len(shopping_list)
        random_indexes = random.sample(range(0, length-1), change_value)
        for i, offer_shopping_list in enumerate(shopping_list):
            if not any(x == i for x in random_indexes):
                shopping_list_new.append(offer_shopping_list)
        for index in random_indexes:
            name = shopping_list[index].cardname
            #print(name)
            item = None
            item = next((x for x in deck if x.cardname == name), None)
            #item = [x for x in deck if x.cardname == name]
            #item = item[0]
            if len(item.offers) == 0:
                print("Hier geflooogen :" + name + item.cardname)
            #length_offers = len(item.offers)
            max_amount_to_satisfy = 0
            if shopping_list[index].playset:
                max_amount_to_satisfy = shopping_list[index].amountaviable_used * 4
            else:
                max_amount_to_satisfy = shopping_list[index].amountaviable_used
            amount_satisfied = 0
            while amount_satisfied < max_amount_to_satisfy:
                if len(item.offers) == 0:
                    print("Hier geflooogen 2 :" + name + item.cardname)
                try:
                    offer = random.choice(item.offers)
                except:
                    print(item)
                    print(item.cardname)
                    print(item.offers)
                    print(name)
                    for card in deck:
                        print(card.cardname)
                offer.cardname = name
                if not any(x.id == offer.id for x in shopping_list_new):
                    max_amount_offer = 0
                    if offer.playset:
                        max_amount_offer = offer.amountaviable * 4
                    else:
                        max_amount_offer = offer.amountaviable
                    shopping_list_new.append(offer)
                    amount_satisfied += max_amount_offer
        return shopping_list_new

    def amountofdistributor(self, list, name):
        hits = 0
        for item in list:
            if item.distributorname == name:
                hits += 1
        return hits

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
            default_price_20g = 3.0
            default_price_50g = 4.0
            default_price_500g = 5.5
            between25_50_price = 9.0
            between50_100_price = 11.0
            between100_500price = 14.0
            between500_2500price = 28.0

        # bei höheren Preisen ist Gewicht vernachlässigbar
        if totalprice <= 25:
            if amount <= 4:
                return default_price_20g + totalprice
            elif amount < 18:
                return default_price_50g + totalprice
            else:
                return default_price_500g + totalprice
        elif totalprice <= 50:
            return between25_50_price + totalprice
        elif totalprice <= 100:
            return between50_100_price + totalprice
        elif totalprice <= 500:
            return between100_500price + totalprice
        else:
            return between500_2500price + totalprice

    def local_search(self, deck_orig, location, shopping_list_old):
        shopping_list = shopping_list_old
        # Gehe alle Karten durch
        deck = deck_orig
        for card in deck:
            # Sequenz für die momentanen Karten
            current_sequence_card = []
            # Menge an Karten, die von dieser Karte benötigt werden
            amount_to_Satisfy = int(card.cardamount)
            # Menge die bereits gefunden wurde
            currently_at_amount = 0
            # Alle Angebote für die Karte
            offers = card.offers
            # Fülle current_sequence card mit den Einträgn der alten shopping_list
            current_sequence_card.extend([x for x in shopping_list_old if x.cardname == card.cardname])
            for item_in_seq in current_sequence_card:
                shopping_list.remove(item_in_seq)
            # Sortiere Angebote nach Preis
            offers.sort(key=lambda x: x.price, reverse=False)
            # Gehe alle Angebote durch
            for offer in offers:
                # Offer ist eine Kopie des Eintrags offer im modeldeck im objekt card
                # Ich kann hier also offer verändern ohne meine tatsählichen Daten zu ändern
                # Offer benötigt hier für meine Sortierung noch den Namen der Karte
                offer.cardname = card.cardname
                # Menge an verfügbaren Karten in sequence
                amount_in_sequence = 0
                # Wenn am Anfang, füge einfach hinzu
                # Setze wieviele Karten eines Typs ich schon hab
                for seq in current_sequence_card:
                    if seq.playset:
                        amount_in_sequence += (seq.amountaviable*4)
                    else:
                        amount_in_sequence += seq.amountaviable
                # Gucke, ob das Angebot schon in der Sequence ist
                # Vergleiche ob Anzahl der Karten reicht
                # Wenn nicht dann füge Angebot hinzu
                if amount_in_sequence < amount_to_Satisfy:
                     current_sequence_card.append(offer)
                # Wenn schon erfüllt, dann Vergleiche
                else:
                    if not any(x.id == offer.id for x in current_sequence_card):
                        # Falls Händler dieses Angebotes schon in der sequence oder der shopping liste ist
                        if any(x.distributorname == offer.distributorname for x in shopping_list) or any(
                                    x.distributorname == offer.distributorname for x in current_sequence_card):
                                    for seq in current_sequence_card:
                                        # Kein Vergleich mit Angebot des Händlers, da es eine sortierte Liste war
                                        # Angebot kann nicht günstiger werden
                                        # if seq.distributorname != offer.distributorname:
                                            # Falls dieser Distributor nicht auch schon einmal vorkam, so wird verglichen, ansonsten wird es wahscheinlich nicht günstiger
                                            if not (any(x.distributorname == seq.distributorname for x in
                                                        current_sequence_card) or any(
                                                    x.distributorname == seq.distributorname for x in shopping_list)):
                                                max_amount_for_seq = 0
                                                if seq.playset:
                                                    if seq.amountaviable * 4 < amount_to_Satisfy:
                                                        max_amount_for_seq = seq.amountaviable * 4
                                                    else:
                                                        max_amount_for_seq = amount_to_Satisfy
                                                    total_price_distributor = max_amount_for_seq * float(seq.price)/float(4)
                                                else:
                                                    if (seq.amountaviable < amount_to_Satisfy):
                                                        max_amount_for_seq = seq.amountaviable
                                                    else:
                                                        max_amount_for_seq = amount_to_Satisfy
                                                    total_price_distributor = max_amount_for_seq * seq.price
                                                offer_playset_mutator = 1
                                                if offer.playset:
                                                    offer_playset_mutator = 4
                                                if float(offer.price)/float(offer_playset_mutator) < self.calculateShipping(seq.location, location,
                                                                                        max_amount_for_seq,
                                                                                        total_price_distributor):
                                                    amount_without_seq = 0
                                                    amount_without_seq = amount_in_sequence - max_amount_for_seq
                                                    # Wenn nach theoretischem entfernen und hinzufügen des neuen Angebots die Anzahl die benötigt wird erreicht wird
                                                    # , so entferne das Angebot aus seq und tausche es durch das neue aus
                                                    if offer.playset:
                                                        if amount_without_seq + offer.amountaviable*4 >= amount_to_Satisfy:
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
                                        if not (any(x.distributorname == seq.distributorname for x in
                                                    current_sequence_card) or any(
                                                x.distributorname == seq.distributorname for x in shopping_list)):
                                            max_amount_for_seq = 0
                                            total_price_seq = 0
                                            if seq.playset:
                                                if seq.amountaviable * 4 < amount_to_Satisfy:
                                                    max_amount_for_seq = seq.amountaviable * 4
                                                else:
                                                    max_amount_for_seq = amount_to_Satisfy
                                                total_price_seq = max_amount_for_seq * float(seq.price) / float(4)
                                            else:
                                                if (seq.amountaviable < amount_to_Satisfy):
                                                    max_amount_for_seq = seq.amountaviable
                                                else:
                                                    max_amount_for_seq = amount_to_Satisfy
                                                total_price_seq = max_amount_for_seq * seq.price
                                            max_amount_for_offer = 0
                                            total_price_offer = 0
                                            if offer.playset:
                                                if offer.amountaviable * 4 < amount_to_Satisfy:
                                                    max_amount_for_offer = offer.amountaviable * 4
                                                else:
                                                    max_amount_for_offer = amount_to_Satisfy
                                                total_price_offer = max_amount_for_offer * float(offer.price) / float(4)
                                            else:
                                                if (offer.amountaviable < amount_to_Satisfy):
                                                    max_amount_for_offer = offer.amountaviable
                                                else:
                                                    max_amount_for_offer = amount_to_Satisfy
                                                total_price_offer = max_amount_for_offer * offer.price
                                            # total_price_seq = max_amount_for_seq * seq.price
                                            # total_price_offer = max_amount_for_offer * offer.price
                                            if self.calculateShipping(offer.location, location, max_amount_for_offer,
                                                                      total_price_offer) < self.calculateShipping(
                                                seq.location, location, max_amount_for_seq, total_price_seq):
                                                amount_without_seq = amount_in_sequence - max_amount_for_seq
                                                # Wenn nach theoretischem entfernen und hinzufügen des neuen Angebots die Anzahl die benötigt wird erreicht wird
                                                # , so entferne das Angebot aus seq und tausche es durch das neue aus
                                                if amount_without_seq + max_amount_for_offer >= amount_to_Satisfy:
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
                    max_amount_item = 0
                    if item.playset:
                        max_amount_item = item.amountaviable * 4
                    else:
                        max_amount_item = item.amountaviable
                    if max_amount_item < amount_to_Satisfy:
                        mutator = 1.0
                        price_per_card = 0
                        if hits > 0:
                            mutator = float(1) / float((1 + hits))
                            shipping = float(max_amount_item) * item.price
                        else:
                            shipping = self.calculateShipping(item.location, location, max_amount_item,
                                                              (max_amount_item * item.price)) * mutator
                        price_per_card = (float(shipping) / float(max_amount_item))
                        current_sequence_card[index].overall_price_per_card = price_per_card
                    else:
                        mutator = 1
                        price_per_card = 0
                        if hits > 0:
                            mutator = float(1) / float((1 + hits))
                            shipping = float(amount_to_Satisfy) * item.price
                        else:
                            shipping = self.calculateShipping(item.location, location, amount_to_Satisfy,
                                                              (amount_to_Satisfy * item.price)) * mutator
                        price_per_card = (float(shipping) / float(amount_to_Satisfy))
                        current_sequence_card[index].overall_price_per_card = price_per_card
            else:
                for index, item in enumerate(current_sequence_card):
                    hits = self.amountofdistributor(current_sequence_card, item.distributorname)
                    hits += self.amountofdistributor(shopping_list, item.distributorname)
                    max_amount_item = 0
                    if item.playset:
                        max_amount_item = item.amountaviable * 4
                    else:
                        max_amount_item = item.amountaviable
                    if max_amount_item < amount_to_Satisfy:
                        if any(x.distributorname == item.distributorname for x in shopping_list):
                            current_sequence_card[index].overall_price_per_card = current_sequence_card[index].price
                        else:
                            mutator = 1.0
                            if hits > 0:
                                mutator = float(1) / float((1 + hits))
                                shipping = float(max_amount_item) * item.price
                            else:
                                shipping = self.calculateShipping(item.location, location, max_amount_item,
                                                                  (max_amount_item * item.price)) * mutator
                            price_per_card = (float(shipping) / float(max_amount_item))
                            current_sequence_card[index].overall_price_per_card = price_per_card
                    else:
                        if any(x.distributorname == item.distributorname for x in shopping_list):
                            current_sequence_card[index].overall_price_per_card = current_sequence_card[index].price
                        else:
                            mutator = 1.0
                            price_per_card = 0
                            if hits > 0:
                                mutator = float(1) / float((1 + hits))
                                shipping = float(amount_to_Satisfy) * item.price
                            else:
                                shipping = self.calculateShipping(item.location, location, amount_to_Satisfy,
                                                                (amount_to_Satisfy * item.price)) * mutator
                            price_per_card = (float(shipping) / float(amount_to_Satisfy))
                            current_sequence_card[index].overall_price_per_card = price_per_card
            # Sortiere die Liste nach overall_price_per_card
            current_sequence_card.sort(key=lambda x: x.overall_price_per_card, reverse=False)
            for ind_item, usable_item in enumerate(current_sequence_card):
                if amount_satisfied == amount_to_Satisfy:
                    break
                else:
                    max_amount_usable_item = 0
                    if usable_item.playset:
                        max_amount_usable_item = usable_item.amountaviable * 4
                    else:
                        max_amount_usable_item = usable_item.amountaviable
                    if (amount_satisfied + max_amount_usable_item) <= amount_to_Satisfy:
                        current_sequence_card[ind_item].amountaviable_used = max_amount_usable_item
                        usable_sequence.append(current_sequence_card[ind_item])
                        amount_satisfied += max_amount_usable_item
                    else:
                        if usable_item.playset:
                            current_sequence_card[ind_item].amountaviable_used = int(math.ceil((amount_to_Satisfy - amount_satisfied)/4))
                        else:
                            current_sequence_card[ind_item].amountaviable_used = amount_to_Satisfy - amount_satisfied
                        amount_satisfied = amount_to_Satisfy
                        usable_sequence.append(current_sequence_card[ind_item])
            shopping_list.extend(usable_sequence)
        return shopping_list

    def minminSearch(self, deck_orig, location):
        shopping_list = []
        deck = deck_orig
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
                # Offer ist eine Kopie des Eintrags offer im modeldeck im objekt card
                # Ich kann hier also offer verändern ohne meine tatsählichen Daten zu ändern
                # Offer benötigt hier für meine Sortierung noch den Namen der Karte
                offer.cardname = card.cardname
                # Menge an verfügbaren Karten in sequence
                amount_in_sequence = 0
                # Wenn am Anfang, füge einfach hinzu
                if current_sequence_card.__len__() == 0:
                    current_sequence_card.append(offer)
                # Wenn schon ein Element gefunden
                else:
                    # Setze wieviele Karten eines Typs ich schon hab
                    for seq in current_sequence_card:
                        if seq.playset:
                            amount_in_sequence += (seq.amountaviable * 4)
                        else:
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
                                    # if seq.distributorname != offer.distributorname:
                                        # Falls dieser Distributor nicht auch schon einmal vorkam, so wird verglichen, ansonsten wird es wahscheinlich nicht günstiger
                                        if not any(x.distributorname == seq.distributorname for x in
                                                   current_sequence_card):
                                            max_amount_for_seq = 0
                                            total_price_distributor = 0
                                            if seq.playset:
                                                if seq.amountaviable * 4 < amount_to_Satisfy:
                                                    max_amount_for_seq = seq.amountaviable * 4
                                                else:
                                                    max_amount_for_seq = amount_to_Satisfy
                                                total_price_distributor = max_amount_for_seq * float(seq.price) / float(
                                                    4)
                                            else:
                                                if (seq.amountaviable < amount_to_Satisfy):
                                                    max_amount_for_seq = seq.amountaviable
                                                else:
                                                    max_amount_for_seq = amount_to_Satisfy
                                                total_price_distributor = max_amount_for_seq * seq.price
                                            offer_playset_mutator = 1
                                            if offer.playset:
                                                offer_playset_mutator = 4
                                            if float(offer.price) / float(offer_playset_mutator) < self.calculateShipping(seq.location, location,
                                                                                    max_amount_for_seq,
                                                                                    total_price_distributor):
                                                amount_without_seq = amount_in_sequence - max_amount_for_seq
                                                # Wenn nach theoretischem entfernen und hinzufügen des neuen Angebots die Anzahl die benötigt wird erreicht wird
                                                # , so entferne das Angebot aus seq und tausche es durch das neue aus
                                                if amount_without_seq + offer.amountaviable * offer_playset_mutator >= amount_to_Satisfy:
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
                                        total_price_seq = 0
                                        if seq.playset:
                                            if seq.amountaviable * 4 < amount_to_Satisfy:
                                                max_amount_for_seq = seq.amountaviable * 4
                                            else:
                                                max_amount_for_seq = amount_to_Satisfy
                                            total_price_seq = max_amount_for_seq * float(seq.price) / float(4)
                                        else:
                                            if (seq.amountaviable < amount_to_Satisfy):
                                                max_amount_for_seq = seq.amountaviable
                                            else:
                                                max_amount_for_seq = amount_to_Satisfy
                                            total_price_seq = max_amount_for_seq * seq.price
                                        max_amount_for_offer = 0
                                        total_price_offer = 0
                                        if offer.playset:
                                            if offer.amountaviable * 4 < amount_to_Satisfy:
                                                max_amount_for_offer = offer.amountaviable * 4
                                            else:
                                                max_amount_for_offer = amount_to_Satisfy
                                            total_price_offer = max_amount_for_offer * float(offer.price) / float(4)
                                        else:
                                            if (offer.amountaviable < amount_to_Satisfy):
                                                max_amount_for_offer = offer.amountaviable
                                            else:
                                                max_amount_for_offer = amount_to_Satisfy
                                            total_price_offer = max_amount_for_offer * offer.price
                                        if self.calculateShipping(offer.location, location, max_amount_for_offer,
                                                                  total_price_offer) < self.calculateShipping(
                                                seq.location, location, max_amount_for_seq, total_price_seq):
                                            amount_without_seq = amount_in_sequence - max_amount_for_seq
                                            # Wenn nach theoretischem entfernen und hinzufügen des neuen Angebots die Anzahl die benötigt wird erreicht wird
                                            # , so entferne das Angebot aus seq und tausche es durch das neue aus
                                            if amount_without_seq + max_amount_for_offer >= amount_to_Satisfy:
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
                            if any(x.distributorname == offer.distributorname for x in shopping_list) or any(
                                            x.distributorname == offer.distributorname for x in current_sequence_card):
                                for seq in current_sequence_card:
                                    # Kein Vergleich mit Angebot des Händlers, da es eine sortierte Liste war
                                    # Angebot kann nicht günstiger werden
                                    # if seq.distributorname != offer.distributorname:
                                        # Falls dieser Distributor nicht auch schon einmal vorkam, so wird verglichen, ansonsten wird es wahscheinlich nicht günstiger
                                        if not (any(x.distributorname == seq.distributorname for x in
                                                    current_sequence_card) or any(
                                                    x.distributorname == seq.distributorname for x in shopping_list)):
                                            max_amount_for_seq = 0
                                            total_price_distributor = 0
                                            if seq.playset:
                                                if seq.amountaviable * 4 < amount_to_Satisfy:
                                                    max_amount_for_seq = seq.amountaviable * 4
                                                else:
                                                    max_amount_for_seq = amount_to_Satisfy
                                                total_price_distributor = max_amount_for_seq * float(seq.price) / float(
                                                    4)
                                            else:
                                                if (seq.amountaviable < amount_to_Satisfy):
                                                    max_amount_for_seq = seq.amountaviable
                                                else:
                                                    max_amount_for_seq = amount_to_Satisfy
                                                total_price_distributor = max_amount_for_seq * seq.price
                                            offer_playset_mutator = 1
                                            if offer.playset:
                                                offer_playset_mutator = 4
                                            if float(offer.price)/float(offer_playset_mutator) < self.calculateShipping(seq.location, location,
                                                                                    max_amount_for_seq,
                                                                                    total_price_distributor):
                                                amount_without_seq = amount_in_sequence - max_amount_for_seq
                                                # Wenn nach theoretischem entfernen und hinzufügen des neuen Angebots die Anzahl die benötigt wird erreicht wird
                                                # , so entferne das Angebot aus seq und tausche es durch das neue aus
                                                if amount_without_seq + offer.amountaviable * offer_playset_mutator >= amount_to_Satisfy:
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
                                    if not (any(x.distributorname == seq.distributorname for x in
                                                current_sequence_card) or any(
                                                x.distributorname == seq.distributorname for x in shopping_list)):
                                        max_amount_for_seq = 0
                                        total_price_seq = 0
                                        if seq.playset:
                                            if seq.amountaviable * 4 < amount_to_Satisfy:
                                                max_amount_for_seq = seq.amountaviable * 4
                                            else:
                                                max_amount_for_seq = amount_to_Satisfy
                                            total_price_seq = max_amount_for_seq * float(seq.price) / float(4)
                                        else:
                                            if (seq.amountaviable < amount_to_Satisfy):
                                                max_amount_for_seq = seq.amountaviable
                                            else:
                                                max_amount_for_seq = amount_to_Satisfy
                                            total_price_seq = max_amount_for_seq * seq.price
                                        max_amount_for_offer = 0
                                        total_price_offer = 0
                                        if offer.playset:
                                            if offer.amountaviable * 4 < amount_to_Satisfy:
                                                max_amount_for_offer = offer.amountaviable * 4
                                            else:
                                                max_amount_for_offer = amount_to_Satisfy
                                            total_price_offer = max_amount_for_offer * float(offer.price) / float(4)
                                        else:
                                            if (offer.amountaviable < amount_to_Satisfy):
                                                max_amount_for_offer = offer.amountaviable
                                            else:
                                                max_amount_for_offer = amount_to_Satisfy
                                            total_price_offer = max_amount_for_offer * offer.price

                                        if self.calculateShipping(offer.location, location, max_amount_for_offer,
                                                                  total_price_offer) < self.calculateShipping(
                                                seq.location, location, max_amount_for_seq, total_price_seq):
                                            amount_without_seq = amount_in_sequence - max_amount_for_seq
                                            # Wenn nach theoretischem entfernen und hinzufügen des neuen Angebots die Anzahl die benötigt wird erreicht wird
                                            # , so entferne das Angebot aus seq und tausche es durch das neue aus
                                            if amount_without_seq + max_amount_for_offer >= amount_to_Satisfy:
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
                    max_amount_item = 0
                    if item.playset:
                        max_amount_item = item.amountaviable * 4
                    else:
                        max_amount_item = item.amountaviable
                    if max_amount_item < amount_to_Satisfy:
                        mutator = 1.0
                        price_per_card = 0
                        if hits > 0:
                            mutator = float(1) / float((1 + hits))
                            shipping = float(max_amount_item) * item.price
                        else:
                            shipping = self.calculateShipping(item.location, location, max_amount_item,
                                                              (max_amount_item * item.price)) * mutator
                        price_per_card = (float(shipping) / float(max_amount_item))
                        current_sequence_card[index].overall_price_per_card = price_per_card
                    else:
                        mutator = 1.0
                        price_per_card = 0
                        if hits > 0:
                            mutator = float(1) / float((1 + hits))
                            shipping = float(amount_to_Satisfy) * item.price
                        else:
                            shipping = self.calculateShipping(item.location, location, amount_to_Satisfy,
                                                              (amount_to_Satisfy * item.price)) * mutator
                        price_per_card = (float(shipping) / float(amount_to_Satisfy))
                        current_sequence_card[index].overall_price_per_card = price_per_card
            else:
                for index, item in enumerate(current_sequence_card):
                    hits = self.amountofdistributor(current_sequence_card, item.distributorname)
                    hits += self.amountofdistributor(shopping_list, item.distributorname)
                    max_amount_item = 0
                    if item.playset:
                        max_amount_item = item.amountaviable * 4
                    else:
                        max_amount_item = item.amountaviable
                    if max_amount_item < amount_to_Satisfy:
                        if any(x.distributorname == item.distributorname for x in shopping_list):
                            current_sequence_card[index].overall_price_per_card = current_sequence_card[index].price
                        else:
                            mutator = 1.0
                            price_per_card = 0
                            if hits > 0:
                                mutator = float(1) / float((1 + hits))
                                shipping = float(max_amount_item) * item.price
                            else:
                                shipping = self.calculateShipping(item.location, location, max_amount_item,
                                                                  (max_amount_item * item.price)) * mutator
                            price_per_card = (shipping / max_amount_item)
                            current_sequence_card[index].overall_price_per_card = price_per_card
                    else:
                        if any(x.distributorname == item.distributorname for x in shopping_list):
                            current_sequence_card[index].overall_price_per_card = current_sequence_card[index].price
                        else:
                            mutator = 1
                            price_per_card = 0
                            if hits > 0:
                                mutator = float(1) / float((1 + hits))
                                shipping = float(amount_to_Satisfy) * item.price
                            else:
                                shipping = self.calculateShipping(item.location, location, amount_to_Satisfy,
                                                                  (amount_to_Satisfy * item.price)) * mutator
                            price_per_card = (float(shipping) / float(amount_to_Satisfy))
                            current_sequence_card[index].overall_price_per_card = price_per_card
            # Sortiere die Liste nach overall_price_per_card
            current_sequence_card.sort(key=lambda x: x.overall_price_per_card, reverse=False)
            for ind_item, usable_item in enumerate(current_sequence_card):
                if amount_satisfied == amount_to_Satisfy:
                    break
                else:
                    max_amount_usable_item = 0
                    if usable_item.playset:
                        max_amount_usable_item = usable_item.amountaviable * 4
                    else:
                        max_amount_usable_item = usable_item.amountaviable
                    if (amount_satisfied + max_amount_usable_item) < amount_to_Satisfy:
                        usable_item.amountaviable_used = max_amount_usable_item
                        usable_sequence.append(usable_item)
                        amount_satisfied += max_amount_usable_item
                    else:
                        if usable_item.playset:
                            current_sequence_card[ind_item].amountaviable_used = int(math.ceil((amount_to_Satisfy - amount_satisfied)/4))
                        else:
                            current_sequence_card[ind_item].amountaviable_used = amount_to_Satisfy - amount_satisfied
                        amount_satisfied = amount_to_Satisfy
                        usable_sequence.append(current_sequence_card[ind_item])
            shopping_list.extend(usable_sequence)
        return shopping_list

    def eval_cost(self, shopping_list, location):
        shopping_list.sort(key=lambda x: x.distributorname, reverse=False)
        buyer_list = []
        temp_buyer = ""
        temp_location = None
        temp_amount = 0
        temp_price = 0
        overall_price = 0
        for item in shopping_list:
            if temp_buyer == "":
                temp_buyer = item.distributorname
                temp_location = item.location
                if item.playset:
                    temp_amount = item.amountaviable_used * 4
                else:
                    temp_amount = item.amountaviable_used
                temp_price = temp_amount * item.price
            else:
                if temp_buyer != item.distributorname:
                    overall_price += self.calculateShipping(temp_location, location, temp_amount, temp_price)
                    temp_location = item.location
                    temp_buyer = item.distributorname
                    if item.playset:
                        temp_amount = item.amountaviable_used * 4
                    else:
                        temp_amount = item.amountaviable_used
                    temp_price = temp_amount * item.price
                else:
                    temp = 0
                    if item.playset:
                        temp = item.amountaviable_used * 4
                        temp_amount += temp
                    else:
                        temp = item.amountaviable_used
                        temp_amount += temp
                    temp_price += temp * item.price
        overall_price += self.calculateShipping(temp_location, location, temp_amount, temp_price)
        return overall_price

    def searchAlgorithm(self):
        queue = Queue()
        # deck variable
        deck = self.model.deck
        # standort
        location = self.model.location
        # alle besten ergebisse
        shopping_list = []
        shopping_list_min = self.minminSearch(deck, location)
        shopping_list = self.local_search(deck, location, copy.deepcopy(shopping_list_min))
        shopping_list.sort(key=lambda x: x.distributorname, reverse=False)
        self.best_solution = copy.deepcopy(shopping_list)
        price_overall = 0
        new_price_overall = self.eval_cost(shopping_list, location)
        change_value = 0
        for i in range(MAX_THREADS):
            queue.put(copy.deepcopy(self.best_solution))
        for i in range(MAX_THREADS):
            worker = threading.Thread(
                target=self.mutator,
                args=(queue, copy.deepcopy(self.model.deck), location),
                name='worker-{}'.format(i),
            )
            worker.setDaemon(True)
            worker.start()
        self.message('*** main thread waiting')
        queue.join()
        ind = 0
        while ind < 5:
            for i in range(MAX_THREADS):
                queue.put(copy.deepcopy(self.best_solution))
            self.message('*** main thread waiting')
            queue.join()
            ind += 1
            print("AHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH + " + str(ind))


        shipping_overall = 0
        amount_temp = 0
        shipping_temp = 0
        price_temp = 0
        last_distributor = ""
        amount_overall = 0
        for item in self.best_solution:
            #if last_distributor == "":
                #last_distributor = item.distributorname
            #if last_distributor != item.distributorname:
                #shipping_temp = 0
            #price_overall += item.overall_price_per_card
            if item.playset:
                amount_overall += item.amountaviable_used * 4
            else:
                amount_overall += item.amountaviable_used
            print("Händler: " + item.distributorname + " Preis pro Karte: " + str(item.price) + " Anzahl der Karten: " + str(item.amountaviable_used)+ " Kartenname: " + item.cardname + " Playset: " + str(item.playset))
        #print(price_overall)
        print(amount_overall)
        print(new_price_overall)
        print(self.eval_cost(self.best_solution, location))
        #new_list = self.random_order(shopping_list, deck, int(len(shopping_list)/2))
        #print(self.eval_cost(new_list, location))
        self.model.shopping_list = self.best_solution