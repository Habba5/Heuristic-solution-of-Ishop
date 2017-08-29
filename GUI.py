from tkinter import *
from tkinter import ttk
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


class Start:
    # global variable
    root = Tk()
    root.title("Einkaufshelfer für magickartenmarkt.de")
    username = StringVar()
    password = StringVar()

    def __init__(self):
        #self.root = Tk()
        #self.root.title("Einkaufshelfer für magickartenmarkt.de")

        # Grid Layout 3x3
        mainframe = ttk.Frame(self.root, padding="2 4 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        # Resizing window
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)

        ttk.Label(mainframe, textvariable="Login für magickartenmarkt.de").grid(column=1, row=1, sticky=(W, E))
        ttk.Label(mainframe, text="Benutzername :").grid(column=1, row=2, sticky=W)
        username_entry = ttk.Entry(mainframe, width=7, textvariable=self.username)
        username_entry.grid(column=2, row=2, sticky=(W, E))
        ttk.Label(mainframe, text="Passwort :").grid(column=1, row=3, sticky=W)
        password_entry = ttk.Entry(mainframe, width=7, textvariable=self.password)
        password_entry.grid(column=2, row=3, sticky=(W, E))

        ttk.Button(mainframe, text="Login", command=self.test_login).grid(column=1, row=4, sticky=W)

        for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)
        username_entry.focus()

        self.root.mainloop()


    def test_login(self):
        try:
            un = self.username.get()
            pw = self.password.get()

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
            username_site.send_keys(un)
            password_site.send_keys(pw)

            # Click on the submit button
            submit.click()

            #Test if login works
            welcome_user = browser.find_element_by_id("welcomeUsername")
            assert un in welcome_user.text

            browser.quit()
        except (NoSuchElementException,AssertionError):
            browser.quit()
            self.clickAbout()
            pass


    def clickAbout(self):
        toplevel = Toplevel()
        label1 = Label(toplevel, text="Falscher Benutzername oder Passwort.")
        label1.pack()
        button1 = Button(toplevel, text="Ok", command=toplevel.destroy)
        button1.pack()
        toplevel.focus_force()

app = Start()