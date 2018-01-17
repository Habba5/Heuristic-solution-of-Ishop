from View.view import *
from tkinter import ttk

class ViewAlgorithm(View):
    def __init__(self, master=None):
        super().__init__(master)
        # Zeigt ob Progressbar schon erstellt wurde 0 - Nein, 1 - Ja
        self.running = 0
        # Progressbar
        self.progress = None

    def view(self, *args):
        # Falls keine Argumente übergeben wurden, so erstelle ein einfaches Hinweisfenster
        if not args:
            super().view()
            lbl = Label(self, text="Annäherung an Lösung ...")
            lbl.grid(sticky="nsew", columnspan=2, padx=10, pady=10)
        #Falls Argumente übergeben wurde, so starte oder aktualisiere den Fortschritt
        else:
            size = args[0]
            unfinished = args[1]
            threadstate = args[2]
            if (threadstate == 0):
                if (self.running == 0):
                    self.running = 1
                    super().view()
                    lbl = Label(self, text="Suche nach geeigneten Kombinationen ...")
                    lbl.grid(row=0, sticky="nsew", padx=5, pady=5)
                    # Initialisiere progress
                    self.progress = ttk.Progressbar(self, mode='determinate', maximum=unfinished)
                    self.progress.grid(row=1, sticky="nsew", padx=5, pady=50)
                    self.progress.update_idletasks()
                    self.update()
                else:
                    self.progress['value'] = (size - unfinished)
                    self.progress.update()
            else:
                self.progress.stop()
