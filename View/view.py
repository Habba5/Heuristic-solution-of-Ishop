from tkinter import *


class View(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master.title("Einkaufshelfer für magickartenmarkt.de")
        self.controller = None

    def clear_frame(self):
        self.quit()
        self.destroy()

    def clear_screen(self):
        for widget in self.winfo_children():
           widget.destroy()

    def view(self):
        self.clear_screen()
        self.grid(sticky="nsew")

    def register(self, controller):
        self.controller = controller

    def main_loop(self):
        mainloop()
