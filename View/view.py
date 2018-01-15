from tkinter import *


class View(Frame):
    def __init__(self, master=None):
        #self.parent = Tk()
        super().__init__(master)
        #self.parent = master
        #self.parent.title("Einkaufshelfer für magickartenmarkt.de")
        #self.title("Einkaufshelfer für magickartenmarkt.de")
        self.master.title("Einkaufshelfer für magickartenmarkt.de")
        self.initialise_ui()
        self.controller = None

    def clear_frame_else(self):
        self.parent.destroy()

    def clear_frame(self):
        #self.frame.quit()
        #self.frame.destroy()
        #self.parent.quit()
        #self.parent.destroy()
        self.quit()
        self.destroy()

    def clear_screen(self):
        """ Clears the screen deleting all widgets. """
        #self.frame.destroy()
        #for widget in self.winfo_children():
           # widget.destroy()
        #self.destroy()
        self.initialise_ui()

    def initialise_ui(self):
        print("Heyho")
        #self.frame = Frame(self.master)
        #self.frame = self.parent.frame
        # self.frame.pack()

    def view(self):
        self.clear_screen()
        #self.frame.grid(sticky="nsew")
        self.grid(sticky="nsew")

    def register(self, controller):
        """ Register a controller to give callbacks to. """
        self.controller = controller

    def main_loop(self):
        mainloop()
