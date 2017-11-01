from tkinter import *
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


class Switch:
    def __init__(self, value): self._val = value

    def __enter__(self): return self

    def __exit__(self, type, value, traceback): return False # Allows traceback to occur

    def __call__(self, cond, *mconds): return self._val in (cond,)+mconds


# ==============================================================================
class Model(object):

    def __init__(self):
        self.username = None
        self.password = None

    def username(self):
        return self.username

    def password(self):
        return self.password


# ==============================================================================
class View(object):
    def __init__(self):
        self.parent = Tk()
        self.parent.title("Einkaufshelfer für magickartenmarkt.de")
        #self.username = ""
        #self.password = ""
        self.initialise_ui()
        self.controller = None

    def clear_screen(self):
        """ Clears the screen deleting all widgets. """
        self.frame.destroy()
        self.initialise_ui()

    def initialise_ui(self):
        self.frame = Frame(self.parent)
        self.frame.pack()

    def viewLogin(self):
        self.clear_screen()
        self.frame.grid(sticky="nsew")

        lbl = Label(self.frame, text="Login für magickartenmarkt.de")
        lbl.grid(sticky="nsew", columnspan=2, padx=10, pady=10)

        lbl_username = Label(self.frame, text="Benutzername")
        lbl_username.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        username = StringVar()
        username_entry = Entry(self.frame, textvariable=username)
        username_entry.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

        lbl_password = Label(self.frame, text="Passwort")
        lbl_password.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        password = StringVar()
        password_entry = Entry(self.frame, textvariable=password)
        password_entry.grid(row=2, column=1, sticky="nsew", padx=5, pady=5)

        btn = Button(self.frame, text="Login", command=lambda: self.clickedLogin(username.get(), password.get()))
        btn.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)

        username_entry.focus()

    def clickedLogin(self, username, password):
        self.controller.login(username, password)

    def viewCard(self):
        self.clear_screen()
        self.frame.grid(sticky="nsew")

        lbl = Label(self.frame, text="Karten die bestellt werden sollen: ")
        lbl.grid(sticky="nsew", columnspan=2, padx=10, pady=10)

        TextArea = Text()
        TextArea.grid(row=1, column=0, sticky="nsew", padx=40, pady=40)
        btn = Button(self.frame, text="Karten prüfen", command=lambda: self.clickedCard(TextArea.get("1.0",'end-1c')))
        btn.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)

    def clickedCard(self, cards):
        self.controller.searchCards(cards)

    def register(self, controller):
        """ Register a controller to give callbacks to. """
        self.controller = controller

    def viewError(self, error):
        toplevel = Toplevel()
        label1 = Label(toplevel, text=error)
        label1.pack()
        button1 = Button(toplevel, text="Ok", command=toplevel.destroy)
        button1.pack()
        toplevel.focus_force()

    def main_loop(self):
        mainloop()


# ==============================================================================
class Controller(object):
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.viewCounter = 0

        self.view.register(self)
        self.update()

    def update(self):
        with Switch(self.viewCounter) as case:
            if case(0):
                self.view.viewLogin()
            elif case(1):
                self.view.viewCard()
            else:
                self.view.viewError()

    def login(self, username, password):
        try:
            #Options to run chrome headless
            options = webdriver.ChromeOptions()
            options.add_argument('headless')
            browser = webdriver.Chrome(chrome_options=options)

            browser.get("https://www.magickartenmarkt.de/")

            # Fetch username, password input boxes and submit button
            username_site = browser.find_element_by_id("username")
            password_site = browser.find_element_by_id("userPassword")
            submit = browser.find_element_by_id("login-btn")

            # Input text in username and password inputboxes
            username_site.send_keys(username)
            password_site.send_keys(password)

            # Click on the submit button
            submit.click()

            #Test if login works
            welcome_user = browser.find_element_by_id("welcomeUsername")
            assert username in welcome_user.text

            browser.quit()
            self.model.username = username
            self.model.password = password
            self.viewCounter += 1
            self.update()
        except (NoSuchElementException, AssertionError):
            browser.quit()
            self.view.viewError("Falscher Benutzername oder Passwort.")
            pass


# ==============================================================================
if (__name__ == "__main__"):
    view = View()
    model = Model()
    controller = Controller(model, view)

    view.main_loop()