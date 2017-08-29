from selenium import webdriver
from selenium.common.exceptions import TimeoutException

browser = webdriver.Firefox()
browser.get("https://www.magickartenmarkt.de/")

# Fetch username, password input boxes and submit button
# This time I'm now testing if the elements were found.
# See the previous exmaples to see how to do that.
username = browser.find_element_by_id("username")
password = browser.find_element_by_id("userPassword")
submit = browser.find_element_by_id("login-btn")

# Input text in username and password inputboxes
username.send_keys("Habba5")
password.send_keys("496257abdr")

# Click on the submit button
submit.click()
