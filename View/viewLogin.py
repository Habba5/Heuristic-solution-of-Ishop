from View.view import *


class ViewLogin(View):
    def __init__(self, master=None):
        super().__init__(master)

    def view(self):
        super().view()

        # Erstelle Überschrift
        lbl = Label(self, text="Login für magickartenmarkt.de")
        lbl.grid(sticky="nsew", columnspan=2, padx=10, pady=10)

        # Erstelle Label und Texteingabefeld für Nutzername
        lbl_username = Label(self, text="Benutzername")
        lbl_username.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        # Tkinter variable in der der Input des Textfeldes gespeichert wird
        username = StringVar()
        username_entry = Entry(self, textvariable=username)
        username_entry.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

        # Erstelle Label und Texteingabefeld für Passwort
        lbl_password = Label(self, text="Passwort")
        lbl_password.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        # Tkinter variable in der der Input des Textfeldes gespeichert wird
        password = StringVar()
        password_entry = Entry(self, textvariable=password)
        password_entry.grid(row=2, column=1, sticky="nsew", padx=5, pady=5)

        # Erstelle Button
        btn = Button(self, text="Login", command=lambda: self.clickedLogin(username.get(), password.get()))
        btn.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)
        # Erster Eintrag, der fokussiert werden soll
        username_entry.focus()

    def clickedLogin(self, username, password):
        self.controller.login(username, password)

    def viewError(self, error):
        toplevel = Toplevel()
        label1 = Label(toplevel, text=error)
        label1.pack()
        button1 = Button(toplevel, text="Ok", command=toplevel.destroy)
        button1.pack()
        toplevel.focus_force()



