from View.view import *
from tkinter import ttk

class ViewCardSearch(View):
    def __init__(self, master=None):
        super().__init__(master)
        self.running = 0
        self.progress = None

    def view(self):
        super().view()
        # self.clear_screen()
        # self.frame.grid(sticky="nsew")

        lbl = Label(self, text="Karten die bestellt werden sollen: ")
        lbl.grid(row=0, sticky="nsew", padx=5, pady=5)

        TextArea = Text(self)
        TextArea.grid(row=1, column=0, padx=5, pady=5)
        btn = Button(self, text="Karten prüfen", command=lambda: self.clickedCardSearch(TextArea.get("1.0", 'end-1c')))
        btn.grid(row=2, sticky="w", column=0, padx=5, pady=5)

    def testprog(self, size, unfinished, threadstate):
        if(threadstate == 0):
            if(self.running == 0):
                self.running = 1
                toplevel = Toplevel()
                lbl = Label(toplevel, text="Bin am arbeiten")
                lbl.grid(row=0, sticky="nsew", padx=5, pady=5)
                self.progress = ttk.Progressbar(toplevel, mode='determinate', maximum=unfinished)
                self.progress.grid(row=1, sticky="nsew", padx=5, pady=50)
                #self.progress.start()
                self.progress.update_idletasks()
                toplevel.update()
            else:
                #print((size)-unfinished)
                self.progress['value']=(size-unfinished)
                self.progress.update()
        else:
            self.progress.stop()
            self.progress.master.destroy()
            self.master.deiconify()

    def clickedCardSearch(self, cards):
        self.master.withdraw()
        self.controller.searchCards(cards)

    #def shutdown_ttk_repeat(self):
        #self.parent.eval('::ttk::CancelRepeat')
        #self.parent.destroy()

    def viewError(self, error, errorcards):
        toplevel = Toplevel()
        label1 = Label(toplevel, text=error)
        label1.pack()
        label2 = Label(toplevel, text=errorcards)
        label2.pack()
        button1 = Button(toplevel, text="Ok", command=toplevel.destroy)
        button1.pack()
        toplevel.focus_force()
