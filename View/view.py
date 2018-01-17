from tkinter import *


class View(Frame):
    # Konstruktor
    def __init__(self, master=None):
        # Konstruktor der Klasse Frame
        super().__init__(master)
        self.master.title("Einkaufshelfer für magickartenmarkt.de")
        self.controller = None

    # Zerstört sich selbst
    # Bendet mainloop
    def clear_frame(self):
        self.quit()
        self.destroy()

    # Zerstöre alle Widgets
    def clear_screen(self):
        for widget in self.winfo_children():
           widget.destroy()

    # clear_screen und erstelle ein grid
    def view(self):
        self.clear_screen()
        self.grid(sticky="nsew")

    # Erhalte Referenz vom Controller
    def register(self, controller):
        self.controller = controller

    # Starte mainloop()
    def main_loop(self):
        mainloop()
