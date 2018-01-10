from Controller.controller import *
from View.viewLogin import *
import time
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


class ControllerBuy(Controller):
    def __init__(self, modelcred, modeldeck, view):
        #view = ViewLogin()
        self.modelcred = modelcred
        super().__init__(modeldeck, view)
        self.buy()

    def buy(self):
        browser = webdriver.Chrome()
        browser.get("https://www.magickartenmarkt.de/")
        # Fetch username, password input boxes and submit button
        username_site = browser.find_element_by_id("username")
        password_site = browser.find_element_by_id("userPassword")
        submit = browser.find_element_by_id("login-btn")

        # Input text in username and password inputboxes
        username_site.send_keys(self.modelcred.username)
        password_site.send_keys(self.modelcred.password)

        # Click on the submit button
        submit.click()
        shopping_list = self.model.shopping_list
        for item in shopping_list:
            while True:
                time.sleep(1)
                try:
                    id = item.id
                    amount = item.amountaviable
                    script = "jcp('xvNHXYCEKnO%5DD%0B%08r%7Etnv%5C%5D%7BIHT%5DS%25%2A%2A%2A'+encodeURI('"+id+"'+','+"+str(amount)+"+','+'1'),addArticleToSCCallback,false,false,false)"
                    browser.execute_script(str(script))
                    break
                except UnexpectedAlertPresentException as e:
                    print(e)
                    time.sleep()
                    browser.switch_to.alert.accept()
                    browser.switch_to.default_content()
                    pass

        time.sleep(1000)
