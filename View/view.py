from tkinter import *


class View(object):
    def __init__(self):
        self.parent = Tk()
        #self.parent = tk
        self.parent.title("Einkaufshelfer für magickartenmarkt.de")
        self.initialise_ui()
        self.controller = None

    def clear_frame_else(self):
        self.parent.destroy()

    def clear_frame(self):
        self.parent.quit()
        self.parent.destroy()

    def clear_screen(self):
        """ Clears the screen deleting all widgets. """
        self.frame.destroy()
        self.initialise_ui()

    def initialise_ui(self):
        self.frame = Frame(self.parent)
        # self.frame.pack()

    def view(self):
        self.clear_screen()
        self.frame.grid(sticky="nsew")

    def register(self, controller):
        """ Register a controller to give callbacks to. """
        self.controller = controller

    def main_loop(self):
        mainloop()
