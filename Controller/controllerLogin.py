from Controller.controller import *
from View.viewLogin import *
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


class ControllerLogin(Controller):
    def __init__(self, model, view):
        #view = ViewLogin()
        super().__init__(model, view)

    def login(self, username, password):
        try:
            # Options to run chrome headless
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

            # Test if login works
            welcome_user = browser.find_element_by_id("welcomeUsername")
            assert username in welcome_user.text

            browser.quit()
            self.model.username = username
            self.model.password = password
            self.update()
            self.cardSearch()
        except (NoSuchElementException, AssertionError):
            browser.quit()
            self.view.viewError("Falscher Benutzername oder Passwort.")
            pass

    def cardSearch(self):
        self.view.clear_frame()
        #cardSearch()
